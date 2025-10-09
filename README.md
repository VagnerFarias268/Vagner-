# 🤖 Vagner Sales Agent

> **WhatsApp AI Sales Agent** with voice support, knowledge base, and automated conversational selling

A production-ready FastAPI application that integrates with WhatsApp Cloud API to provide AI-powered sales conversations in Portuguese. Features include voice message transcription, text-to-speech responses, RAG-based knowledge retrieval, and intelligent payment link distribution.

## 🌟 Features

- **🎯 WhatsApp Integration**: Full webhook support for receiving and sending messages
- **🧠 AI-Powered Responses**: GPT-4 with RAG (Retrieval Augmented Generation) via Pinecone
- **🎤 Voice Support**: 
  - Speech-to-Text using OpenAI Whisper
  - Text-to-Speech using ElevenLabs (Brazilian Portuguese)
- **📚 Knowledge Base**: Ingest PDFs, web pages, and media with semantic search
- **💰 Smart Payment Links**: Context-aware payment link distribution with discount tiers
- **🎨 Media Handling**: Send relevant images/videos based on conversation context
- **📊 Conversation Archiving**: Automatic chat history storage for continuous learning

## 🏗️ Architecture

```
vagner-sales-agent/
├── app/                          # Main application package
│   ├── api/                      # API routes
│   │   └── routes/
│   │       ├── webhook.py        # WhatsApp webhook handler
│   │       └── health.py         # Health check endpoints
│   ├── core/                     # Core business logic
│   │   ├── ai/                   # LLM and prompt management
│   │   ├── speech/               # STT and TTS processing
│   │   └── kb/                   # Knowledge base operations
│   ├── services/                 # External service integrations
│   │   ├── whatsapp.py          # WhatsApp API client
│   │   ├── payment.py           # Payment link service
│   │   └── message_handler.py   # Message processing orchestration
│   ├── models/                   # Pydantic models
│   ├── utils/                    # Utility functions
│   ├── config.py                 # Configuration management
│   └── main.py                   # FastAPI app entry point
├── scripts/                      # Utility scripts
│   └── init_kb.py               # Knowledge base initialization
├── materials/                    # Content files
│   ├── pdfs/                    # Product documentation
│   ├── media/                   # Images and videos
│   └── temp/                    # Temporary files
├── Dockerfile                    # Docker container definition
├── docker-compose.yml           # Docker Compose configuration
└── requirements.txt             # Python dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker & Docker Compose (optional)
- API Keys:
  - OpenAI API key
  - Pinecone API key
  - WhatsApp Cloud API credentials
  - ElevenLabs API key

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd vagner-sales-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your favorite editor
```

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENV`: Your Pinecone environment
- `WHATSAPP_ACCESS_TOKEN`: WhatsApp Cloud API token
- `WHATSAPP_PHONE_ID`: Your WhatsApp Business phone ID
- `ELEVENLABS_API_KEY`: ElevenLabs API key
- `ELEVEN_VOICE_ID`: ElevenLabs voice ID for Brazilian Portuguese

### 3. Prepare Knowledge Base

```bash
# Add your content
# - Place PDFs in materials/pdfs/
# - Place images/videos in materials/media/
# - Update materials/media_dataset.json with media captions

# Initialize the knowledge base
python scripts/init_kb.py
```

### 4. Run the Application

#### Option A: Direct Python

```bash
# Development mode (with auto-reload)
DEBUG=true python -m app.main

# Production mode
python -m app.main
```

#### Option B: Docker Compose

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### 5. Configure WhatsApp Webhook

1. **Expose your server** (development):
   ```bash
   # Using ngrok
   ngrok http 8000
   ```

2. **Configure webhook** in Meta Developer Portal:
   - Webhook URL: `https://your-domain.com/webhook`
   - Verify Token: Set in `.env` as `WHATSAPP_VERIFY_TOKEN`
   - Subscribe to: `messages`

3. **Verify webhook**:
   - Meta will send a GET request to verify
   - Your endpoint will respond with the challenge

## 📡 API Endpoints

### Health Check
```bash
GET /health
```
Returns service status and version information.

### Root
```bash
GET /
```
Returns basic app information.

### Webhook Verification
```bash
GET /webhook?hub.mode=subscribe&hub.challenge=<challenge>&hub.verify_token=<token>
```
WhatsApp webhook verification endpoint.

### Webhook Handler
```bash
POST /webhook
```
Receives and processes WhatsApp messages.

## 🔧 Configuration

### Environment Variables

All configuration is managed via environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `false` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LLM_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `PINECONE_INDEX` | Pinecone index name | `sales-agent-kb` |
| `PAYMENT_LINK_NORMAL` | Normal payment link | - |
| `PAYMENT_LINK_DISCOUNT40` | 40% discount link | - |
| `PAYMENT_LINK_DISCOUNT50` | 50% discount link | - |

### Customization

#### Modify AI Prompt
Edit `app/core/ai/prompts.py` to customize the AI's personality and behavior.

#### Adjust Payment Logic
Modify `app/services/message_handler.py` to customize buying intent detection and discount triggers.

#### Add New Routes
Create new route files in `app/api/routes/` and register them in `app/main.py`.

## 📊 Knowledge Base Management

### Adding Documents

```python
# Via script
python scripts/init_kb.py

# Programmatically
from app.core.kb.manager import add_file_to_kb, add_url_to_kb, add_media_to_kb

# Add PDF
add_file_to_kb("materials/pdfs/product-guide.pdf")

# Add webpage
add_url_to_kb("https://example.com/product")

# Add media with caption
add_media_to_kb("materials/media/demo.jpg", "Product demonstration video")
```

### Media Dataset Format

Edit `materials/media_dataset.json`:

```json
[
  {
    "file": "product-demo.mp4",
    "caption": "Full product demonstration showing all features"
  },
  {
    "file": "before-after.jpg",
    "caption": "Before and after results from real customers"
  }
]
```

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t vagner-sales-agent .

# Run container
docker run -d \
  --name sales-agent \
  -p 8000:8000 \
  --env-file .env \
  vagner-sales-agent
```

### Docker Compose (Recommended)

```bash
# Start services
docker-compose up -d

# Scale if needed
docker-compose up -d --scale app=3

# View logs
docker-compose logs -f app

# Restart
docker-compose restart

# Stop
docker-compose down
```

## 📈 Production Deployment

### Recommended Stack

- **Server**: DigitalOcean, AWS EC2, or Google Cloud
- **Reverse Proxy**: Nginx or Caddy
- **SSL**: Let's Encrypt (automatic with Caddy)
- **Process Manager**: Docker Compose or Systemd

### Example Nginx Configuration

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Security Checklist

- [ ] Set `DEBUG=false` in production
- [ ] Use strong `WHATSAPP_VERIFY_TOKEN`
- [ ] Keep API keys in `.env` (never commit)
- [ ] Enable HTTPS
- [ ] Set up firewall rules
- [ ] Regular dependency updates
- [ ] Monitor logs for suspicious activity

## 🔍 Monitoring

### Health Checks

```bash
# Check service health
curl http://localhost:8000/health

# Expected response
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

### Logs

```bash
# Docker logs
docker-compose logs -f app

# Python logs (when running directly)
# Logs are printed to stdout with timestamps
```

## 🛠️ Development

### Project Commands

```bash
# Format code (if dev dependencies installed)
black app/ scripts/

# Lint (if dev dependencies installed)
flake8 app/

# Type checking (if dev dependencies installed)
mypy app/

# Sort imports (if dev dependencies installed)
isort app/
```

### Adding New Features

1. Create feature branch
2. Add functionality in appropriate module
3. Write tests
4. Update documentation
5. Submit pull request

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for GPT and Whisper
- Pinecone for vector database
- ElevenLabs for Brazilian Portuguese TTS
- Meta for WhatsApp Cloud API
- LangChain for RAG framework

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review API documentation at `/docs` (when `DEBUG=true`)

## 🗺️ Roadmap

- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] CRM integration
- [ ] A/B testing for prompts
- [ ] Custom voice cloning
- [ ] Webhook signature verification
- [ ] Rate limiting
- [ ] Redis caching layer

---

**Made with ❤️ for automated sales conversations**
