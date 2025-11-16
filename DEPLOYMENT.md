# 🚀 Complete Setup & Deployment Guide

## 📋 Prerequisites

- Docker & Docker Compose installed
- Git (for cloning)
- OpenRouter API key (free from https://openrouter.ai)
- Telegram Bot Token (from @BotFather) - optional for bot

## ⚡ Quick Start

### 1. Clone and Configure

```bash
git clone https://github.com/muhammaduss/alfapilot.git
cd alfapilot
```

### 2. Setup Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your credentials:
# - OPENROUTER_API_KEY=your_key_here
# - TOKEN=your_telegram_bot_token (if using bot)
# - DEMO_MODE=true (for testing without API limits)
```

### 3. Start All Services

```bash
docker-compose up --build
```

This will start:
- **Backend** on http://localhost:8000
- **Frontend** on http://localhost:3000
- **Bot** (if configured)

## 🧪 Testing

### Test Backend API
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### Test Frontend
Open http://localhost:3000 in your browser

### Test Backend Endpoints
```bash
# Marketing API
curl -X POST http://localhost:8000/api/v1/marketing/generate-posts \
  -H "Content-Type: application/json" \
  -d '{"idea":"New AI product launch","tone":"professional","target_audience":"startups"}'

# Documents API
curl -X POST http://localhost:8000/api/v1/documents/generate-document \
  -H "Content-Type: application/json" \
  -d '{"doc_type":"business letter","content":"Partnership proposal","style":"formal"}'

# Legal API
curl -X POST http://localhost:8000/api/v1/legal/analyze-contract \
  -H "Content-Type: application/json" \
  -d '{"contract_text":"Service agreement...","analyze_risks":true}'

# Finance API
curl -X POST http://localhost:8000/api/v1/finance/analyze-data \
  -H "Content-Type: application/json" \
  -d '{"data":"Q1 Revenue: $100k, Expenses: $70k","analysis_type":"summary"}'
```

## 🏗️ Architecture

```
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Frontend  │────────>│   nginx     │────────>│   Backend   │
│  (React)    │         │  (proxy)    │         │  (FastAPI)  │
│  Port 3000  │         └─────────────┘         │  Port 8000  │
└─────────────┘                                  └──────┬──────┘
                                                        │
                                                        v
                                                 ┌─────────────┐
                                                 │ OpenRouter  │
                                                 │     API     │
                                                 └─────────────┘
                                                 
┌─────────────┐
│  Telegram   │────────────────────────────────>│   Backend   │
│     Bot     │         HTTP requests            │  Port 8000  │
└─────────────┘                                  └─────────────┘
```

## 🔄 Development Workflow

### Local Development (Without Docker)

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python app/main.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
# Opens on http://localhost:5173
# API requests automatically proxy to backend
```

#### Bot
```bash
cd bot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild after changes
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f bot

# Restart a service
docker-compose restart backend
```

## 🔧 Troubleshooting

### Frontend can't connect to backend

**Symptom:** API errors in browser console

**Solution:**
1. Check backend is running: `curl http://localhost:8000/health`
2. Check nginx config is properly copied in Docker
3. Check browser network tab for actual request URLs
4. Verify CORS is enabled in backend (it is by default)

### Backend rate limiting (429 errors)

**Symptom:** "Provider returned error, code: 429"

**Solution:**
1. Enable DEMO_MODE in `.env`:
   ```
   DEMO_MODE=true
   ```
2. Or wait 10-30 minutes for API limits to reset
3. Or add credits to OpenRouter account

### Docker build fails

**Symptom:** Build errors during `docker-compose up --build`

**Solution:**
1. Check Docker is running
2. Clear Docker cache:
   ```bash
   docker-compose down
   docker system prune -a
   docker-compose up --build
   ```

### Services can't communicate

**Symptom:** Backend/Frontend/Bot connection errors

**Solution:**
1. All services must use service names (not localhost) in Docker:
   - Frontend → Backend: `http://backend:8000`
   - Bot → Backend: `http://backend:8000`
2. Check network configuration in docker-compose.yml
3. Restart all services:
   ```bash
   docker-compose down
   docker-compose up
   ```

## 📝 Environment Variables Reference

### Required
```bash
OPENROUTER_API_KEY=sk-or-v1-...  # Get from https://openrouter.ai
```

### Optional
```bash
TOKEN=<bot_token>                              # Telegram bot token
BACKEND_URL=http://localhost:8000              # Backend URL for bot
DEMO_MODE=true                                 # Use mock responses
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free  # AI model
```

## 🌐 URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 📚 Additional Documentation

- [Backend README](./backend/README.md) - API details
- [Backend QUICKSTART](./backend/QUICKSTART.md) - Backend setup
- [Backend TROUBLESHOOTING](./backend/TROUBLESHOOTING.md) - Common issues

## 🎯 Production Deployment

### Using Docker

```bash
# Build images
docker-compose build

# Push to registry (optional)
docker tag alfapilot-backend:latest your-registry/alfapilot-backend:latest
docker push your-registry/alfapilot-backend:latest

# Deploy on server
docker-compose up -d
```

### Environment Variables for Production

```bash
OPENROUTER_API_KEY=<your_production_key>
TOKEN=<your_bot_token>
DEMO_MODE=false
```

### Nginx for Production (if not using Docker)

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
    }
}
```

## 🔒 Security Notes

1. **Never commit `.env` file** (already in .gitignore)
2. **Rotate API keys regularly**
3. **Use HTTPS in production**
4. **Limit CORS origins in production:**
   ```python
   # backend/app/main.py
   allow_origins=["https://yourdomain.com"]
   ```

## 🆘 Support

- Check logs: `docker-compose logs -f`
- Review documentation in `backend/` folder
- Open GitHub issue with:
  - Error message
  - Steps to reproduce
  - Environment (OS, Docker version)
  - Logs output

---

**Ready to go!** 🎉 Your Alfapilot stack should now be fully functional.
