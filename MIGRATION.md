# 🔄 Migration Guide

This guide helps you migrate from the old flat structure to the new professional FastAPI structure.

## Overview

### Old Structure
```
vagner-sales-agent/
├── main.py
├── kb_manager.py
├── whatsapp_client.py
├── payment_manager.py
├── stt.py
├── tts.py
└── init_kb.py
```

### New Structure
```
vagner-sales-agent/
├── app/
│   ├── api/routes/
│   ├── core/
│   ├── services/
│   └── main.py
├── scripts/
└── tests/
```

## Step-by-Step Migration

### ✅ Already Done

The restructuring has been completed! All your old files have been refactored into the new structure:

| Old File | New Location | Changes |
|----------|-------------|---------|
| `main.py` | `app/main.py` | Simplified, uses new modular structure |
| `kb_manager.py` | `app/core/kb/manager.py` + `app/core/kb/retriever.py` | Split into manager and retriever |
| `whatsapp_client.py` | `app/services/whatsapp.py` | Converted to class-based service |
| `payment_manager.py` | `app/services/payment.py` | Converted to class-based service |
| `stt.py` | `app/core/speech/stt.py` | Moved to speech module |
| `tts.py` | `app/core/speech/tts.py` | Moved to speech module |
| `init_kb.py` | `scripts/init_kb.py` | Moved to scripts folder |

### What You Need to Do

#### 1. Update Your Imports (if you have custom code)

**Old way:**
```python
from kb_manager import add_file_to_kb
from whatsapp_client import send_text
from payment_manager import get_payment_link
```

**New way:**
```python
from app.core.kb.manager import add_file_to_kb
from app.services.whatsapp import get_whatsapp_client
from app.services.payment import get_payment_service

# Usage
whatsapp = get_whatsapp_client()
whatsapp.send_text(phone, message)

payment = get_payment_service()
link = payment.get_payment_link()
```

#### 2. Update Environment Variables

The new structure uses `pydantic-settings` for configuration. Your `.env` file should now include:

```bash
# Add these if not present
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

All other environment variables remain the same!

#### 3. Update Run Commands

**Old way:**
```bash
python main.py
```

**New way:**
```bash
# Option 1: Use the run script
python run.py

# Option 2: Run as module
python -m app.main

# Option 3: Use Docker
docker-compose up -d
```

#### 4. Update Knowledge Base Initialization

**Old way:**
```bash
python init_kb.py
```

**New way:**
```bash
python scripts/init_kb.py
```

## Benefits of New Structure

### ✨ Improvements

1. **Better Organization**: Code is logically separated into modules
2. **Easier Testing**: Each module can be tested independently
3. **Scalability**: Easy to add new features without cluttering
4. **Professional**: Follows FastAPI best practices
5. **Docker Support**: Easy containerization and deployment
6. **Type Safety**: Pydantic models for requests/responses
7. **Logging**: Proper logging infrastructure
8. **Health Checks**: Built-in health monitoring
9. **Documentation**: Auto-generated API docs at `/docs`

### 📦 New Features

- **Health check endpoint**: `GET /health`
- **API documentation**: Visit `/docs` when `DEBUG=true`
- **Docker support**: `docker-compose up -d`
- **Development script**: `python run.py` with nice output
- **Test suite**: `pytest` to run tests
- **Environment validation**: Automatic validation of config

## Backwards Compatibility

### Old Files

Your old files are still in the root directory. You can:

**Option 1: Keep them as backup**
```bash
mkdir old_backup
mv main.py kb_manager.py whatsapp_client.py payment_manager.py stt.py tts.py init_kb.py old_backup/
```

**Option 2: Delete them** (if you're confident everything works)
```bash
rm main.py kb_manager.py whatsapp_client.py payment_manager.py stt.py tts.py init_kb.py
rm kb_manager_continued.py test.py test1.py  # old test files
```

### Custom Code Migration

If you have custom modifications in your old files:

1. **Identify your custom code**: Look for sections you modified
2. **Find equivalent location**: See mapping table above
3. **Apply changes**: Update the new files with your customizations
4. **Test**: Run `pytest` to ensure everything works

## Testing Your Migration

### 1. Check Health

```bash
python run.py
# In another terminal:
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "services": {
    "openai": true,
    "pinecone": true,
    "whatsapp": true,
    "elevenlabs": true
  }
}
```

### 2. Test Knowledge Base

```bash
python scripts/init_kb.py
```

Should complete without errors.

### 3. Test WhatsApp Webhook

Send a test message to your WhatsApp number and verify:
- Message is received
- AI responds correctly
- Audio TTS is sent
- Media is sent when relevant

### 4. Run Test Suite

```bash
pip install -r requirements-dev.txt
pytest
```

## Troubleshooting

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'app'`

**Solution:** Run from project root:
```bash
cd /path/to/vagner-sales-agent
python -m app.main
```

### Configuration Errors

**Error:** `Field required` for environment variables

**Solution:** Check your `.env` file has all required variables:
```bash
# Compare with .env.example
diff .env .env.example
```

### Docker Issues

**Error:** Container won't start

**Solution:** Check logs:
```bash
docker-compose logs -f
```

## Rollback Plan

If something goes wrong, you can rollback:

```bash
# Stop new version
docker-compose down
# or kill the process

# Restore old files
cp old_backup/* .

# Run old version
python main.py
```

## Need Help?

- Check logs: `docker-compose logs -f` or console output
- Review `README.md` for detailed documentation
- Check `DEPLOYMENT.md` for production setup
- Open an issue on GitHub with error details

## Next Steps

After successful migration:

1. ✅ Delete old files (optional)
2. ✅ Update any documentation you have
3. ✅ Update CI/CD pipelines if applicable
4. ✅ Deploy to production (see `DEPLOYMENT.md`)
5. ✅ Celebrate! 🎉

---

**Migration completed successfully?** You can now use all the new features and benefits of the professional FastAPI structure!

