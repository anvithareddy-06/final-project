DreamPath AI – Career Roadmap Chatbot 
DreamPath AI is an interactive chatbot platform that helps students and tech learners explore different career paths, generate personalized roadmaps, and track learning goals. Powered by Together.ai API, this chatbot answers user queries step-by-step and allows feedback on responses.

 Live Demo
View it deployed here: https://final-project-u6kf.onrender.com

📁 Project Structure

├── app.py
├── requirements.txt
├── users.json
├── templates/
│ ├── home.html
│ ├── register.html
│ ├── login.html
│ ├── chatbot.html
│ └── career.html
├── static/
│ └── feedback.js
├── .env
└── render.yaml

 Features

Career query chatbot using Together.ai API

User registration & login system

Career selection page to explore roles like Data Scientist, IAS Officer, Lawyer, etc.

Auto-prompt injection into chatbot when career is selected

Feedback buttons (👍 👎) for every AI response

User messages and AI replies formatted into step-by-step roadmaps

Technologies Used :

Python (Flask)

Together.ai API (for generating responses)

HTML/CSS/JS (Bootstrap 5)

Flask-CORS

dotenv (to secure API keys)

Render.com for deployment

 How to Run Locally

Clone the repository:

git clone https://github.com/anvithareddy-06/final-project.git
cd project-repo-name

Create a virtual environment:

python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows

Install dependencies:

pip install -r requirements.txt

Set environment variables in a .env file:

TOGETHER_API_KEY=your_together_api_key
SECRET_KEY=your_secret_key

Run the app:

python app.py

Open your browser at:

https://final-project-u6kf.onrender.com

 Deployment

This app is deployed using Render. Deployment link:
https://final-project-u6kf.onrender.com

You can deploy by:

Creating a GitHub repo with this project

Linking the repo in Render.com

Adding a render.yaml for automatic builds

 Example Queries to Try:

How to become a data scientist?

What is the roadmap to become an IAS officer?

Give me steps to become a software engineer.
