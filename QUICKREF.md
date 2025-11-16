# 🎯 Alfapilot - Quick Reference

## 🚀 One-Command Start

```bash
docker-compose up --build
```

## 🔗 URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | React web interface |
| Backend API | http://localhost:8000 | FastAPI backend |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/health | Backend health status |

## 📡 API Endpoints

### Marketing
```bash
POST /api/v1/marketing/generate-posts
Body: {"idea":"...", "tone":"professional", "target_audience":"..."}
```

### Documents
```bash
POST /api/v1/documents/generate-document
Body: {"doc_type":"...", "content":"...", "style":"formal"}
```

### Legal
```bash
POST /api/v1/legal/analyze-contract
Body: {"contract_text":"...", "analyze_risks":true}
```

### Finance
```bash
POST /api/v1/finance/analyze-data
Body: {"data":"...", "analysis_type":"summary"}
```

## ⚙️ Configuration (.env)

```bash
# Required
OPENROUTER_API_KEY=sk-or-v1-...

# Optional
TOKEN=<telegram_bot_token>
DEMO_MODE=true
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Rebuild after code changes
docker-compose up --build

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend
```

## 🧪 Testing

```bash
# Test full stack
.\test_stack.ps1

# Test backend only
cd backend
python test_api.py

# Test health endpoint
curl http://localhost:8000/health
```

## 🔧 Common Issues & Fixes

### Frontend can't reach backend
**Fix:** Check nginx config and restart:
```bash
docker-compose restart frontend
```

### API Rate Limiting (429)
**Fix:** Enable demo mode in `.env`:
```bash
DEMO_MODE=true
```

### Services won't start
**Fix:** Clean rebuild:
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

### Port already in use
**Fix:** Change ports in docker-compose.yml:
```yaml
ports:
  - "8001:8000"  # Backend
  - "3001:80"    # Frontend
```

## 📂 Project Structure

```
alfapilot/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py
│   │   ├── routers/
│   │   ├── services/
│   │   └── models/
│   └── Dockerfile
├── frontend/         # React application
│   ├── src/
│   ├── nginx.conf
│   └── Dockerfile
├── bot/             # Telegram bot
│   └── main.py
├── docker-compose.yml
└── .env
```

## 🎓 Development Mode

### Backend (Local)
```bash
cd backend
python app/main.py
# Runs on http://localhost:8000
```

### Frontend (Local)
```bash
cd frontend
npm run dev
# Runs on http://localhost:5173
# API calls auto-proxy to backend
```

## 📚 Documentation

- **Complete Setup:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Backend Details:** [backend/README.md](backend/README.md)
- **Quick Start:** [backend/QUICKSTART.md](backend/QUICKSTART.md)
- **Troubleshooting:** [backend/TROUBLESHOOTING.md](backend/TROUBLESHOOTING.md)

## 🆘 Need Help?

1. Check logs: `docker-compose logs -f`
2. Run test script: `.\test_stack.ps1`
3. Review troubleshooting guide
4. Check GitHub issues

---

**Happy coding!** 🚀
