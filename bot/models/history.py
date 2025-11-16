from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserHistory(Base):
    __tablename__ = "user_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    category = Column(String(100), nullable=False)
    request_text = Column(Text, nullable=False)
    response_text = Column(Text)
    response_data = Column(JSON)  # Для хранения структурированных данных
    created_at = Column(DateTime, default=datetime.utcnow)
    message_id = Column(Integer)  # ID сообщения в Telegram для ссылок

    def to_dict(self):
        return {
            "id": self.id,
            "category": self.category,
            "request_text": (
                self.request_text[:100] + "..."
                if len(self.request_text) > 100
                else self.request_text
            ),
            "response_preview": (
                self.response_text[:150] + "..."
                if self.response_text and len(self.response_text) > 150
                else self.response_text
            ),
            "created_at": self.created_at.strftime("%d.%m.%Y %H:%M"),
            "message_id": self.message_id,
        }
