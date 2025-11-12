# 🔧 Troubleshooting Guide - Alfapilot Backend

## ⚠️ Rate Limiting Errors (429)

**Error Message:**
```
"Provider returned error", code: 429
"google/gemini-2.0-flash-exp:free is temporarily rate-limited upstream"
```

**Solution: Switch to a different free model**

### Option 1: Use environment variable (Recommended)

Add to your `.env` file:
```bash
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
```

### Option 2: Available Free Models

Try these models in order if one is rate-limited:

1. **meta-llama/llama-3.2-3b-instruct:free** (Default, most reliable)
   ```bash
   OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
   ```

2. **qwen/qwen-2-7b-instruct:free** (Alternative, good performance)
   ```bash
   OPENROUTER_MODEL=qwen/qwen-2-7b-instruct:free
   ```

3. **google/gemini-2.0-flash-exp:free** (High quality but may have limits)
   ```bash
   OPENROUTER_MODEL=google/gemini-2.0-flash-exp:free
   ```

4. **nousresearch/hermes-3-llama-3.1-405b:free** (Highest quality, slower)
   ```bash
   OPENROUTER_MODEL=nousresearch/hermes-3-llama-3.1-405b:free
   ```

### How to change the model:

1. Open `.env` file in the project root
2. Add or update the line:
   ```
   OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
   ```
3. Restart the backend server
4. Run tests again

## 🔑 API Key Errors (401)

**Error Message:**
```
"No auth credentials found", code: 401
```

**Solution:**

1. Get a free API key from https://openrouter.ai
2. Register/login → Go to "Keys" section → Create new key
3. Copy the key (starts with `sk-or-v1-...`)
4. Add to `.env`:
   ```bash
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   ```
5. Restart backend

## 🚫 Model Not Found (404)

**Error Message:**
```
"No endpoints found for [model-name]", code: 404
```

**Solution:**

The model name is incorrect or deprecated. Update to a current free model:

```bash
OPENROUTER_MODEL=meta-llama/llama-3.2-3b-instruct:free
```

Check available models at: https://openrouter.ai/models?order=newest&supported_parameters=tools&max_price=0

## 🐌 Slow Response Times

**Issue:** API requests take 30-60 seconds

**Causes:**
- First request (cold start) is always slower
- Free models may have queues during peak times
- Model complexity varies

**Solutions:**
1. Use faster model: `meta-llama/llama-3.2-3b-instruct:free`
2. Implement caching for common requests
3. Consider adding your own API keys for better priority

## 🔌 Connection Errors

**Error Message:**
```
"Cannot connect to remote server"
```

**Solution:**

1. Check internet connection
2. Verify OpenRouter status: https://status.openrouter.ai
3. Check firewall settings
4. Try alternative model endpoint

## 📦 Module Not Found Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'httpx'
```

**Solution:**

```powershell
cd backend
pip install -r requirements.txt
```

Or reinstall specific package:
```powershell
pip install httpx python-dotenv fastapi uvicorn
```

## 🔄 Backend Won't Restart

**Issue:** Changes not reflecting after code update

**Solution:**

1. Stop the backend completely (Ctrl+C)
2. Check no Python process is running:
   ```powershell
   Get-Process python | Stop-Process -Force
   ```
3. Wait 2 seconds
4. Start backend again:
   ```powershell
   cd backend
   python app\main.py
   ```

## 🧪 Tests Fail But API Works

**Issue:** Test script fails but Swagger UI works

**Possible causes:**
1. Backend not running on localhost:8000
2. Test timeout too short for free models
3. Rate limiting during test run

**Solutions:**

1. Test individual endpoints in Swagger UI: http://localhost:8000/docs
2. Increase test timeout in `test_api.py` (line with `timeout=60.0` → `timeout=120.0`)
3. Run tests with delays between requests:
   ```python
   await asyncio.sleep(2)  # Add between tests
   ```

## 💾 Environment Variables Not Loading

**Issue:** `.env` file exists but variables not recognized

**Solutions:**

1. Ensure `.env` is in project root (not in `backend/` folder)
2. Check file encoding (should be UTF-8)
3. No spaces around `=`:
   ```bash
   ✅ OPENROUTER_API_KEY=sk-or-v1-...
   ❌ OPENROUTER_API_KEY = sk-or-v1-...
   ```
4. Restart terminal after editing `.env`

## 🌐 CORS Errors (from browser)

**Error Message:**
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Solution:**

Already configured for all origins. If issue persists:

1. Check `backend/app/main.py` has:
   ```python
   allow_origins=["*"]
   ```
2. Clear browser cache
3. Try different browser

## 📝 Still Having Issues?

1. **Check logs**: Look at terminal output for detailed error messages
2. **Test with curl**:
   ```powershell
   curl -X POST http://localhost:8000/api/v1/marketing/generate-posts `
     -H "Content-Type: application/json" `
     -d '{"idea":"test","tone":"professional","target_audience":"general"}'
   ```
3. **Use Swagger UI**: http://localhost:8000/docs for interactive testing
4. **Check OpenRouter dashboard**: See your usage and rate limits
5. **Try different model**: See "Available Free Models" above

## 🆘 Emergency Restart

If everything is broken:

```powershell
# 1. Stop all Python processes
Get-Process python | Stop-Process -Force

# 2. Clean reinstall dependencies
cd backend
pip uninstall -y -r requirements.txt
pip install -r requirements.txt

# 3. Verify .env file
Get-Content ..\.env | Select-String "OPENROUTER"

# 4. Start fresh
python app\main.py
```

---

**Need more help?** Open an issue on GitHub with:
- Error message
- Steps to reproduce
- Your `.env` configuration (without revealing API key)
- Terminal output
