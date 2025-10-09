# 🎯 Commands Cheat Sheet

Quick reference for all common commands.

## 🚀 Setup & Installation

```bash
# Clone repository
git clone <repo-url>
cd vagner-sales-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies (code quality tools)
pip install -r requirements-dev.txt

# Setup environment
cp .env.example .env
# Then edit .env with your API keys
```

## 🏃 Running the Application

```bash
# Development mode (recommended)
python run.py

# Production mode
python -m app.main

# With custom port
PORT=8080 python run.py

# With debug mode
DEBUG=true python run.py

# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🐳 Docker Commands

```bash
# Build image
docker build -t vagner-sales-agent .

# Build with docker-compose
docker-compose build

# Start services
docker-compose up -d

# Start in foreground (see logs)
docker-compose up

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f app

# Execute command in container
docker-compose exec app bash

# Rebuild and restart
docker-compose up -d --build

# Remove all containers and volumes
docker-compose down -v
```

## 📚 Knowledge Base

```bash
# Initialize knowledge base
python scripts/init_kb.py

# Add PDFs
# 1. Copy PDFs to materials/pdfs/
# 2. Run init script
python scripts/init_kb.py

# Update media dataset
# 1. Edit materials/media_dataset.json
# 2. Run init script
python scripts/init_kb.py
```

## 🔍 Debugging & Monitoring

```bash
# Check health
curl http://localhost:8000/health

# Check health (formatted)
curl http://localhost:8000/health | python -m json.tool

# View API docs
# Open browser: http://localhost:8000/docs

# Check logs (Docker)
docker-compose logs -f

# Check logs (systemd)
sudo journalctl -u vagner-agent -f

# Monitor container resources
docker stats

# Check container status
docker-compose ps
```

## 🌐 Development Tools

```bash
# Expose local server with ngrok
ngrok http 8000

# Format code with black
black app/ scripts/

# Check code style
flake8 app/

# Sort imports
isort app/

# Type checking
mypy app/

# Security check
pip-audit

# Check outdated packages
pip list --outdated
```

## 📦 Dependency Management

```bash
# Install package
pip install package-name

# Install and add to requirements
pip install package-name
pip freeze > requirements.txt

# Update all packages
pip install --upgrade -r requirements.txt

# Check for security vulnerabilities
pip install pip-audit
pip-audit
```

## 🔧 Configuration

```bash
# View current configuration
cat .env

# Edit configuration
# Windows:
notepad .env
# Mac/Linux:
nano .env

# Validate environment variables
python -c "from app.config import get_settings; print(get_settings())"
```

## 🚀 Deployment

```bash
# Build for production
docker build -t vagner-sales-agent:latest .

# Tag for registry
docker tag vagner-sales-agent:latest registry/vagner-sales-agent:latest

# Push to registry
docker push registry/vagner-sales-agent:latest

# Deploy with docker-compose
docker-compose -f docker-compose.yml up -d

# Check deployment status
docker-compose ps

# View production logs
docker-compose logs --tail=100 -f
```

## 🛠️ Maintenance

```bash
# Backup materials folder
tar -czf materials_backup_$(date +%Y%m%d).tar.gz materials/

# Clean temporary files
rm -rf materials/temp/*

# Clean Docker resources
docker system prune -a

# Clean Python cache
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Update repository
git pull origin main
pip install -r requirements.txt
docker-compose up -d --build
```

## 🔐 Security

```bash
# Generate strong verify token
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Check SSL certificate
openssl s_client -connect yourdomain.com:443

# Test webhook security
curl -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{}'
```

## 📊 System Administration

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
ps aux | grep python

# Kill process on port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
# Then: taskkill /PID <pid> /F

# Check port availability
nc -zv localhost 8000

# Restart service (systemd)
sudo systemctl restart vagner-agent

# Check service status (systemd)
sudo systemctl status vagner-agent
```

## 🐛 Troubleshooting

```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check specific package version
pip show fastapi

# Verify environment variables
env | grep OPENAI
env | grep PINECONE
env | grep WHATSAPP

# Test Pinecone connection
python -c "from app.core.kb.manager import init_pinecone_if_needed; init_pinecone_if_needed()"

# Test OpenAI connection
python -c "from openai import OpenAI; c = OpenAI(); print(c.models.list())"

# Check network connectivity
ping api.openai.com
ping controller.pinecone.io

# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

## 📝 Git Operations

```bash
# Check status
git status

# Add files
git add .

# Commit changes
git commit -m "Your message"

# Push changes
git push origin main

# Pull latest
git pull origin main

# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout main

# Merge branch
git merge feature/new-feature

# View log
git log --oneline
```

## 🎨 Customization

```bash
# Edit AI prompt
# Edit file: app/core/ai/prompts.py

# Edit payment links
# Edit file: .env
# PAYMENT_LINK_NORMAL=...
# PAYMENT_LINK_DISCOUNT40=...
# PAYMENT_LINK_DISCOUNT50=...

# Edit buying intent keywords
# Edit file: app/services/message_handler.py
# Function: detect_buying_intent()

# Edit price objection keywords
# Edit file: app/services/message_handler.py
# Function: handle_price_objection()
```

## 📚 Documentation

```bash
# Generate API documentation
# Run server and visit: http://localhost:8000/docs

# View README
cat README.md

# View quick start
cat QUICKSTART.md

# View deployment guide
cat DEPLOYMENT.md

# View migration guide
cat MIGRATION.md
```

## 🔄 Quick Workflows

### Complete Setup
```bash
git clone <repo>
cd vagner-sales-agent
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env
python scripts/init_kb.py
python run.py
```

### Development Workflow
```bash
# Make changes
# Test changes
pytest
# Run locally
python run.py
# Commit
git add .
git commit -m "Description"
git push
```

### Deploy Updates
```bash
git pull
pip install -r requirements.txt
python scripts/init_kb.py  # if KB changed
docker-compose up -d --build
docker-compose logs -f
```

---

**Pro Tip**: Bookmark this file for quick reference! 📌

