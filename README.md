# AI Chatbot with Jack Sparrow Personality

A Flask-based chatbot API powered by Google's Gemini 2.0 Flash model, featuring a Captain Jack Sparrow personality and a comprehensive debug-enabled web interface.

## Features

- **AI-Powered Conversations**: Uses Google's Gemini 2.0 Flash model for intelligent responses
- **Character Personality**: Responds as Captain Jack Sparrow with wit and iconic dialogues
- **Session Management**: Persistent conversation history with session-based memory
- **Debug Interface**: Comprehensive debugging tools with real-time logging
- **RESTful API**: Clean API endpoints for integration
- **CORS Enabled**: Cross-origin resource sharing for web applications
- **Health Monitoring**: Built-in health check endpoints

## Project Structure

```
├── chatbot_api.py          # Main Flask API server
├── chatbot_debug.html      # Debug-enabled web interface
├── chatbot_api.log         # Application logs (auto-generated)
├── chat_history.json       # Persistent chat history (auto-generated)
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Prerequisites

- Python 3.8+
- Google AI API key (for Gemini 2.0 Flash)
- Modern web browser (for the frontend)

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-chatbot-jack-sparrow
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API key**
   
   Create a file named `KEYS.py` in a `safe` directory (or modify the path in `chatbot_api.py`):
   ```python
   # KEYS.py
   google_Key = "your_google_ai_api_key_here"
   ```
   
   Alternatively, set the environment variable directly:
   ```bash
   export GOOGLE_API_KEY="your_google_ai_api_key_here"
   ```

## Usage

### Starting the Server

1. **Run the Flask API**
   ```bash
   python chatbot_api.py
   ```

2. **Access the application**
   - Backend API: `http://localhost:5000`
   - Health Check: `http://localhost:5000/health`
   - Web Interface: Open `chatbot_debug.html` in your browser

### Web Interface Features

- **Chat Interface**: Clean, modern chat interface with message history
- **Debug Panel**: Real-time logging and debugging information
- **Connection Testing**: Built-in backend connectivity tests
- **Session Management**: Message count and session tracking
- **Customizable Backend URL**: Configure different backend endpoints

## API Endpoints

### Health Check
```http
GET /health
GET /api/health
```
Returns server status and basic information.

### Chat
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Hello, who are you?",
  "session_id": "default_session"
}
```

### Session Management
```http
GET /api/sessions                           # List all sessions
GET /api/sessions/{session_id}/messages     # Get session messages
POST /api/sessions/{session_id}/clear       # Clear session history
```

### Debug
```http
GET /api/debug/logs                         # Get recent debug logs
```

## Configuration

### Model Settings
- **Model**: Gemini 2.0 Flash
- **Provider**: Google GenAI
- **Temperature**: 0.7 (configurable in `chatbot_api.py`)

### Personality Prompt
The chatbot uses this prompt template:
```
"You are Captain Jack Sparrow. Answer every question with wit and iconic dialogues. Question: {question}"
```

### Logging
- **Log Level**: DEBUG
- **Log File**: `chatbot_api.log`
- **Console Output**: Enabled
- **Log Rotation**: Manual (last 200 debug logs in web interface)

## Development

### Running in Development Mode
The Flask app runs in debug mode by default:
```python
app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
```

### Adding New Features

1. **New API Endpoints**: Add routes in `chatbot_api.py`
2. **Frontend Modifications**: Edit `chatbot_debug.html`
3. **Personality Changes**: Modify the prompt template
4. **Model Configuration**: Update model initialization parameters

### Debug Features

The web interface includes:
- **Real-time Logs**: View API calls, responses, and errors
- **Connection Testing**: Test backend connectivity
- **Message Tracking**: Monitor conversation flow
- **Session Information**: View active sessions and message counts

## Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Failed to load API key
   ```
   **Solution**: Ensure `KEYS.py` exists with valid `google_Key` or set `GOOGLE_API_KEY` environment variable.

2. **Connection Failed**
   ```
   Connection test failed: All endpoints failed
   ```
   **Solution**: Verify the Flask server is running on `http://localhost:5000`.

3. **CORS Errors**
   ```
   Access to fetch blocked by CORS policy
   ```
   **Solution**: CORS is enabled for all origins. Check browser console for specific errors.

4. **Model Initialization Error**
   ```
   Failed to initialize Gemini model
   ```
   **Solution**: Verify API key is valid and has access to Gemini 2.0 Flash.

### Debug Logging

Check `chatbot_api.log` for detailed error information:
```bash
tail -f chatbot_api.log
```

## Security Considerations

- **API Key Protection**: Never commit API keys to version control
- **CORS Policy**: Currently allows all origins - restrict for production
- **Input Validation**: Basic validation implemented - enhance for production use
- **Rate Limiting**: Not implemented - consider adding for production

## Dependencies

### Backend (Python)
- `flask`: Web framework
- `flask-cors`: Cross-origin resource sharing
- `langchain`: AI framework
- `langchain-google-genai`: Google AI integration
- `langchain-community`: Community extensions

### Frontend (JavaScript)
- **Tailwind CSS**: Styling framework (CDN)
- **Vanilla JavaScript**: No additional frameworks required

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request


## Acknowledgments

- Google AI for the Gemini 2.0 Flash model
- LangChain for the AI framework
- Flask community for the web framework
- Pirates of the Caribbean for the inspiration

## Support

For issues and questions:
1. Check the [Issues](../../issues) section
2. Review the debug logs in `chatbot_api.log`
3. Use the built-in debug panel in the web interface
4. Create a new issue with detailed error information

---

**Note**: This is a development version with debug features enabled. For production deployment, consider implementing proper security measures, error handling, and performance optimizations.
