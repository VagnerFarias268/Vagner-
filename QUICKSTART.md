# ⚡ Quick Start Guide

Get up and running in 5 minutes!

## 🚀 Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Environment

```bash
# Copy the example
cp .env.example .env

# Edit with your API keys
# Windows: notepad .env
# Mac/Linux: nano .env
```

**Required Keys:**
- `OPENAI_API_KEY` - Get from https://platform.openai.com/api-keys
- `PINECONE_API_KEY` - Get from https://app.pinecone.io/
- `WHATSAPP_ACCESS_TOKEN` - Get from https://developers.facebook.com/
- `ELEVENLABS_API_KEY` - Get from https://elevenlabs.io/

### 3. Initialize Knowledge Base

```bash
# Add your PDFs to materials/pdfs/
# Add your media to materials/media/
# Edit materials/media_dataset.json

# Then run:
python scripts/init_kb.py
```

### 4. Run the Server

```bash
# Simple way
python run.py

# Or directly
python -m app.main
```

Your server is now running at `http://localhost:8000`! 🎉

Check the health endpoint:
```bash
curl http://localhost:8000/health
```

## 🔗 Setup WhatsApp Webhook

### Development (using ngrok)

```bash
# Install ngrok from https://ngrok.com/
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### Configure in Meta Developer Console

1. Go to https://developers.facebook.com/
2. Select your app → WhatsApp → Configuration
3. Webhook URL: `https://your-url.ngrok.io/webhook`
4. Verify Token: (set in your `.env` as `WHATSAPP_VERIFY_TOKEN`)
5. Subscribe to: **messages**

## 🧪 Test It

### Check Health

```bash
curl http://localhost:8000/health
```

### Check API Docs

Open in browser: http://localhost:8000/docs

### Send a Test Message

Send a WhatsApp message to your configured number and watch the magic! ✨

## 📁 Project Structure

```
app/
  ├── api/routes/       # API endpoints
  ├── core/            # AI, speech, KB logic
  ├── services/        # WhatsApp, payment services
  └── main.py          # Entry point

scripts/
  └── init_kb.py       # Initialize knowledge base

materials/
  ├── pdfs/           # Documents
  ├── media/          # Images/videos
  └── temp/           # Temporary files
```

## 🐳 Docker Quick Start

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🛠️ Common Commands

```bash
# Development with auto-reload
DEBUG=true python run.py

# Re-initialize knowledge base
python scripts/init_kb.py

# Check health
curl localhost:8000/health
```

## ❓ Troubleshooting

**Module not found?**
```bash
pip install -r requirements.txt
```

**Port 8000 in use?**
```bash
# Change port in .env
PORT=8001
```

**Pinecone errors?**
- Check your API key and environment in `.env`
- Make sure index name matches

**WhatsApp not receiving messages?**
- Check ngrok is running
- Verify webhook URL in Meta console
- Check logs: `docker-compose logs -f`

## 📚 Next Steps

- Customize AI prompt in `app/core/ai/prompts.py`
- Add your PDFs and media
- Configure payment links in `.env`
- Read full documentation in `README.md`
- Deploy to production: See `DEPLOYMENT.md`

---

**Need help?** Check `README.md` or open an issue on GitHub.

