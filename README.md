# Alfapilot - AI Assistant for Microbusiness

Решение для кейса "Разработка copilot-приложения для клиентов микробизнеса" / Альфа-Будущее хакатон

## 🏗️ Архитектура

Проект состоит из двух основных компонентов:

1. **Backend (FastAPI)** - AI сервис с интеграцией OpenRouter API
2. **Bot (Telegram)** - Telegram бот для взаимодействия с пользователями

## 🚀 Быстрый старт

### Предварительные требования

1. Python 3.11+
2. Docker и Docker Compose (опционально)
3. OpenRouter API key (бесплатно: <https://openrouter.ai>)
4. Telegram Bot Token (от @BotFather)

### Настройка окружения

1. **Клонируйте репозиторий**:

```bash
git clone https://github.com/muhammaduss/alfapilot.git
cd alfapilot
```

2. **Создайте .env файл**:

```bash
cp .env.example .env
```

3. **Заполните .env**:

```bash
# Telegram Bot
TOKEN=your_telegram_bot_token

# Backend API
OPENROUTER_API_KEY=your_openrouter_api_key
BACKEND_URL=http://localhost:8000
```

## 📦 Запуск

### Вариант 1: Docker Compose (Рекомендуется)

Запуск обоих сервисов одной командой:

```bash
docker-compose up --build
```

Backend будет доступен на `http://localhost:8000`
Bot автоматически подключится к backend

### Вариант 2: Локальный запуск

#### Backend

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# или: source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Документация API: <http://localhost:8000/docs>

#### Bot

В новом терминале:

```bash
cd bot
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell

pip install -r requirements.txt
python main.py
```

### Вариант 3: Docker (только бот)

```bash
docker build -t alfapilot .
docker run --name alfapilot -e TOKEN=<TELEGRAM_BOT_TOKEN> alfapilot
```

Или из DockerHub:

```bash
docker pull muhammaduss/alfapilot:latest
docker run --name alfapilot -e TOKEN=<TELEGRAM_BOT_TOKEN> muhammaduss/alfapilot
```

## 🧪 Тестирование Backend

После запуска backend:

```bash
cd backend
python test_api.py
```

Или используйте интерактивную документацию: <http://localhost:8000/docs>

## 📚 Документация

- [Backend README](./backend/README.md) - Подробная документация API
- [API Docs](http://localhost:8000/docs) - Swagger UI (после запуска)
- [ReDoc](http://localhost:8000/redoc) - Альтернативная документация

## 🛠️ Возможности

### Backend API

- **Marketing** - Генерация постов для социальных сетей
- **Documents** - Создание деловых документов
- **Legal** - Анализ договоров и юридических рисков
- **Finance** - Финансовый анализ и прогнозирование

### Telegram Bot

- Интеграция со всеми функциями backend
- Удобные клавиатуры и меню
- Поддержка различных типов запросов

## 📁 Структура проекта

```
alfapilot/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI приложение
│   │   ├── models/      # Pydantic схемы
│   │   ├── routers/     # API endpoints
│   │   └── services/    # AI сервисы
│   ├── Dockerfile
│   ├── requirements.txt
│   └── test_api.py
├── bot/                 # Telegram bot
│   ├── handlers/        # Обработчики команд
│   ├── keyboards.py     # Клавиатуры
│   └── main.py         # Точка входа
├── docker-compose.yml   # Оркестрация сервисов
├── .env.example         # Пример конфигурации
└── README.md
```

## 🔧 Разработка

### Добавление нового endpoint

1. Добавьте Pydantic схемы в `backend/app/models/schemas.py`
2. Создайте метод в `backend/app/services/ai_service.py`
3. Добавьте роутер в `backend/app/routers/`
4. Зарегистрируйте роутер в `backend/app/main.py`

### Тестирование

```bash
# Backend
cd backend
python test_api.py

# Bot (ручное тестирование в Telegram)
```

## 🐛 Решение проблем

### Backend не запускается

- Проверьте `.env` файл и наличие `OPENROUTER_API_KEY`
- Убедитесь, что порт 8000 свободен
- Проверьте установку зависимостей: `pip install -r requirements.txt`

### Bot не подключается к backend

- Убедитесь, что backend запущен на `http://localhost:8000`
- Проверьте `BACKEND_URL` в `.env`
- Для Docker: используйте `http://backend:8000` вместо `localhost`

### Ошибки API ключей

- Получите бесплатный ключ на <https://openrouter.ai>
- Проверьте формат ключа в `.env`
- Убедитесь, что ключ активен

## 📝 Лицензия

MIT

## 👥 Команда

Проект для хакатона Альфа-Будущее / Copilot отбор 2025

## 🤝 Вклад

Pull requests приветствуются! Для крупных изменений сначала откройте issue.
