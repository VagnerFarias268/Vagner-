# 🚀 Deployment Guide

This guide covers deploying the Vagner Sales Agent to production.

## Table of Contents

1. [Server Setup](#server-setup)
2. [Docker Deployment](#docker-deployment)
3. [Manual Deployment](#manual-deployment)
4. [Reverse Proxy Setup](#reverse-proxy-setup)
5. [SSL Configuration](#ssl-configuration)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)

## Server Setup

### Minimum Requirements

- **CPU**: 2 cores
- **RAM**: 4GB
- **Storage**: 20GB
- **OS**: Ubuntu 22.04 LTS or later

### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Dependencies

```bash
# Install Python
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install FFmpeg (for audio processing)
sudo apt install ffmpeg -y

# Install Docker (optional but recommended)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt install docker-compose -y
```

## Docker Deployment (Recommended)

### 1. Clone Repository

```bash
cd /opt
sudo git clone <your-repo-url> vagner-sales-agent
cd vagner-sales-agent
sudo chown -R $USER:$USER .
```

### 2. Configure Environment

```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

### 3. Build and Run

```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

### 4. Auto-start on Boot

Create systemd service:

```bash
sudo nano /etc/systemd/system/vagner-agent.service
```

```ini
[Unit]
Description=Vagner Sales Agent
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/vagner-sales-agent
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable vagner-agent
sudo systemctl start vagner-agent
```

## Manual Deployment

### 1. Create Virtual Environment

```bash
cd /opt/vagner-sales-agent
python3.11 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Knowledge Base

```bash
python scripts/init_kb.py
```

### 4. Create Systemd Service

```bash
sudo nano /etc/systemd/system/vagner-agent.service
```

```ini
[Unit]
Description=Vagner Sales Agent
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/vagner-sales-agent
Environment="PATH=/opt/vagner-sales-agent/venv/bin"
ExecStart=/opt/vagner-sales-agent/venv/bin/python -m app.main
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable vagner-agent
sudo systemctl start vagner-agent
sudo systemctl status vagner-agent
```

## Reverse Proxy Setup

### Nginx

Install:

```bash
sudo apt install nginx -y
```

Create config:

```bash
sudo nano /etc/nginx/sites-available/vagner-agent
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for long-running requests
        proxy_connect_timeout 600;
        proxy_send_timeout 600;
        proxy_read_timeout 600;
        send_timeout 600;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/vagner-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Caddy (Easier with Auto-SSL)

Install:

```bash
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

Create Caddyfile:

```bash
sudo nano /etc/caddy/Caddyfile
```

```
your-domain.com {
    reverse_proxy localhost:8000
}
```

Restart:

```bash
sudo systemctl restart caddy
```

## SSL Configuration

### Using Certbot (with Nginx)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

### Auto-renewal

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

## Monitoring

### Application Logs

```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u vagner-agent -f
```

### Health Monitoring

Set up a cron job:

```bash
crontab -e
```

```bash
*/5 * * * * curl -f http://localhost:8000/health || echo "Health check failed" | mail -s "Vagner Agent Down" your@email.com
```

### Resource Monitoring

Install htop:

```bash
sudo apt install htop -y
htop
```

## Backup Strategy

### Automated Backups

```bash
#!/bin/bash
# backup.sh

BACKUP_DIR="/backups/vagner-agent"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup .env
cp /opt/vagner-sales-agent/.env $BACKUP_DIR/env_$DATE

# Backup materials
tar -czf $BACKUP_DIR/materials_$DATE.tar.gz /opt/vagner-sales-agent/materials

# Keep only last 7 days
find $BACKUP_DIR -mtime +7 -delete
```

Add to cron:

```bash
0 2 * * * /path/to/backup.sh
```

## Troubleshooting

### Check Service Status

```bash
sudo systemctl status vagner-agent
```

### Check Logs

```bash
sudo journalctl -u vagner-agent -n 100 --no-pager
```

### Test API Directly

```bash
curl http://localhost:8000/health
```

### Common Issues

**Port already in use:**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

**Permission denied:**
```bash
sudo chown -R www-data:www-data /opt/vagner-sales-agent
```

**Module not found:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Security Checklist

- [ ] Firewall configured (UFW)
- [ ] SSH key authentication only
- [ ] Regular system updates
- [ ] SSL certificate installed
- [ ] Environment variables secured
- [ ] API keys rotated regularly
- [ ] Logs monitored
- [ ] Backups automated
- [ ] Rate limiting enabled
- [ ] Fail2ban installed

## Performance Optimization

### Gunicorn (Multiple Workers)

Install:
```bash
pip install gunicorn
```

Run:
```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Redis Caching (Future)

```bash
sudo apt install redis-server
pip install redis
```

## Scaling

### Horizontal Scaling

Use Docker Swarm or Kubernetes for multi-server deployment.

### Load Balancer

Use Nginx or HAProxy to distribute traffic across multiple instances.

---

For support, check logs first, then review the main README.md.

