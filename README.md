# AI Coding Assistant

A professional Flask-based coding assistant API powered by Google's Gemini 2.0 Flash model, designed to help developers write, debug, and optimize code with deterministic accuracy.

[![Live Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://chatbotfrontend-two.vercel.app)
[![API Status](https://img.shields.io/badge/API-online-blue)](https://chatbot-iejv.onrender.com/health)
[![Version](https://img.shields.io/badge/version-2.1-orange)](https://github.com/yourusername/ai-coding-assistant)

## 🚀 Live Deployment

- **Frontend (Debug Console):** https://chatbotfrontend-two.vercel.app
- **Backend API:** https://chatbot-iejv.onrender.com
- **Health Check:** https://chatbot-iejv.onrender.com/health

## ✨ Features

### Core Capabilities
- **AI-Powered Code Generation**: Uses Google's Gemini 2.0 Flash with temperature 0.2 for deterministic, accurate responses
- **Professional Coding Assistant**: Specialized in writing clean, well-documented code across multiple languages
- **Multi-Language Support**: Python, JavaScript, Java, C++, and more
- **Code Debugging & Review**: Explains errors, suggests optimizations, and reviews code quality
- **Session-Based Memory**: Maintains conversation context per session
- **Comprehensive Debug Console**: Real-time logging and monitoring interface

### Technical Features
- **RESTful API**: Clean, well-documented endpoints
- **CORS Enabled**: Cross-origin support for web applications
- **Health Monitoring**: Built-in health check and ping endpoints
- **Error Handling**: Robust exception handling with detailed logging
- **Production Ready**: Deployed on Render with environment-based configuration

## 📁 Project Structure

```
ai-coding-assistant/
├── python_chatbot_api.py           # Main Flask API server (V2.1)
├── chatbot_debug.html              # Debug console frontend
├── coding_assistant_api.log        # Application logs (auto-generated)
├── coding_assistant_history.json   # Session history (auto-generated)
├── requirements.txt                # Python dependencies
├── v2.docx                        # Project handover document
└── README.md                      # This file
```

## 🔧 Prerequisites

- **Python**: 3.8 or higher
- **Google AI API Key**: For Gemini 2.0 Flash access
- **Modern Web Browser**: For the debug console interface

## 📦 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-coding-assistant
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

**For Local Development:**
```bash
export GOOGLE_API_KEY="your_google_ai_api_key_here"
```

**For Production (Render):**
Set the environment variable in your Render dashboard:
```
GOOGLE_API_KEY=your_google_ai_api_key_here
```

## 🚀 Usage

### Starting the Server

**Local Development:**
```bash
python python_chatbot_api.py
```

The server will start on `http://localhost:5000`

**Production (Render):**
The server automatically starts using the `PORT` environment variable provided by Render.

### Accessing the Application

- **Backend API:** `http://localhost:5000` (local) or `https://chatbot-iejv.onrender.com` (production)
- **Health Check:** `/health` or `/api/health`
- **Ping Test:** `/ping`
- **Debug Console:** Open `chatbot_debug.html` in your browser

### Debug Console Features

The professional debug console includes:

- **Clean Chat Interface**: Modern, developer-focused UI with JetBrains Mono font
- **Real-Time Logging**: View all API calls, responses, and errors
- **Connection Testing**: Built-in backend connectivity diagnostics
- **Session Management**: Track message count and conversation flow
- **Configurable Backend**: Switch between local and production endpoints
- **Log Controls**: Auto-scroll, detailed logs, and timestamp options

## 📡 API Endpoints

### Health & Status

#### Health Check
```http
GET /health
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Coding Assistant API",
  "model": "gemini-2.0-flash",
  "message": "Coding Assistant API is running",
  "timestamp": "2025-10-01T12:00:00.000000",
  "active_sessions": 2,
  "version": "1.0.0"
}
```

#### Ping
```http
GET /ping
```

**Response:**
```json
{
  "status": "ok",
  "message": "pong",
  "timestamp": "2025-10-01T12:00:00.000000"
}
```

### Chat Operations

#### Send Message
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Write a Python function to reverse a string",
  "session_id": "default_session"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Here's a Python function to reverse a string:\n\n```python\ndef reverse_string(text):\n    \"\"\"\n    Reverse a string.\n    \n    Args:\n        text (str): The string to reverse\n    \n    Returns:\n        str: The reversed string\n    \"\"\"\n    return text[::-1]\n```",
  "session_id": "default_session",
  "message_count": 2,
  "processing_time": 1.23,
  "request_id": "1696176000.123456",
  "timestamp": "2025-10-01T12:00:01.234567"
}
```

### Session Management

#### List All Sessions
```http
GET /api/sessions
```

#### Get Session Messages
```http
GET /api/sessions/{session_id}/messages
```

#### Clear Session
```http
POST /api/sessions/{session_id}/clear
```

### Debug

#### Get Debug Logs
```http
GET /api/debug/logs
```

Returns the last 100 lines from the application log file.

## ⚙️ Configuration

### Model Settings
- **Model:** Gemini 2.0 Flash
- **Provider:** Google GenAI
- **Temperature:** 0.2 (optimized for deterministic code generation)
- **Max Tokens:** Default (configurable)

### System Prompt

The assistant uses an enhanced prompt focused on:
- Writing clean, well-documented code
- Debugging and error explanation
- Code review and optimization
- API development and design patterns
- Best practices and maintainability

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | Yes | None | Google AI API key for Gemini access |
| `PORT` | No | 5000 | Server port (auto-set by Render) |
| `RENDER` | No | None | Production flag (auto-set by Render) |
| `PRODUCTION` | No | None | Alternative production flag |

### Logging

- **Log Level:** DEBUG
- **Log File:** `coding_assistant_api.log`
- **Console Output:** Enabled (stdout/stderr)
- **Log Retention:** Last 200 entries in debug console
- **Format:** `%(asctime)s - %(name)s - %(levelname)s - %(message)s`

## 🛠️ Development

### Project History

| Version | Status | Key Changes |
|---------|--------|-------------|
| **V1** | Prototype | Flask API, in-memory sessions, Jack Sparrow theme |
| **V2** | Professional | Removed character persona, temperature 0.2, enhanced debug console, decoupled hosting |
| **V2.1** | Current | Environment validation, `/ping` endpoint, enhanced prompts, production-ready |

### Running in Development Mode

The Flask app runs with debug mode enabled locally:

```python
app.run(
    host='0.0.0.0',
    port=PORT,
    debug=not IS_PRODUCTION,
    use_reloader=False
)
```

### Testing

#### Local API Tests

**Health Check:**
```bash
curl -X GET "http://localhost:5000/health"
```

**Chat Test:**
```bash
curl -X POST "http://localhost:5000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain Python decorators",
    "session_id": "test_session"
  }'
```

**Production Health Check:**
```bash
curl -X GET "https://chatbot-iejv.onrender.com/health"
```

### Debug Features

The debug console provides:

- **Connection Testing**: Test multiple endpoints automatically
- **Real-Time Logs**: View all system operations as they happen
- **Message Tracking**: Monitor request/response flow
- **Error Diagnostics**: Detailed error information with stack traces
- **Session Info**: Active session count and message statistics

## 🔒 Security & Privacy

### Current Implementation (V2.1)

| Area | Implementation | Status |
|------|----------------|--------|
| **API Keys** | Stored in Render environment variables | ✅ Secure |
| **Chat History** | Non-persistent local JSON file | ⚠️ **Known Issue** |
| **Logs** | Non-persistent local file | ⚠️ **Known Issue** |
| **CORS Policy** | Open (`*`) | ⚠️ Needs Restriction |
| **Rate Limiting** | Not implemented | ⚠️ Planned for V2.1 |
| **Input Validation** | Basic validation | ✅ Operational |

### Known Limitations

#### ⚠️ **CRITICAL: Non-Persistent Storage**

**Problem:** Render's free tier deletes local file system changes on restart.

**Affected Files:**
- `coding_assistant_history.json` (session history)
- `coding_assistant_api.log` (application logs)

**Impact:** All conversation history and logs are lost when the server restarts.

**Planned Fix (V2.1+):** Migrate to PostgreSQL database for persistent storage.

## 🗺️ Roadmap

### V2.1 - Critical Fixes (~5 Days) 🚧

- [ ] **Database Integration**: PostgreSQL for persistent session storage
- [ ] **Cloud Logging**: Migrate from file-based to stdout/stderr logging
- [ ] **Rate Limiting**: Protect API from abuse
- [ ] **CORS Restriction**: Limit to production frontend domain only
- [ ] **WebSocket Support**: Real-time streaming responses (optional)

### V2.2 - Medium Term (4-8 Weeks)

- [ ] **Multi-User Frontend**: User authentication and profiles
- [ ] **Docker Deployment**: Containerized backend
- [ ] **CI/CD Pipeline**: Automated GitHub → Render/Vercel deployment
- [ ] **Enhanced Security**: Request validation, API key rotation
- [ ] **Analytics Dashboard**: Usage statistics and monitoring

## 🐛 Troubleshooting

### Common Issues

#### 1. API Key Error
```
CRITICAL: GOOGLE_API_KEY not found in environment!
```

**Solution:**
```bash
# Local
export GOOGLE_API_KEY='your-key-here'

# Render
Add GOOGLE_API_KEY in Settings → Environment
```

#### 2. Connection Failed
```
Connection test failed: All endpoints failed
```

**Solution:**
- Verify Flask server is running
- Check firewall/network settings
- Ensure correct backend URL in debug console
- Test with: `curl http://localhost:5000/health`

#### 3. History Lost After Restart
```
Session history is empty after server restart
```

**Expected Behavior:** This is a known limitation. History is non-persistent on Render's free tier.

**Workaround:** Upgrade to V2.1 with database integration (coming soon).

#### 4. CORS Errors
```
Access to fetch blocked by CORS policy
```

**Solution:**
- CORS is currently open (`*`) - this should work
- If issues persist, check browser console for specific errors
- Ensure you're using HTTPS for production requests

### Debug Logging

**View Real-Time Logs (Local):**
```bash
tail -f coding_assistant_api.log
```

**View Logs (Render):**
Go to your Render dashboard → Select service → View logs

**Access Logs via API:**
```bash
curl http://localhost:5000/api/debug/logs
```

## 📚 Dependencies

### Backend (Python)
```
flask>=2.3.0              # Web framework
flask-cors>=4.0.0         # CORS support
langchain>=0.1.0          # AI framework
langchain-google-genai>=1.0.0  # Gemini integration
langchain-community>=0.0.20    # Community extensions
gunicorn                  # Production WSGI server
```

### Frontend (JavaScript)
- **Tailwind CSS** (via CDN) - Styling framework
- **JetBrains Mono** (via Google Fonts) - Monospace font
- **Vanilla JavaScript** - No additional frameworks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Test thoroughly (local + production)
5. Commit with clear messages (`git commit -am 'Add new feature'`)
6. Push to branch (`git push origin feature/new-feature`)
7. Create a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Add comprehensive logging for new features
- Update this README for significant changes
- Test both local and production environments
- Document new API endpoints

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Google AI** for the Gemini 2.0 Flash model
- **LangChain** for the AI framework
- **Flask** community for the web framework
- **Vercel** and **Render** for hosting services

## 📞 Support

For issues, questions, or feature requests:

1. **Check Documentation**: Review this README and `v2.docx`
2. **Debug Console**: Use built-in debug panel for diagnostics
3. **Logs**: Check `coding_assistant_api.log` for errors
4. **GitHub Issues**: Create an issue with detailed information
5. **Live Status**: Check https://chatbot-iejv.onrender.com/health

## 📊 Project Status

**Current Version:** V2.1 (Professional Build)  
**Status:** ✅ Functionally Complete  
**Known Issues:** ⚠️ Non-persistent storage (Render free tier limitation)  
**Next Priority:** Database integration for persistence

---

**Last Updated:** October 2025  
**Maintainer:** p krishna surya   
**Documentation Version:** 2.1.0

---

**Note:** This is a production-ready V2.1 release with a known persistence limitation. V2.1+ will address this with PostgreSQL database integration. For immediate production use, consider upgrading to a paid Render tier with persistent disk storage.
