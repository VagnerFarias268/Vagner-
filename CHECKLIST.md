# ✅ Getting Started Checklist

Complete guide to get your Vagner Sales Agent up and running.

## 📋 Pre-Installation Checklist

- [ ] Python 3.11+ installed
- [ ] Git installed (for cloning)
- [ ] Text editor installed (VS Code, Sublime, etc.)
- [ ] Terminal/Command prompt access
- [ ] Internet connection for API calls

### Optional but Recommended
- [ ] Docker & Docker Compose installed
- [ ] ngrok or similar tunneling tool (for development)
- [ ] Postman or similar API testing tool

---

## 🔑 API Keys Checklist

Gather these before starting:

### Required
- [ ] **OpenAI API Key**
  - Sign up: https://platform.openai.com/
  - Create key: https://platform.openai.com/api-keys
  - Note: Requires payment method

- [ ] **Pinecone API Key**
  - Sign up: https://app.pinecone.io/
  - Create index or use existing
  - Free tier available

- [ ] **WhatsApp Cloud API**
  - Meta Developer Account: https://developers.facebook.com/
  - Create App → Add WhatsApp
  - Get: Access Token & Phone Number ID
  - Note: Requires Business verification for production

- [ ] **ElevenLabs API Key**
  - Sign up: https://elevenlabs.io/
  - Get API key from profile
  - Choose Brazilian Portuguese voice
  - Note: Free tier has limits

### Optional
- [ ] Payment gateway links (for checkout)
- [ ] Custom domain (for production)

---

## 🚀 Installation Checklist

### Step 1: Clone & Setup
- [ ] Clone repository
  ```bash
  git clone <repo-url>
  cd vagner-sales-agent
  ```

- [ ] Create virtual environment
  ```bash
  python -m venv venv
  ```

- [ ] Activate virtual environment
  - Windows: `venv\Scripts\activate`
  - Mac/Linux: `source venv/bin/activate`

- [ ] Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

### Step 2: Configuration
- [ ] Copy environment template
  ```bash
  cp .env.example .env
  ```

- [ ] Edit `.env` file with your API keys
  ```bash
  # Windows: notepad .env
  # Mac/Linux: nano .env
  ```

- [ ] Fill in required variables:
  - [ ] `OPENAI_API_KEY`
  - [ ] `PINECONE_API_KEY`
  - [ ] `PINECONE_ENV`
  - [ ] `WHATSAPP_ACCESS_TOKEN`
  - [ ] `WHATSAPP_PHONE_ID`
  - [ ] `ELEVENLABS_API_KEY`
  - [ ] `ELEVEN_VOICE_ID` or `ELEVEN_VOICE_NAME`

- [ ] (Optional) Configure payment links:
  - [ ] `PAYMENT_LINK_NORMAL`
  - [ ] `PAYMENT_LINK_DISCOUNT40`
  - [ ] `PAYMENT_LINK_DISCOUNT50`

### Step 3: Prepare Content
- [ ] Create/verify folders exist:
  - [ ] `materials/pdfs/`
  - [ ] `materials/media/`
  - [ ] `materials/temp/`

- [ ] Add your content:
  - [ ] Place PDF documents in `materials/pdfs/`
  - [ ] Place images/videos in `materials/media/`
  - [ ] Edit `materials/media_dataset.json` with media descriptions

- [ ] (Optional) Add URLs to scrape in `scripts/init_kb.py`

### Step 4: Initialize Knowledge Base
- [ ] Run initialization script
  ```bash
  python scripts/init_kb.py
  ```

- [ ] Verify success messages:
  - [ ] PDFs ingested
  - [ ] URLs scraped (if configured)
  - [ ] Media indexed
  - [ ] No errors

### Step 5: Test Locally
- [ ] Start the server
  ```bash
  python run.py
  ```

- [ ] Verify startup messages
  - [ ] No errors
  - [ ] Server running message
  - [ ] Port displayed

- [ ] Test health endpoint
  ```bash
  curl http://localhost:8000/health
  ```

- [ ] Expected response:
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

- [ ] Open API docs (if DEBUG=true)
  - [ ] Visit: http://localhost:8000/docs
  - [ ] Verify endpoints visible

---

## 🌐 WhatsApp Setup Checklist

### Development Setup (ngrok)
- [ ] Install ngrok from https://ngrok.com/
- [ ] Start ngrok tunnel
  ```bash
  ngrok http 8000
  ```
- [ ] Copy HTTPS URL (e.g., `https://abc123.ngrok.io`)
- [ ] Keep terminal open (ngrok must stay running)

### WhatsApp Configuration
- [ ] Go to https://developers.facebook.com/
- [ ] Select your app
- [ ] Go to WhatsApp → Configuration
- [ ] Click "Edit" on webhook
- [ ] Enter callback URL: `https://your-url.ngrok.io/webhook`
- [ ] Enter verify token (set in `.env` as `WHATSAPP_VERIFY_TOKEN`)
- [ ] Click "Verify and save"
- [ ] Subscribe to webhook fields:
  - [ ] messages
- [ ] Save configuration

### Test WhatsApp Integration
- [ ] Add test phone number in Meta dashboard
- [ ] Send test message from WhatsApp
- [ ] Verify in server logs:
  - [ ] Webhook received
  - [ ] Message processed
  - [ ] Response sent
- [ ] Check WhatsApp for response:
  - [ ] Text message received
  - [ ] Audio message received (TTS)
  - [ ] Media received (if applicable)

---

## 🧪 Manual Testing Checklist
- [ ] Test text message
  - [ ] Send text to WhatsApp
  - [ ] Receive AI response
  - [ ] Verify response is relevant

- [ ] Test audio message
  - [ ] Send voice note to WhatsApp
  - [ ] Verify transcription works
  - [ ] Receive AI response

- [ ] Test buying intent
  - [ ] Send message: "quero comprar"
  - [ ] Verify payment link received
  - [ ] Link is correct

- [ ] Test price objection
  - [ ] Send message: "muito caro"
  - [ ] Verify discount link received
  - [ ] Discount is applied

- [ ] Test media sending
  - [ ] Ask about product
  - [ ] Verify relevant media sent
  - [ ] Media is correct

---

## 🐳 Docker Setup Checklist (Optional)

- [ ] Docker installed and running
- [ ] Docker Compose installed
- [ ] Build image
  ```bash
  docker-compose build
  ```

- [ ] Start services
  ```bash
  docker-compose up -d
  ```

- [ ] Check logs
  ```bash
  docker-compose logs -f
  ```

- [ ] Verify health
  ```bash
  curl http://localhost:8000/health
  ```

- [ ] Test WhatsApp integration (same as above)

---

## 🚀 Production Deployment Checklist

See `DEPLOYMENT.md` for detailed steps.

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Knowledge base initialized
- [ ] Domain name purchased (optional)
- [ ] SSL certificate ready (Let's Encrypt)

### Server Setup
- [ ] Server provisioned (DigitalOcean, AWS, etc.)
- [ ] SSH access configured
- [ ] Firewall configured
- [ ] Docker installed (if using Docker)
- [ ] Reverse proxy configured (Nginx/Caddy)

### Deployment
- [ ] Code deployed to server
- [ ] Environment variables set
- [ ] Services started
- [ ] Health check passing
- [ ] Logs reviewed

### WhatsApp Production
- [ ] Business verification completed
- [ ] Production webhook URL configured
- [ ] Test messages sent successfully
- [ ] Monitoring enabled

### Post-Deployment
- [ ] Monitoring set up
- [ ] Backup strategy configured
- [ ] Alerts configured
- [ ] Documentation updated

---

## 🔧 Customization Checklist

### AI Personality
- [ ] Review `app/core/ai/prompts.py`
- [ ] Customize SYSTEM_PROMPT
- [ ] Test with sample messages
- [ ] Adjust as needed

### Business Logic
- [ ] Review buying intent keywords in `app/services/message_handler.py`
- [ ] Add/remove keywords as needed
- [ ] Test detection accuracy

### Payment Links
- [ ] Set up payment processor
- [ ] Generate payment links
- [ ] Add to `.env`
- [ ] Test checkout flow

### Media Strategy
- [ ] Review media sending logic
- [ ] Adjust fallback percentage (currently 30%)
- [ ] Add more media to dataset
- [ ] Test media relevance

---

## 📊 Monitoring Checklist

### Daily
- [ ] Check server status
- [ ] Review error logs
- [ ] Monitor API usage/costs
- [ ] Check message success rate

### Weekly
- [ ] Review conversation quality
- [ ] Update knowledge base if needed
- [ ] Check for package updates
- [ ] Review analytics

### Monthly
- [ ] Rotate API keys (security)
- [ ] Review and optimize prompts
- [ ] Analyze customer feedback
- [ ] Update documentation

---

## 🆘 Troubleshooting Checklist

If something doesn't work:

### Server Won't Start
- [ ] Check Python version: `python --version`
- [ ] Verify all dependencies installed
- [ ] Check `.env` file exists and has all keys
- [ ] Review error message in console
- [ ] Check port 8000 is available

### Health Check Fails
- [ ] Verify all API keys are correct
- [ ] Check internet connection
- [ ] Test individual services:
  - [ ] OpenAI connection
  - [ ] Pinecone connection
  - [ ] ElevenLabs connection

### Webhook Not Receiving Messages
- [ ] Verify ngrok is running
- [ ] Check webhook URL in Meta dashboard
- [ ] Verify verify token matches
- [ ] Check server logs for errors
- [ ] Test with curl:
  ```bash
  curl -X POST http://localhost:8000/webhook \
    -H "Content-Type: application/json" \
    -d '{}'
  ```

### Messages Not Sending
- [ ] Check WhatsApp access token
- [ ] Verify phone number ID
- [ ] Review Meta API status
- [ ] Check server logs for errors

### Audio Issues
- [ ] Verify FFmpeg installed
- [ ] Check ElevenLabs API key
- [ ] Verify voice ID is correct
- [ ] Check audio file permissions

---

## ✨ Final Checks

Before going live:

- [ ] All tests pass
- [ ] Documentation reviewed
- [ ] Security checklist completed
- [ ] Backup strategy in place
- [ ] Monitoring enabled
- [ ] Team trained (if applicable)
- [ ] Emergency rollback plan ready
- [ ] Support contacts documented

---

## 🎉 Success Criteria

Your setup is complete when:

✅ Server starts without errors  
✅ Health check returns "healthy"  
✅ WhatsApp messages received and processed  
✅ AI responds appropriately  
✅ Audio messages work (TTS)  
✅ Media is sent when relevant  
✅ Payment links sent on buying intent  
✅ All logs show normal operation  

---

## 📚 Next Steps

After successful setup:

1. **Customize**: Adjust prompts and business logic
2. **Test**: Thoroughly test with real scenarios
3. **Monitor**: Set up logging and monitoring
4. **Optimize**: Fine-tune based on usage
5. **Scale**: Add more instances if needed
6. **Document**: Keep your own notes and updates

---

**Need help?** Check the troubleshooting section in `README.md` or review the detailed guides in the documentation folder.

**Ready to go live?** See `DEPLOYMENT.md` for production deployment steps.

**Questions?** Open an issue on GitHub or check the documentation.

Good luck! 🚀

