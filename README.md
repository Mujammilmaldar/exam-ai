# 🧠 AI Practical Generator

A FastAPI-powered server that uses **Google Gemini AI** to generate, search, and manage Python practical code. Type your aim → get code → download instantly.

## 🚀 Quick Start

### 1. Get a Gemini API Key

Go to [Google AI Studio](https://aistudio.google.com/apikey) → Create API Key (free)

### 2. Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_key_here
```

### 3. Run the Server

```bash
# Development (with auto-reload)
uvicorn server:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn server:app --host 0.0.0.0 --port 8000
```

### 4. Use It!

**Browser:** Open `http://localhost:8000`

**curl:**
```bash
# Generate / find a practical
curl -X POST http://localhost:8000/generate -F "aim=chi square test program" -o practical.py

# List all practicals
curl http://localhost:8000/list

# Download specific file
curl http://localhost:8000/download/chi_square_test.py -o chi_square_test.py
```

---

## 🌐 Deploy on Your Server (with Domain)

### Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_read_timeout 120s;  # AI generation can take time
    }
}
```

### Run as Background Service (systemd)

Create `/etc/systemd/system/practical.service`:

```ini
[Unit]
Description=AI Practical Generator
After=network.target

[Service]
User=your_user
WorkingDirectory=/path/to/practical
ExecStart=/usr/bin/uvicorn server:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable practical
sudo systemctl start practical
```

Then from your PC:

```bash
curl -X POST https://yourdomain.com/generate -F "aim=logistic regression iris" -o practical.py
```

---

## 📁 Project Structure

```
practical/
├── server.py          # FastAPI app (all endpoints)
├── ai_engine.py       # Gemini API wrapper
├── storage.py         # File management
├── prompts.py         # AI prompt templates
├── config.py          # Environment config
├── requirements.txt   # Dependencies
├── .env               # Your API key (create from .env.example)
├── practicals/        # Generated & stored code files
└── templates/
    └── index.html     # Browser UI
```

## 🧪 API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Browser UI |
| `/generate` | POST | Generate/find/update practical (main brain) |
| `/list` | GET | List all stored practicals |
| `/download/{filename}` | GET | Download a specific file |
| `/view/{filename}` | GET | View file content as JSON |
| `/delete/{filename}` | DELETE | Delete a practical |
| `/health` | GET | Health check |

## ⚙️ How `/generate` Works

1. 🔍 **Search** — AI semantically matches your aim to existing practicals
2. ✏️ **Update** — If match found, checks if code needs modifications for your aim
3. 🆕 **Generate** — If no match, generates fresh code using Gemini
4. 📥 **Download** — Returns the file (or ZIP if multiple files)
