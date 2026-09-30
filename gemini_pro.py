import json
import os

def generate_story(outline, character_name, tone):
    """Expand panels into narration/dialogue. Uses Gemini when a key is available."""
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""Expand this 5-panel comic outline into JSON.
Character: {character_name}
Tone: {tone}
Outline: {json.dumps(outline)}
Return only a JSON array of 5 objects with:
scene_description, caption, narration."""
            response = client.models.generate_content(model="gemini-2.0-pro", contents=prompt)
            text = response.text.strip().replace("```json", "").replace("```", "")
            return json.loads(text)
        except Exception:
            pass

    return [
        {"scene_description": p["scene_description"], "caption": "A new adventure begins.", "narration": f"{character_name}: I wonder what comes next!"}
        for p in outline
    ]
