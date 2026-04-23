from google import genai
import os
import json

api_key = os.getenv("Gemini_API_Key") or "dummy_key"
client = genai.Client(api_key=api_key)

def clean_json(text):
    text = text.strip()
    if "```" in text:
        parts = text.split("```")
        text = parts[1] if len(parts) > 1 else text
    if text.startswith("json"):
        text = text[4:].strip()
    return text

def run_researcher(industry: str, product: str, log_step=None) -> str:
    if log_step:
        log_step("[Researcher] Running Gemini AI...")
    
    prompt = f"Identify 3 key pain points for a business in the {industry} industry that would be solved by using this product: {product}. Keep it brief, actionable, and format as a numbered list."
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        if log_step:
            log_step(f"Gemini failed: {e}")
        return "1. General inefficiency\n2. Low productivity\n3. Growth challenges"

def run_persona_definer(industry, product, pain_points, log_step=None):
    if log_step:
        log_step("[Persona] Running Gemini AI...")
        
    prompt = f"Based on the {industry} industry and the product {product}, and these pain points: {pain_points}, define a target persona. Include Job Role, Responsibilities, Pain Points, and Goal. Keep it brief."
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Target Persona: Manager in {industry}"

def run_email_writer(industry, product, pain_points, persona, log_step=None):
    if log_step:
        log_step("[Email] Generating sequence with Gemini...")
        
    prompt = f"""
Write a 3-step cold email sequence (JSON format only) based on:
Industry: {industry}
Product: {product}
Pain Points: {pain_points}
Persona: {persona}

Format exactly like this JSON:
{{
    "email_1": {{"subject": "...", "body": "...", "cta": "..."}},
    "email_2": {{"subject": "...", "body": "...", "cta": "..."}},
    "email_3": {{"subject": "...", "body": "...", "cta": "..."}}
}}
"""
    try:
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
            "email_1": {"subject": "Quick idea", "body": f"Gemini API Error: {str(e)}", "cta": "Interested?"},
            "email_2": {"subject": "Following up", "body": "Just following up on my previous email.", "cta": "Thoughts?"},
            "email_3": {"subject": "Final check", "body": "Is this a priority right now?", "cta": "Let me know"}
        }