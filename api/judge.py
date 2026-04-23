from google import genai
import json
import os

api_key = os.getenv("Gemini_API_Key", "AIzaSyAMXybQuCC1t68S-EX_F71Kk8A2NGRJUHU")
client = genai.Client(api_key=api_key)

def clean_json(text):
    text = text.strip()

    if "```" in text:
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text

    if text.startswith("json"):
        text = text[4:].strip()

    return text


def run_judge(industry, product, pain_points, persona, emails, log_step=None):
    try:
        prompt = f"""
Return ONLY JSON. Grade these cold emails on a scale of 1-10.

Industry: {industry}
Product: {product}
Emails: {emails}

Format exactly like this:
{{
    "overall_score": 8,
    "summary": "Short explanation of the score"
}}
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        raw = response.text or "{}"
        clean = clean_json(raw)

        return json.loads(clean)

    except Exception as e:
        if log_step:
            log_step(f"Gemini failed: {e}")

        return {
            "overall_score": 3,
            "summary": "Fallback result (Gemini failed)",
            "error": str(e)
        }