# 📋 Project Summary

## Overview

**Vagner Sales Agent** is a production-ready WhatsApp AI sales agent built with FastAPI. It features voice message processing, intelligent responses using GPT-4 with RAG, and automated sales conversion.

## 🎯 Key Features

### 1. **AI Conversations**
- GPT-4 powered responses
- Retrieval Augmented Generation (RAG) via Pinecone
- Context-aware conversations
- Brazilian Portuguese optimized

### 2. **Voice Processing**
- **Speech-to-Text**: OpenAI Whisper for transcription
- **Text-to-Speech**: ElevenLabs with Brazilian Portuguese voice
- OGG format for WhatsApp compatibility

### 3. **Knowledge Base**
- Ingest PDFs, web pages, and media files
- Semantic search with Pinecone vector database
- Automatic conversation archiving
- Media metadata for contextual sending

### 4. **Sales Automation**
- Buying intent detection
- Price objection handling
- Multi-tier discount links (40%/50%)
- Contextual media sharing

### 5. **WhatsApp Integration**
- Webhook for real-time messages
- Text, audio, and media support
- Automatic audio cleanup
- Message acknowledgment

## 🏗️ Architecture

### Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI 0.109.0 |
| **LLM** | OpenAI GPT-4o-mini |
| **Vector DB** | Pinecone 5.0.1 |
| **Orchestration** | LangChain 0.3.26 |
| **STT** | OpenAI Whisper |
| **TTS** | ElevenLabs 0.2.27 |
| **Messaging** | WhatsApp Cloud API |
| **Audio** | Pydub + FFmpeg |

### System Architecture

```
┌─────────────┐
│  WhatsApp   │
│   Messages  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  FastAPI        │
│  /webhook       │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
    ▼          ▼
┌────────┐  ┌──────────┐
│ Speech │  │   Text   │
│  (STT) │  │ Messages │
└───┬────┘  └────┬─────┘
    │            │
    └─────┬──────┘
          │
          ▼
    ┌──────────┐
    │ Message  │
    │ Handler  │
    └─────┬────┘
          │
    ┌─────┼─────┐
    │     │     │
    ▼     ▼     ▼
┌─────┐ ┌───┐ ┌─────┐
│ RAG │ │LLM│ │ KB  │
│     │ │   │ │     │
└──┬──┘ └─┬─┘ └──┬──┘
   │      │     │
   └──────┼─────┘
          │
    ┌─────┴──────┐
    │            │
    ▼            ▼
┌────────┐  ┌─────────┐
│  TTS   │  │  Media  │
│ Audio  │  │  Files  │
└───┬────┘  └────┬────┘
    │            │
    └─────┬──────┘
          │
          ▼
    ┌──────────┐
    │ WhatsApp │
    │ Response │
    └──────────┘
```

## 📁 Project Structure

```
vagner-sales-agent/
│
├── app/                              # Main application
│   ├── api/                          # API layer
│   │   └── routes/
│   │       ├── webhook.py            # WhatsApp webhook
│   │       └── health.py             # Health checks
│   │
│   ├── core/                         # Business logic
│   │   ├── ai/                       # AI/LLM
│   │   │   ├── llm.py               # LLM setup
│   │   │   └── prompts.py           # Prompt templates
│   │   ├── speech/                   # Voice processing
│   │   │   ├── stt.py               # Speech-to-text
│   │   │   └── tts.py               # Text-to-speech
│   │   └── kb/                       # Knowledge base
│   │       ├── manager.py           # KB operations
│   │       └── retriever.py         # LangChain retriever
│   │
│   ├── services/                     # External services
│   │   ├── whatsapp.py              # WhatsApp client
│   │   ├── payment.py               # Payment links
│   │   └── message_handler.py       # Orchestration
│   │
│   ├── models/                       # Data models
│   │   ├── requests.py              # Request models
│   │   └── responses.py             # Response models
│   │
│   ├── utils/                        # Utilities
│   │   ├── text.py                  # Text processing
│   │   └── files.py                 # File handling
│   │
│   ├── config.py                     # Configuration
│   └── main.py                       # App entry point
│
├── scripts/                          # Utility scripts
│   └── init_kb.py                   # KB initialization
│
├── tests/                            # Test suite
│   ├── test_api/
│   ├── test_services/
│   └── test_core/
│
├── materials/                        # Content
│   ├── pdfs/                        # Documents
│   ├── media/                       # Images/videos
│   ├── temp/                        # Temporary files
│   └── media_dataset.json           # Media metadata
│
├── Dockerfile                        # Container definition
├── docker-compose.yml               # Docker orchestration
├── requirements.txt                  # Dependencies
├── requirements-dev.txt             # Dev dependencies
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── pytest.ini                       # Pytest configuration
├── run.py                           # Development runner
│
└── Documentation
    ├── README.md                    # Main documentation
    ├── QUICKSTART.md               # Quick start guide
    ├── DEPLOYMENT.md               # Deployment guide
    ├── MIGRATION.md                # Migration guide
    └── PROJECT_SUMMARY.md          # This file
```

## 🔄 Request Flow

### Incoming Message Flow

1. **WhatsApp sends webhook** → `POST /webhook`
2. **Extract message data** → text or audio
3. **If audio** → Whisper transcription
4. **Query knowledge base** → Pinecone similarity search
5. **Generate AI response** → GPT-4 with context
6. **Archive conversation** → Store in Pinecone
7. **Send text response** → WhatsApp API
8. **Generate TTS audio** → ElevenLabs
9. **Send audio response** → WhatsApp API
10. **Send relevant media** → Based on KB results
11. **Check buying intent** → Send payment link if detected
12. **Handle price objection** → Send discount link if detected

## 🔑 Key Components

### 1. Message Handler
**Location**: `app/services/message_handler.py`

Orchestrates the entire message processing pipeline:
- Text extraction (text/audio)
- KB retrieval
- AI response generation
- Multi-channel response (text + audio + media)
- Intent detection

### 2. Knowledge Base Manager
**Location**: `app/core/kb/manager.py`

Manages Pinecone vector database:
- Document ingestion (PDFs, URLs)
- Media metadata storage
- Conversation archiving
- Semantic search

### 3. WhatsApp Client
**Location**: `app/services/whatsapp.py`

Handles WhatsApp Cloud API:
- Message sending (text, audio, media)
- Media upload/download
- Webhook verification

### 4. AI Engine
**Location**: `app/core/ai/llm.py`

LLM and RAG setup:
- GPT-4 configuration
- RetrievalQA chain
- Prompt template integration

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint |
| GET | `/health` | Health check |
| GET | `/webhook` | Webhook verification |
| POST | `/webhook` | Message handler |
| GET | `/docs` | API documentation (debug mode) |

## 🔐 Environment Variables

### Required
- `OPENAI_API_KEY` - OpenAI API key
- `PINECONE_API_KEY` - Pinecone API key
- `WHATSAPP_ACCESS_TOKEN` - WhatsApp token
- `WHATSAPP_PHONE_ID` - WhatsApp phone ID
- `ELEVENLABS_API_KEY` - ElevenLabs API key

### Optional
- `DEBUG` - Debug mode (default: false)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `LLM_MODEL` - OpenAI model (default: gpt-4o-mini)
- `PINECONE_INDEX` - Index name (default: sales-agent-kb)

See `.env.example` for full list.

## 🚀 Deployment Options

### 1. Docker (Recommended)
```bash
docker-compose up -d
```

### 2. Direct Python
```bash
python run.py
```

### 3. Production Server
- Nginx/Caddy reverse proxy
- Systemd service
- SSL with Let's Encrypt
- See `DEPLOYMENT.md`

## 📊 Performance

### Typical Response Times
- Text message: ~2-4 seconds
- Audio message: ~5-8 seconds (including transcription)
- With media: +1-2 seconds

### Resource Usage
- **CPU**: 1-2 cores
- **RAM**: 2-4GB
- **Storage**: 10GB+ (depends on media)

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app

# Specific test
pytest tests/test_api/test_health.py
```

## 🔧 Customization Points

### 1. AI Personality
Edit `app/core/ai/prompts.py`

### 2. Buying Intent Keywords
Edit `app/services/message_handler.py` → `detect_buying_intent()`

### 3. Payment Links
Configure in `.env`:
- `PAYMENT_LINK_NORMAL`
- `PAYMENT_LINK_DISCOUNT40`
- `PAYMENT_LINK_DISCOUNT50`

### 4. Media Sending Logic
Edit `app/services/message_handler.py` → `send_media_files()`

## 📈 Roadmap

### Planned Features
- [ ] Multi-language support
- [ ] CRM integration (Pipedrive, HubSpot)
- [ ] Analytics dashboard
- [ ] A/B testing for prompts
- [ ] Custom voice cloning
- [ ] Webhook signature verification
- [ ] Rate limiting
- [ ] Redis caching
- [ ] Conversation state management
- [ ] Appointment booking

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit PR

## 📄 License

MIT License - See LICENSE file

## 📞 Support

- **Documentation**: See README.md
- **Quick Start**: See QUICKSTART.md
- **Deployment**: See DEPLOYMENT.md
- **Migration**: See MIGRATION.md
- **Issues**: GitHub Issues

---

**Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production Ready ✅

