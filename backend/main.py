from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth import auth_bp
from gemini_chat import GeminiChat
import os

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.secret_key = os.urandom(24)
app.register_blueprint(auth_bp)

# Initialize Gemini Chat
gemini_chat = GeminiChat()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session and not session.get('demo_mode'):
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        user_input = request.json.get('message')
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        response = gemini_chat.get_response(user_input)
        return jsonify({'response': response})
    
    return render_template('chat.html', username=session.get('username', 'Demo User'))

@app.route('/demo')
def demo():
    session['demo_mode'] = True
    gemini_chat.start_chat()  # Start fresh session for demo
    return render_template('chat.html', username="Demo User")

if __name__ == '__main__':
    app.run(debug=True)
