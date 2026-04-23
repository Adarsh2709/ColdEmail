from flask import Flask, request, jsonify
from flask_cors import CORS
from api.agents import run_researcher, run_persona_definer, run_email_writer
from api.judge import run_judge

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Home route removed to prevent static file conflicts

# Main API route
@app.route("/api/generate", methods=["POST"])
def generate():
    data = request.json or {}

    industry = data.get("industry")
    product = data.get("product")

    pain = run_researcher(industry, product)
    persona = run_persona_definer(industry, product, pain)
    email = run_email_writer(industry, product, pain, persona)
    result = run_judge(industry, product, pain, persona, email)

    return jsonify({
        "pain": pain,
        "persona": persona,
        "email": email,
        "judge": result
    })

# 🔥 REQUIRED for Vercel
def handler(request):
    return app(request.environ, lambda *args: None)