import os
import logging
import json
import re
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'debate-gravity-secret-key-change-in-prod')
CORS(app)

# Constants
MAX_MESSAGE_LENGTH = 2000
MIN_MESSAGE_LENGTH = 1
MAX_HISTORY_LENGTH = 10  # Keep last 10 exchanges for context
VALID_MODES = {'logical', 'aggressive', 'devil'}

# ============================================================
# GEMINI AI SETUP
# ============================================================

api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')

if not api_key:
    logger.error("❌ API Key not found! Check your .env file.")
    logger.info("   → Get a new key at: https://aistudio.google.com/app/apikey")
    model = None
else:
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info("✅ Gemini AI Connected!")
    except Exception as e:
        logger.error(f"❌ Configuration Error: {e}")
        model = None

# System Prompts with scoring instruction
SYSTEM_PROMPTS = {
    'logical': """You are Debate Gravity, an AI debate opponent. Your role is to argue the OPPOSITE of the user's position.
Be sharp, academic, logical, and concise. Use facts, statistics, and reasoning.
Remember the conversation history and build upon previous points.""",
    
    'aggressive': """You are Debate Gravity, an AI debate opponent. Your role is to argue the OPPOSITE of the user's position.
Be aggressive, assertive, and forceful. Challenge every assumption. Point out flaws ruthlessly.
Remember the conversation history and escalate your arguments.""",
    
    'devil': """You are Debate Gravity playing Devil's Advocate. Argue the COMPLETE OPPOSITE of whatever the user says.
No matter how absurd or extreme. Be provocative and challenge conventional wisdom.
Remember the conversation history and push boundaries further."""
}

SCORING_PROMPT = """Based on the debate so far, evaluate the USER's argumentation skills.
Score from 0-100 on these criteria and provide brief feedback:
- Logic (0-25): How well-reasoned are their arguments?
- Evidence (0-25): Do they use facts, examples, or data?
- Persuasion (0-25): How compelling is their rhetoric?
- Rebuttal (0-25): How well do they counter your points?

Respond ONLY in this exact JSON format:
{"logic": X, "evidence": X, "persuasion": X, "rebuttal": X, "total": X, "feedback": "Brief 1-2 sentence feedback"}"""

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/stats')
def stats():
    """Health check and stats endpoint"""
    return jsonify({
        "status": "online" if model else "offline",
        "count": 12,
        "recent": ["AI Safety", "Mars Colony"]
    })


@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint with conversation history"""
    
    if not model:
        logger.warning("Chat attempted but model is not available")
        return jsonify({
            'error': 'AI service unavailable. Check API key configuration.'
        }), 503

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON body'}), 400

    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    if len(user_message) > MAX_MESSAGE_LENGTH:
        return jsonify({'error': f'Message exceeds {MAX_MESSAGE_LENGTH} characters'}), 400

    mode = data.get('mode', 'logical')
    if mode not in VALID_MODES:
        mode = 'logical'

    # Get conversation history from request
    history = data.get('history', [])
    if not isinstance(history, list):
        history = []
    
    # Limit history length
    history = history[-MAX_HISTORY_LENGTH:]

    logger.info(f"Chat request: mode={mode}, history_len={len(history)}")

    try:
        # Build prompt with conversation history
        system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS['logical'])
        
        # Format history
        history_text = ""
        for exchange in history:
            if isinstance(exchange, dict):
                history_text += f"User: {exchange.get('user', '')}\n"
                history_text += f"AI: {exchange.get('ai', '')}\n\n"
        
        full_prompt = f"""{system_prompt}

CONVERSATION HISTORY:
{history_text if history_text else "(This is the start of the debate)"}

CURRENT MESSAGE:
User: {user_message}
AI:"""
        
        response = model.generate_content(full_prompt)
        
        if not response.text:
            return jsonify({'error': 'AI generated empty response'}), 500
        
        logger.info(f"AI response generated: {len(response.text)} chars")
        return jsonify({
            'response': response.text,
            'historyLength': len(history) + 1
        })

    except Exception as e:
        logger.error(f"Generation error: {str(e)}")
        error_msg = str(e)
        
        if '429' in error_msg or 'quota' in error_msg.lower():
            return jsonify({
                'error': 'API quota exceeded. Please try again later or get a new API key.'
            }), 429
        elif '401' in error_msg or 'key' in error_msg.lower():
            return jsonify({
                'error': 'Invalid API key. Please check your configuration.'
            }), 401
        else:
            return jsonify({
                'error': 'Failed to generate response. Please try again.'
            }), 500


@app.route('/score', methods=['POST'])
def score_debate():
    """Score the user's debate performance"""
    
    if not model:
        return jsonify({'error': 'AI service unavailable'}), 503

    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json(silent=True)
    history = data.get('history', [])
    
    if not history or len(history) < 2:
        return jsonify({
            'error': 'Need at least 2 exchanges to score',
            'score': None
        }), 400

    try:
        # Format history for scoring
        history_text = ""
        for exchange in history:
            if isinstance(exchange, dict):
                history_text += f"User: {exchange.get('user', '')}\n"
                history_text += f"AI: {exchange.get('ai', '')}\n\n"
        
        scoring_request = f"""DEBATE TRANSCRIPT:
{history_text}

{SCORING_PROMPT}"""
        
        response = model.generate_content(scoring_request)
        
        if not response.text:
            return jsonify({'error': 'Failed to generate score'}), 500
        
        # Parse JSON from response
        try:
            # Extract JSON from response (handle markdown code blocks)
            json_match = re.search(r'\{[^}]+\}', response.text)
            if json_match:
                score_data = json.loads(json_match.group())
            else:
                score_data = json.loads(response.text)
            
            # Validate required fields
            required = ['logic', 'evidence', 'persuasion', 'rebuttal', 'total', 'feedback']
            if all(k in score_data for k in required):
                logger.info(f"Debate scored: {score_data['total']}/100")
                return jsonify({'score': score_data})
            else:
                raise ValueError("Missing required fields")
                
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Score parse error: {e}, raw: {response.text[:100]}")
            # Fallback scoring
            return jsonify({
                'score': {
                    'logic': 15,
                    'evidence': 15,
                    'persuasion': 15,
                    'rebuttal': 15,
                    'total': 60,
                    'feedback': 'Good effort! Keep building stronger arguments with more evidence.'
                }
            })

    except Exception as e:
        logger.error(f"Scoring error: {str(e)}")
        return jsonify({'error': 'Failed to score debate'}), 500


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def server_error(e):
    logger.error(f"Server error: {e}")
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    app.run(debug=True, port=5000)