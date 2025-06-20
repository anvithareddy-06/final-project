faq_answers = {
    "html": "HTML stands for HyperText Markup Language. It's used to structure web pages.",
    "css": "CSS stands for Cascading Style Sheets. It controls the appearance of web elements.",
    "javascript": "JavaScript is a programming language used for dynamic content on websites.",
    "learn html css": "Start with HTML basics, then learn CSS layout, flexbox, and responsive design.",
    "frontend": "Frontend development involves HTML, CSS, JS. Use tools like React or Vue.",
    "backend": "Backend involves server-side programming like Node.js, Python, or Java.",
}

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
import json
import requests
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv("SECRET_KEY", "dev_default_key")

# API config
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
print("Loaded API Key:", TOGETHER_API_KEY) 
TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"

# Ensure user data file exists
users_file = 'users.json'
if not os.path.exists(users_file):
    with open(users_file, 'w') as f:
        json.dump({}, f)
# Auto-fix any improperly formatted users
with open(users_file, 'r+') as f:
    try:
        data = json.load(f)
        updated = False
        for email in data:
            if isinstance(data[email], str):
                # convert to proper format
                data[email] = {
                    "name": "Unknown",
                    "password": data[email]
                }
                updated = True
        if updated:
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()
    except json.JSONDecodeError:
        json.dump({}, f)


@app.route('/')
def home():
    return render_template('home.html')
@app.route('/career')
def career_page():
    return render_template('career.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if not fullname or not email or not password or not confirm_password:
            return "All fields are required", 400

        if password != confirm_password:
            return "Passwords do not match. <a href='/register'>Try again</a>"

        with open(users_file, 'r') as f:
            users = json.load(f)

        users[email] = {
            "name": fullname, "password": password
        }

        with open(users_file, 'w') as f:
            json.dump(users, f)

        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return "Please enter both email and password"

        with open(users_file, 'r') as f:
            users_data = json.load(f)

        if email in users_data and users_data[email]["password"] == password:
            session['user'] = email
            next_page = session.pop('redirect_after_login', None)
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('chatbot_page'))

        else:
            return "Invalid credentials. <a href='/login'>Try again</a>"

    return render_template('login.html')

def get_faq_response(message):
    message_lower = message.lower()
    for keyword, answer in faq_answers.items():
        if keyword in message_lower:
            return answer
    return None

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_page():
    if 'user' not in session:
        session['redirect_after_login'] = request.full_path
        return redirect(url_for('login'))

   
    if request.method == 'POST':
        data = request.get_json()
        message = data.get('message')
        print("Received message:", message)

        # ✅ Try keyword-based match first
        faq_reply = get_faq_response(message)
        if faq_reply:
            return jsonify({"reply": faq_reply})

        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "meta-llama/Llama-3-8b-chat-hf",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant. Always reply in roadmap format using step-by-step guidance or bullet points."},
                {"role": "user", "content": message}
            ],
            "max_tokens": 1024,
            "temperature": 0.7
        }

        try:
            print("Sending request to Together API...")
            response = requests.post(TOGETHER_URL, headers=headers, json=payload)
            print("API response status:", response.status_code)
            if response.status_code == 200:
                response_json = response.json()
                print("API JSON:", response_json)
                if "choices" in response_json and len(response_json["choices"]) > 0:
                    reply = response_json["choices"][0]["message"]["content"]
                else:
                    reply = "Sorry, no valid reply from the API."
            else:
                print("Full error:", response.text)
                reply = f"API Error {response.status_code}: {response.text}"
        except Exception as e:
            print("Error occurred:", str(e))
            reply = f"Error: {str(e)}"

        return jsonify({"reply": reply})

    return render_template('chatbot.html', user=session['user'])

# ✅ Helper to store unanswered questions
def store_unanswered(question):
    import os
    import json

    file_path = 'unanswered.json'
    question = question.strip()

    if not question:
        return

    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            data = []

        if question not in data:
            data.append(question)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
    except Exception as e:
        print("Failed to store unanswered question:", e)


@app.route('/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    feedback_entry = {
        "message": data.get("message"),
        "feedback": data.get("feedback")  # 'up' or 'down'
    }

    feedback_file = 'feedback.json'
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            all_feedback = json.load(f)
    else:
        all_feedback = []

    all_feedback.append(feedback_entry)

    with open(feedback_file, 'w') as f:
        json.dump(all_feedback, f, indent=2)

    return jsonify({"status": "success"})


@app.route('/unanswered')
def show_unanswered():
    import os
    import json

    file_path = 'unanswered.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return "<h2>Unanswered Questions</h2><ul>" + "".join(f"<li>{q}</li>" for q in data) + "</ul>"
    else:
        return "No unanswered questions found."

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

