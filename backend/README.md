# Alfapilot Backend - FastAPI AI Service

FastAPI backend для AI-функциональности Telegram бота Alfapilot. Использует OpenRouter API с бесплатной моделью `meta-llama/llama-3.2-3b-instruct:free`.

## 🚀 Возможности

- **Marketing**: Генерация постов для соцсетей с различными стилями
- **Documents**: Создание и редактирование документов
- **Legal**: Анализ договоров, выявление рисков
- **Finance**: Финансовый анализ и прогнозирование

## 📋 Требования

- Python 3.11+
- Docker (опционально)
- OpenRouter API Key (бесплатно на https://openrouter.ai)

## 🛠️ Установка и запуск

### Локальный запуск

1. **Создайте .env файл** (скопируйте из .env.example):
```bash
OPENROUTER_API_KEY=your_api_key_here
```

2. **Установите зависимости**:
```bash
cd backend
pip install -r requirements.txt
```

3. **Запустите сервер**:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Откройте документацию**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker запуск

1. **Билд образа**:
```bash
cd backend
docker build -t alfapilot-backend .
```

2. **Запуск контейнера**:
```bash
docker run -p 8000:8000 -e OPENROUTER_API_KEY=your_key alfapilot-backend
```

### Docker Compose (с ботом)

```bash
# В корне проекта
docker-compose up --build
```

## 📡 API Endpoints

### Health Check
```http
GET /health
```

### Marketing
```http
POST /api/v1/marketing/generate-posts
Content-Type: application/json

{
  "idea": "Запуск нового продукта",
  "tone": "professional",
  "target_audience": "молодые предприниматели"
}
```

**Ответ:**
```json
{
  "post_variants": ["вариант 1", "вариант 2", "вариант 3"],
  "suggestions": ["совет 1", "совет 2"]
}
```

### Documents
```http
POST /api/v1/documents/generate-document
Content-Type: application/json

{
  "doc_type": "деловое письмо",
  "content": "Описание содержания письма",
  "style": "formal"
}
```

**Ответ:**
```json
{
  "document": "Текст документа...",
  "corrections": ["исправление 1"],
  "suggestions": ["предложение 1"]
}
```

### Legal
```http
POST /api/v1/legal/analyze-contract
Content-Type: application/json

{
  "contract_text": "Текст договора...",
  "analyze_risks": true
}
```

**Ответ:**
```json
{
  "summary": "Краткое содержание",
  "risks": ["риск 1", "риск 2"],
  "recommendations": ["рекомендация 1"],
  "todo_items": ["задача 1"]
}
```

### Finance
```http
POST /api/v1/finance/analyze-data
Content-Type: application/json

{
  "data": "Финансовые данные...",
  "analysis_type": "summary"
}
```

**Ответ:**
```json
{
  "analysis": "Детальный анализ...",
  "insights": ["инсайт 1", "инсайт 2"],
  "recommendations": ["рекомендация 1"],
  "forecast": {"trend": "positive", "growth": "10%"}
}
```

## 🧪 Тестирование

Запустите тесты после запуска сервера:

```bash
cd backend
python test_api.py
```

Или используйте pytest:
```bash
pytest test_api.py -v
```

## 📁 Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app и настройки
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Pydantic модели
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── marketing.py     # Marketing endpoints
│   │   ├── documents.py     # Documents endpoints
│   │   ├── legal.py         # Legal endpoints
│   │   └── finance.py       # Finance endpoints
│   └── services/
│       ├── __init__.py
│       └── ai_service.py    # OpenRouter интеграция
├── Dockerfile
├── requirements.txt
└── test_api.py              # Тесты API
```

## 🔧 Конфигурация

Все настройки в `.env` файле:

```bash
# OpenRouter API
OPENROUTER_API_KEY=sk-or-v1-...

# Backend settings (опционально)
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0
```

## 🐛 Обработка ошибок

Все endpoints возвращают структурированные ошибки:

```json
{
  "detail": "AI service error: ..."
}
```

Коды ошибок:
- `200`: Успех
- `400`: Некорректный запрос
- `500`: Ошибка сервера или AI API

## 🔒 CORS

CORS настроен для всех источников в development режиме. Для production ограничьте в `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    ...
)
```

## 📝 Лицензия

MIT

## 🤝 Контрибьюция

Для хакатона Альфа Хак / Copilot отбор 2025
