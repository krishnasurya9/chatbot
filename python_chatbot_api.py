import os
import sys
import json
import logging
import traceback
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Your existing imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# --- Logging Setup ---
LOG_FILE = 'coding_assistant_api.log'
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# --- Environment Validation ---
def validate_environment():
    """Validate required environment variables."""
    if "GOOGLE_API_KEY" not in os.environ:
        logger.error("=" * 60)
        logger.error("CRITICAL: GOOGLE_API_KEY not found in environment!")
        logger.error("=" * 60)
        logger.error("Please set it with:")
        logger.error("  export GOOGLE_API_KEY='your-api-key-here'")
        logger.error("Or add it to your .env file for local development")
        logger.error("=" * 60)
        raise EnvironmentError("GOOGLE_API_KEY is required to run the Coding Assistant")
    logger.info("✓ GOOGLE_API_KEY validated successfully")

# Validate environment before proceeding
try:
    validate_environment()
except EnvironmentError as e:
    logger.error(f"Environment validation failed: {e}")
    sys.exit(1)

# --- Constants ---
HISTORY_FILE = "coding_assistant_history.json"
SESSIONS = {}  # Store session data in memory
REQUEST_TIMEOUT = 30  # seconds

# --- Utility Functions ---
def load_history():
    """Load chat history from file."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Loaded {len(data)} messages from history file: {HISTORY_FILE}")
                return data
        logger.info(f"No existing history file found: {HISTORY_FILE}")
        return []
    except Exception as e:
        logger.error(f"Error loading history from {HISTORY_FILE}: {e}")
        return []


def save_history(messages):
    """Save chat history to file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        logger.debug(f"Saved {len(messages)} messages to history file: {HISTORY_FILE}")
    except Exception as e:
        logger.error(f"Error saving history to {HISTORY_FILE}: {e}")


def get_session_data(session_id):
    """Get or create session data."""
    if session_id not in SESSIONS:
        logger.info(f"Creating new session: {session_id}")
        SESSIONS[session_id] = {
            'messages': load_history() if session_id == 'default_session' else [],
            'history': ChatMessageHistory(),
            'created_at': datetime.now().isoformat()
        }

        # Load existing messages into ChatMessageHistory
        for msg in SESSIONS[session_id]['messages']:
            if msg["role"] == "user":
                SESSIONS[session_id]['history'].add_user_message(msg["content"])
            elif msg["role"] == "assistant":
                SESSIONS[session_id]['history'].add_ai_message(msg["content"])

        logger.debug(f"Session {session_id} initialized with {len(SESSIONS[session_id]['messages'])} messages")

    return SESSIONS[session_id]


# --- Model Setup ---
try:
    logger.info("Initializing Gemini 2.0 Flash model for Coding Assistant...")
    model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.2  # Lower temperature for deterministic, accurate coding results
    )
    logger.info("✓ Gemini 2.0 Flash model initialized successfully")
    logger.debug(f"Model configuration: gemini-2.0-flash, temperature=0.2")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {e}")
    logger.error("Make sure GOOGLE_API_KEY is set correctly in environment variables.")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise

# --- Enhanced Prompt Template ---
SYSTEM_PROMPT = (
    "You are a professional Coding Assistant powered by Gemini 2.0 Flash. "
    "Your expertise includes:\n"
    "- Writing clean, well-documented code in multiple languages (Python, JavaScript, Java, C++, etc.)\n"
    "- Debugging code and explaining error messages clearly\n"
    "- Code review with optimization and best practice suggestions\n"
    "- API development, integration, and RESTful design\n"
    "- Design patterns, algorithms, and data structures\n"
    "- DevOps, deployment, and infrastructure guidance\n\n"
    "Guidelines:\n"
    "- ALWAYS format code in markdown code blocks with proper language syntax highlighting\n"
    "- Provide clear explanations alongside code examples\n"
    "- Ask clarifying questions when requirements are ambiguous\n"
    "- Include inline comments for complex logic\n"
    "- Suggest improvements, alternatives, and potential edge cases\n"
    "- Be concise but thorough in explanations\n"
    "- Prioritize readability and maintainability\n\n"
    "Question: {question}"
)

prompt_template = ChatPromptTemplate.from_template(SYSTEM_PROMPT)
logger.info("✓ Enhanced Coding Assistant prompt template created")

# Test the model initialization
try:
    logger.info("Testing model with prompt template...")
    test_chain = prompt_template | model
    logger.info("✓ Model and prompt template chain created successfully")
except Exception as e:
    logger.error(f"Failed to create model chain: {e}")
    raise


# --- Memory Setup ---
def get_history_for_session(session_id: str):
    """Return a message history object for a given session."""
    session_data = get_session_data(session_id)
    return session_data['history']


# Create conversation chain
try:
    logger.info("Creating RunnableWithMessageHistory conversation chain...")
    conversation = RunnableWithMessageHistory(
        prompt_template | model,
        get_history_for_session,
        input_messages_key="question",
        history_messages_key="history",
    )
    logger.info("✓ Conversation chain with memory created successfully")
except Exception as e:
    logger.error(f"Failed to create conversation chain: {e}")
    logger.error(f"Error details: {traceback.format_exc()}")
    raise

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app, origins=["*"])
logger.info("✓ Flask app initialized with CORS enabled for all origins")


# --- API Endpoints ---

@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        logger.debug("Health check requested")
        return jsonify({
            "status": "healthy",
            "service": "Coding Assistant API",
            "model": "gemini-2.0-flash",
            "message": "Coding Assistant API is running",
            "timestamp": datetime.now().isoformat(),
            "active_sessions": len(SESSIONS),
            "version": "1.0.0"
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/ping', methods=['GET'])
def ping():
    """Simple ping endpoint for connectivity testing."""
    logger.debug("Ping requested")
    return jsonify({
        "status": "ok",
        "message": "pong",
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint for coding assistance."""
    start_time = datetime.now()
    request_id = f"{start_time.timestamp()}"

    try:
        logger.info(f"[{request_id}] Chat request received")

        if not request.is_json:
            logger.error(f"[{request_id}] Invalid request format - not JSON")
            return jsonify({
                "success": False,
                "error": "Request must be JSON",
                "timestamp": datetime.now().isoformat()
            }), 400

        data = request.get_json()
        logger.debug(f"[{request_id}] Request data: {data}")

        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default_session')

        if not message:
            logger.error(f"[{request_id}] Empty message provided")
            return jsonify({
                "success": False,
                "error": "Message cannot be empty",
                "timestamp": datetime.now().isoformat()
            }), 400

        logger.info(f"[{request_id}] Processing message for session '{session_id}': '{message[:100]}...'")

        session_data = get_session_data(session_id)

        logger.debug(f"[{request_id}] Invoking conversation chain")
        response = conversation.invoke(
            {"question": message},
            config={"configurable": {"session_id": session_id}}
        )

        bot_reply = getattr(response, "content", str(response))
        logger.debug(f"[{request_id}] Bot response generated: '{bot_reply[:100]}...'")

        # Update session messages
        session_data['messages'].append({
            "role": "user",
            "content": message,
            "timestamp": start_time.isoformat()
        })
        session_data['messages'].append({
            "role": "assistant",
            "content": bot_reply,
            "timestamp": datetime.now().isoformat()
        })

        # Save only the default session to file for persistence
        if session_id == 'default_session':
            save_history(session_data['messages'])

        processing_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"[{request_id}] ✓ Request processed successfully in {processing_time:.2f}s")

        return jsonify({
            "success": True,
            "response": bot_reply,
            "session_id": session_id,
            "message_count": len(session_data['messages']),
            "processing_time": processing_time,
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        error_details = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "processing_time": processing_time,
            "request_id": request_id,
            "timestamp": datetime.now().isoformat()
        }

        logger.error(f"[{request_id}] ✗ Chat request failed: {error_details}")

        return jsonify({
            "success": False,
            "error": str(e),
            "response": f"Sorry, the Coding Assistant encountered an error: {str(e)}",
            "error_details": error_details
        }), 500


@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """Get all active sessions."""
    try:
        logger.debug("Sessions list requested")
        sessions_info = {}
        for session_id, session_data in SESSIONS.items():
            sessions_info[session_id] = {
                "message_count": len(session_data['messages']),
                "created_at": session_data['created_at'],
                "last_activity": session_data['messages'][-1]['timestamp'] if session_data['messages'] else session_data['created_at']
            }

        return jsonify({
            "success": True,
            "sessions": sessions_info,
            "total_sessions": len(SESSIONS),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/sessions/<session_id>/clear', methods=['POST'])
def clear_session(session_id):
    """Clear a specific session."""
    try:
        logger.info(f"Clearing session: {session_id}")

        if session_id in SESSIONS:
            SESSIONS[session_id]['messages'] = []
            SESSIONS[session_id]['history'] = ChatMessageHistory()
            if session_id == 'default_session':
                save_history([])

            logger.info(f"✓ Session {session_id} cleared successfully")
            return jsonify({
                "success": True,
                "message": f"Session {session_id} cleared",
                "timestamp": datetime.now().isoformat()
            })
        else:
            logger.warning(f"Session {session_id} not found")
            return jsonify({
                "success": False,
                "message": f"Session {session_id} not found",
                "timestamp": datetime.now().isoformat()
            }), 404

    except Exception as e:
        logger.error(f"Failed to clear session {session_id}: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/sessions/<session_id>/messages', methods=['GET'])
def get_session_messages(session_id):
    """Get messages for a specific session."""
    try:
        logger.debug(f"Messages requested for session: {session_id}")

        session_data = get_session_data(session_id)
        return jsonify({
            "success": True,
            "session_id": session_id,
            "messages": session_data['messages'],
            "message_count": len(session_data['messages']),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to get messages for session {session_id}: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/api/debug/logs', methods=['GET'])
def get_debug_logs():
    """Get recent debug logs."""
    try:
        log_lines = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                log_lines = f.readlines()[-100:]  # Last 100 lines

        return jsonify({
            "success": True,
            "logs": log_lines,
            "log_count": len(log_lines),
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        logger.error(f"Failed to get debug logs: {e}")
        return jsonify({
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500


# --- Error Handlers ---

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    logger.warning(f"404 error for path: {request.path}")
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "path": request.path,
        "available_endpoints": [
            "/health",
            "/api/health",
            "/ping",
            "/api/chat",
            "/api/sessions",
            "/api/sessions/<session_id>/clear",
            "/api/sessions/<session_id>/messages",
            "/api/debug/logs"
        ],
        "timestamp": datetime.now().isoformat()
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 internal server error: {error}")
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": str(error),
        "timestamp": datetime.now().isoformat()
    }), 500


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle all uncaught exceptions."""
    logger.error(f"Unhandled exception: {e}", exc_info=True)
    return jsonify({
        "success": False,
        "error": str(e),
        "type": type(e).__name__,
        "timestamp": datetime.now().isoformat()
    }), 500


# --- Startup ---
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    IS_PRODUCTION = os.environ.get('RENDER') or os.environ.get('PRODUCTION')
    
    logger.info("=" * 70)
    logger.info("👨‍💻 CODING ASSISTANT API SERVER STARTING")
    logger.info("=" * 70)
    logger.info(f"Environment: {'Production (Render)' if IS_PRODUCTION else 'Development'}")
    logger.info(f"Port: {PORT}")
    logger.info(f"Model: Gemini 2.0 Flash")
    logger.info(f"Temperature: 0.2 (Optimized for coding)")
    logger.info(f"Backend URL: http://0.0.0.0:{PORT}")
    logger.info(f"Health Check: http://0.0.0.0:{PORT}/health")
    logger.info(f"Ping: http://0.0.0.0:{PORT}/ping")
    logger.info(f"Chat Endpoint: http://0.0.0.0:{PORT}/api/chat")
    logger.info(f"Log file: {LOG_FILE}")
    logger.info(f"History file: {HISTORY_FILE}")
    logger.info("=" * 70)

    try:
        # Test model before starting server
        logger.info("Testing Gemini model with Coding Assistant prompt...")
        test_response = conversation.invoke(
            {"question": "Write a simple Python function to reverse a string. Include docstring."},
            config={"configurable": {"session_id": "startup_test"}}
        )
        test_reply = getattr(test_response, "content", str(test_response))
        logger.info(f"✓ Model test successful - Response preview: '{test_reply[:150]}...'")
        logger.info("=" * 70)
        logger.info("✅ All systems operational - Coding Assistant ready!")
        logger.info("=" * 70)

        # Start Flask server
        app.run(
            host='0.0.0.0',
            port=PORT,
            debug=not IS_PRODUCTION,  # Debug mode off in production
            use_reloader=False
        )

    except Exception as e:
        logger.error("=" * 70)
        logger.error(f"✗ CRITICAL ERROR: Failed to start server")
        logger.error(f"Error: {e}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        logger.error("=" * 70)
        raise
