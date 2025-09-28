import os
import sys
import json
import logging
import traceback
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Your existing imports
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

# --- Logging Setup ---
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('chatbot_api.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# --- API Key setup ---
# --- API Key setup ---
try:
    google_key = os.getenv("GOOGLE_API_KEY")  # match the name in Render
    if not google_key:
        raise ValueError("GOOGLE_API_KEY not set in environment")
    os.environ["GOOGLE_API_KEY"] = google_key
    logger.info("API key loaded successfully from environment")
except Exception as e:
    logger.error(f"Failed to load API key: {e}")
    raise


# --- Constants ---
HISTORY_FILE = "chat_history.json"
SESSIONS = {}  # Store session data in memory


# --- Utility Functions ---
def load_history():
    """Load chat history from file."""
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Loaded {len(data)} messages from history file")
                return data
        logger.info("No existing history file found")
        return []
    except Exception as e:
        logger.error(f"Error loading history: {e}")
        return []


def save_history(messages):
    """Save chat history to file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        logger.debug(f"Saved {len(messages)} messages to history file")
    except Exception as e:
        logger.error(f"Error saving history: {e}")


def get_session_data(session_id):
    """Get or create session data."""
    if session_id not in SESSIONS:
        logger.info(f"Creating new session: {session_id}")
        SESSIONS[session_id] = {
            'messages': load_history(),
            'history': ChatMessageHistory(),
            'created_at': datetime.now().isoformat()
        }

        # Load existing messages into ChatMessageHistory
        for msg in SESSIONS[session_id]['messages']:
            if msg["role"] == "user":
                SESSIONS[session_id]['history'].add_user_message(msg["content"])
            else:
                SESSIONS[session_id]['history'].add_ai_message(msg["content"])

        logger.debug(f"Session {session_id} initialized with {len(SESSIONS[session_id]['messages'])} messages")

    return SESSIONS[session_id]


# --- Model Setup (Your exact configuration) ---
try:
    logger.info("Initializing Gemini 2.0 Flash model...")
    model = init_chat_model(
        "gemini-2.0-flash",
        model_provider="google_genai",
        temperature=0.7
    )
    logger.info("Gemini 2.0 Flash model initialized successfully")
    logger.debug(f"Model type: {type(model)}")
    logger.debug(f"Model provider: google_genai")
    logger.debug(f"Temperature: 0.7")
except Exception as e:
    logger.error(f"Failed to initialize Gemini model: {e}")
    logger.error(f"Make sure GOOGLE_API_KEY is set correctly")
    logger.error(f"Traceback: {traceback.format_exc()}")
    raise

# --- Prompt Template (Jack Sparrow style) ---
prompt_template = ChatPromptTemplate.from_template(
    "You are Captain Jack Sparrow. Answer every question with wit and iconic dialogues. Question: {question}"
)
logger.info("Jack Sparrow prompt template created")
logger.debug(f"Prompt template: {prompt_template}")

# Test the model initialization
try:
    logger.info("Testing model with prompt template...")
    test_chain = prompt_template | model
    logger.info("Model and prompt template chain created successfully")
except Exception as e:
    logger.error(f"Failed to create model chain: {e}")
    raise


# --- Memory Setup ---
def get_history_for_session(session_id: str):
    """Return a message history object for a given session."""
    session_data = get_session_data(session_id)
    return session_data['history']


# Create conversation chain (Your exact setup)
try:
    logger.info("Creating RunnableWithMessageHistory conversation chain...")
    conversation = RunnableWithMessageHistory(
        prompt_template | model,  # Your exact chain: prompt_template | model
        get_history_for_session,
        input_messages_key="question",  # Matches your {question} variable
        history_messages_key="history",  # Your history key
    )
    logger.info("Conversation chain with memory created successfully")
    logger.debug("Chain components:")
    logger.debug(f"- Runnable: prompt_template | model")
    logger.debug(f"- History function: get_history_for_session")
    logger.debug(f"- Input key: question")
    logger.debug(f"- History key: history")
except Exception as e:
    logger.error(f"Failed to create conversation chain: {e}")
    logger.error(f"Error details: {traceback.format_exc()}")
    raise

# --- Flask App Setup ---
app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins for development
logger.info("Flask app initialized with CORS enabled")


# --- API Endpoints ---

@app.route('/health', methods=['GET'])
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    try:
        logger.debug("Health check requested")
        return jsonify({
            "status": "healthy",
            "message": "Chatbot API is running",
            "timestamp": datetime.now().isoformat(),
            "active_sessions": len(SESSIONS)
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint."""
    start_time = datetime.now()
    request_id = f"{start_time.timestamp()}"

    try:
        logger.info(f"[{request_id}] Chat request received")

        # Validate request
        if not request.is_json:
            logger.error(f"[{request_id}] Invalid request format - not JSON")
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        logger.debug(f"[{request_id}] Request data: {data}")

        # Extract parameters
        message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default_session')

        if not message:
            logger.error(f"[{request_id}] Empty message provided")
            return jsonify({"error": "Message cannot be empty"}), 400

        logger.info(f"[{request_id}] Processing message for session {session_id}: '{message[:50]}...'")

        # Get session data
        session_data = get_session_data(session_id)

        # Process message with conversation chain
        logger.debug(f"[{request_id}] Invoking conversation chain")
        response = conversation.invoke(
            {"question": message},
            config={"configurable": {"session_id": session_id}}
        )

        # Extract bot reply
        bot_reply = getattr(response, "content", str(response))
        logger.debug(f"[{request_id}] Bot response generated: '{bot_reply[:50]}...'")

        # Update session messages
        session_data['messages'].append({"role": "user", "content": message, "timestamp": start_time.isoformat()})
        session_data['messages'].append(
            {"role": "assistant", "content": bot_reply, "timestamp": datetime.now().isoformat()})

        # Save to file (for persistence)
        save_history(session_data['messages'])

        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        logger.info(f"[{request_id}] Request processed successfully in {processing_time:.2f}s")

        return jsonify({
            "success": True,
            "response": bot_reply,
            "session_id": session_id,
            "message_count": len(session_data['messages']),
            "processing_time": processing_time,
            "request_id": request_id
        })

    except Exception as e:
        processing_time = (datetime.now() - start_time).total_seconds()
        error_details = {
            "error": str(e),
            "type": type(e).__name__,
            "traceback": traceback.format_exc(),
            "processing_time": processing_time,
            "request_id": request_id
        }

        logger.error(f"[{request_id}] Chat request failed: {error_details}")

        return jsonify({
            "success": False,
            "error": str(e),
            "response": f"Sorry, I encountered an error: {str(e)}",
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
                "last_activity": session_data['messages'][-1]['timestamp'] if session_data['messages'] else
                session_data['created_at']
            }

        return jsonify({
            "success": True,
            "sessions": sessions_info,
            "total_sessions": len(SESSIONS)
        })

    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/sessions/<session_id>/clear', methods=['POST'])
def clear_session(session_id):
    """Clear a specific session."""
    try:
        logger.info(f"Clearing session: {session_id}")

        if session_id in SESSIONS:
            SESSIONS[session_id]['messages'] = []
            SESSIONS[session_id]['history'] = ChatMessageHistory()
            save_history([])  # Clear file if default session

            logger.info(f"Session {session_id} cleared successfully")
            return jsonify({
                "success": True,
                "message": f"Session {session_id} cleared"
            })
        else:
            return jsonify({
                "success": False,
                "message": f"Session {session_id} not found"
            }), 404

    except Exception as e:
        logger.error(f"Failed to clear session {session_id}: {e}")
        return jsonify({"error": str(e)}), 500


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
            "message_count": len(session_data['messages'])
        })

    except Exception as e:
        logger.error(f"Failed to get messages for session {session_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/debug/logs', methods=['GET'])
def get_debug_logs():
    """Get recent debug logs."""
    try:
        log_lines = []
        if os.path.exists('chatbot_api.log'):
            with open('chatbot_api.log', 'r', encoding='utf-8') as f:
                log_lines = f.readlines()[-100:]  # Last 100 lines

        return jsonify({
            "success": True,
            "logs": log_lines,
            "log_count": len(log_lines)
        })

    except Exception as e:
        logger.error(f"Failed to get debug logs: {e}")
        return jsonify({"error": str(e)}), 500


# --- Error Handlers ---
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error for path: {request.path}")
    return jsonify({
        "error": "Endpoint not found",
        "path": request.path,
        "available_endpoints": [
            "/health",
            "/api/health",
            "/api/chat",
            "/api/sessions",
            "/api/sessions/<session_id>/clear",
            "/api/sessions/<session_id>/messages",
            "/api/debug/logs"
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    return jsonify({
        "error": "Internal server error",
        "message": str(error)
    }), 500


# --- Startup ---
if __name__ == '__main__':
    logger.info("=" * 50)
    logger.info("🤖 CHATBOT API SERVER STARTING")
    logger.info("=" * 50)
    logger.info(f"Backend URL: http://localhost:5000")
    logger.info(f"Health Check: http://localhost:5000/health")
    logger.info(f"Chat Endpoint: http://localhost:5000/api/chat")
    logger.info(f"Log file: chatbot_api.log")
    logger.info("=" * 50)

    try:
        # Test model before starting server (Your exact test)
        logger.info("Testing Gemini model with Jack Sparrow prompt...")
        test_response = conversation.invoke(
            {"question": "Hello, who are you?"},  # Test your exact prompt format
            config={"configurable": {"session_id": "startup_test"}}
        )
        test_reply = getattr(test_response, "content", str(test_response))
        logger.info(f"Model test successful - Response: '{test_reply[:100]}...'")
        logger.info("✅ Gemini 2.0 Flash + Jack Sparrow prompt working correctly!")

        # Start Flask server
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=True,
            use_reloader=False  # Prevent double startup in debug mode
        )

    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        raise

