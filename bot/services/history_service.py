import logging
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)


class HistoryService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HistoryService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.engine = None
        self.Session = None
        self._initialize_database()

    def _initialize_database(self):
        """Инициализация базы данных PostgreSQL"""
        db_url = os.getenv("DATABASE_URL")

        if not db_url:
            raise Exception("DATABASE_URL environment variable is required")

        if not db_url.startswith("postgresql://") and not db_url.startswith(
            "postgres://"
        ):
            raise Exception("DATABASE_URL must be a PostgreSQL connection string")

        try:
            self.engine = create_engine(db_url, pool_pre_ping=True, pool_recycle=300)
            self.Session = sessionmaker(bind=self.engine)

            # Создаем таблицы
            self._create_tables()
            logger.info("PostgreSQL database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL database: {e}")
            raise Exception(f"Database initialization failed: {str(e)}")

    def _create_tables(self):
        """Создание таблиц в PostgreSQL"""
        with self.engine.connect() as conn:
            # Check if table exists
            result = conn.execute(
                text(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'user_history'
                    );
                """
                )
            )
            table_exists = result.scalar()

            if not table_exists:
                conn.execute(
                    text(
                        """
                        CREATE TABLE user_history (
                            id SERIAL PRIMARY KEY,
                            user_id BIGINT NOT NULL,
                            category VARCHAR(100) NOT NULL,
                            request_text TEXT NOT NULL,
                            response_text TEXT,
                            response_data TEXT,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            message_id BIGINT
                        );
                        
                        CREATE INDEX idx_user_id ON user_history(user_id);
                        CREATE INDEX idx_created_at ON user_history(created_at);
                    """
                    )
                )
                conn.commit()
                logger.info("Created user_history table")
            else:
                # Проверяем тип столбцов и изменяем если нужно
                self._migrate_columns(conn)

    def _migrate_columns(self, conn):
        """Миграция столбцов к BIGINT если нужно"""
        try:
            # Проверяем тип user_id
            result = conn.execute(
                text(
                    """
                    SELECT data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'user_history' AND column_name = 'user_id'
                """
                )
            )
            user_id_type = result.scalar()

            if user_id_type == "integer":
                logger.info("Migrating user_id from INTEGER to BIGINT")
                conn.execute(
                    text("ALTER TABLE user_history ALTER COLUMN user_id TYPE BIGINT")
                )
                conn.commit()

            # Проверяем тип message_id
            result = conn.execute(
                text(
                    """
                    SELECT data_type 
                    FROM information_schema.columns 
                    WHERE table_name = 'user_history' AND column_name = 'message_id'
                """
                )
            )
            message_id_type = result.scalar()

            if message_id_type == "integer":
                logger.info("Migrating message_id from INTEGER to BIGINT")
                conn.execute(
                    text("ALTER TABLE user_history ALTER COLUMN message_id TYPE BIGINT")
                )
                conn.commit()

        except Exception as e:
            logger.warning(f"Column migration not needed or failed: {e}")

    async def add_record(
        self,
        user_id: int,
        category: str,
        request_text: str,
        response_text: str = None,
        response_data: dict = None,
        message_id: int = None,
    ) -> Optional[int]:
        """Добавление записи в историю"""
        session = self.Session()
        try:
            result = session.execute(
                text(
                    """
                    INSERT INTO user_history 
                    (user_id, category, request_text, response_text, response_data, message_id, created_at)
                    VALUES (:user_id, :category, :request_text, :response_text, :response_data, :message_id, :created_at)
                    RETURNING id
                """
                ),
                {
                    "user_id": user_id,
                    "category": category,
                    "request_text": request_text,
                    "response_text": response_text,
                    "response_data": str(response_data) if response_data else None,
                    "message_id": message_id,
                    "created_at": datetime.utcnow(),
                },
            )
            session.commit()
            record_id = result.scalar()
            logger.info(f"Added history record with ID: {record_id}")
            return record_id
        except SQLAlchemyError as e:
            logger.error(f"Error adding history record: {e}")
            session.rollback()
            return None
        finally:
            session.close()

    async def get_user_history(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Получение истории пользователя"""
        session = self.Session()
        try:
            result = session.execute(
                text(
                    """
                    SELECT id, category, request_text, response_text, created_at, message_id
                    FROM user_history 
                    WHERE user_id = :user_id 
                    ORDER BY created_at DESC 
                    LIMIT :limit OFFSET :offset
                """
                ),
                {"user_id": user_id, "limit": limit, "offset": offset},
            )

            records = []
            for row in result:
                request_preview = row.request_text
                if len(request_preview) > 100:
                    request_preview = request_preview[:100] + "..."

                response_preview = ""
                if row.response_text:
                    response_preview = row.response_text
                    if len(response_preview) > 150:
                        response_preview = response_preview[:150] + "..."

                records.append(
                    {
                        "id": row.id,
                        "category": row.category,
                        "request_text": row.request_text,
                        "request_preview": request_preview,
                        "response_preview": response_preview,
                        "created_at": row.created_at.strftime("%d.%m.%Y %H:%M"),
                        "message_id": row.message_id,
                    }
                )

            return records
        except SQLAlchemyError as e:
            logger.error(f"Error getting user history: {e}")
            return []
        finally:
            session.close()

    async def get_record(
        self, record_id: int, user_id: int = None
    ) -> Optional[Dict[str, Any]]:
        """Получение конкретной записи"""
        session = self.Session()
        try:
            query = "SELECT * FROM user_history WHERE id = :record_id"
            params = {"record_id": record_id}

            if user_id:
                query += " AND user_id = :user_id"
                params["user_id"] = user_id

            result = session.execute(text(query), params)
            row = result.fetchone()

            if row:
                return {
                    "id": row.id,
                    "user_id": row.user_id,
                    "category": row.category,
                    "request_text": row.request_text,
                    "response_text": row.response_text,
                    "response_data": (
                        eval(row.response_data) if row.response_data else None
                    ),
                    "created_at": row.created_at,
                    "message_id": row.message_id,
                }
            return None
        except SQLAlchemyError as e:
            logger.error(f"Error getting record: {e}")
            return None
        finally:
            session.close()

    async def delete_record(self, record_id: int, user_id: int = None) -> bool:
        """Удаление записи"""
        session = self.Session()
        try:
            query = "DELETE FROM user_history WHERE id = :record_id"
            params = {"record_id": record_id}

            if user_id:
                query += " AND user_id = :user_id"
                params["user_id"] = user_id

            result = session.execute(text(query), params)
            session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            logger.error(f"Error deleting record: {e}")
            session.rollback()
            return False
        finally:
            session.close()

    async def get_total_count(self, user_id: int) -> int:
        """Получение общего количества записей пользователя"""
        session = self.Session()
        try:
            result = session.execute(
                text(
                    "SELECT COUNT(*) as count FROM user_history WHERE user_id = :user_id"
                ),
                {"user_id": user_id},
            )
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Error getting total count: {e}")
            return 0
        finally:
            session.close()


# Глобальный экземпляр
history_service = None


def get_history_service():
    """Функция для получения экземпляра сервиса"""
    global history_service
    if history_service is None:
        history_service = HistoryService()
    return history_service
