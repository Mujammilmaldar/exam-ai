# 🚀 Server Deployment Guide

Complete guide to deploy the AI Practical Generator on your Linux server with **Nginx + Gunicorn + Uvicorn**.

---

## Step 1: Push Code to GitHub (from your PC)

```bash
cd practical
git init
git add .
git commit -m "AI Practical Generator"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

---

## Step 2: SSH into Your Server

```bash
ssh your_user@your_server_ip
```

---

## Step 3: Install System Dependencies

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install Python, pip, Nginx
sudo apt install python3 python3-pip python3-venv nginx -y
```

---

## Step 4: Clone Your Repo

```bash
cd /home
sudo mkdir practical-api
sudo chown $USER:$USER practical-api
cd practical-api
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git .
```

---

## Step 5: Setup Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Gunicorn with Uvicorn workers
pip install gunicorn
```

---

## Step 6: Create Your .env File

```bash
cp .env.example .env
nano .env
```

Add your Gemini API key:
```
GEMINI_API_KEY=your_actual_gemini_api_key_here
PRACTICALS_DIR=./practicals
MAX_FILES=10
GEMINI_MODEL=gemini-2.0-flash
```

Save: `Ctrl+O` → `Enter` → `Ctrl+X`

---

## Step 7: Test It Works

```bash
source venv/bin/activate
uvicorn server:app --host 0.0.0.0 --port 8000
```

Open `http://your_server_ip:8000` in browser — if you see the UI, it works! Press `Ctrl+C` to stop.

---

## Step 8: Create Systemd Service (Auto-start on Boot)

```bash
sudo nano /etc/systemd/system/practical.service
```

Paste this (replace `YOUR_USER` with your actual Linux username):

```ini
[Unit]
Description=AI Practical Generator
After=network.target

[Service]
User=YOUR_USER
Group=YOUR_USER
WorkingDirectory=/home/practical-api
Environment="PATH=/home/practical-api/venv/bin"
ExecStart=/home/practical-api/venv/bin/gunicorn server:app \
    --workers 2 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    --timeout 120

Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Save and exit, then:

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable (auto-start on boot)
sudo systemctl enable practical

# Start the service
sudo systemctl start practical

# Check status
sudo systemctl status practical
```

You should see **active (running)** ✅

---

## Step 9: Configure Nginx (Reverse Proxy)

```bash
sudo nano /etc/nginx/sites-available/practical
```

Paste this (replace `yourdomain.com` with your actual domain):

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Max upload size (for future file uploads)
    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout for AI generation (can take time)
        proxy_read_timeout 120s;
        proxy_connect_timeout 120s;
    }
}
```

Save and exit, then:

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/practical /etc/nginx/sites-enabled/

# Remove default site (optional)
sudo rm /etc/nginx/sites-enabled/default

# Test Nginx config
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## Step 10: Setup SSL (HTTPS) with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate (auto-configures Nginx)
sudo certbot --nginx -d yourdomain.com

# Auto-renewal is set up automatically
# Test it:
sudo certbot renew --dry-run
```

---

## ✅ Done! Test Your Deployment

**Browser:**
```
https://yourdomain.com
```

**curl (from your PC):**
```bash
curl -X POST https://yourdomain.com/generate -F "aim=chi square test" -o practical.py
```

**Health check:**
```bash
curl https://yourdomain.com/health
```

---

## 🔧 Useful Commands

```bash
# Check service status
sudo systemctl status practical

# View logs
sudo journalctl -u practical -f

# Restart after code changes
cd /home/practical-api
git pull
sudo systemctl restart practical

# Restart Nginx
sudo systemctl restart nginx

# View Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

---

## 🔄 Updating Code on Server

When you push new changes to GitHub:

```bash
ssh your_user@your_server_ip
cd /home/practical-api
git pull
sudo systemctl restart practical
```

That's it — new code is live! 🚀
