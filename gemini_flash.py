import json
import os

def generate_outline(story_prompt, character_name, setting, tone, art_style):
    """Generate a structured five-panel outline with Gemini when configured.
    Falls back to a local demo outline so the project can run without API keys.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""Create exactly 5 comic panels as JSON.
Story: {story_prompt}
Character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}
Return only a JSON array. Each object must contain:
panel_number, title, scene_description, image_prompt."""
            response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
            text = response.text.strip().replace("```json", "").replace("```", "")
            return json.loads(text)
        except Exception:
            pass

    return [
        {"panel_number": 1, "title": "The Beginning", "scene_description": f"{character_name} begins the adventure in {setting}.", "image_prompt": f"{character_name} starting an adventure in {setting}, {art_style}"},
        {"panel_number": 2, "title": "A Strange Discovery", "scene_description": "Something unexpected appears and changes the direction of the journey.", "image_prompt": f"{character_name} discovering something mysterious in {setting}, {art_style}"},
        {"panel_number": 3, "title": "The Challenge", "scene_description": f"{character_name} faces a challenge with a {tone} atmosphere.", "image_prompt": f"{character_name} facing a dramatic challenge in {setting}, {art_style}"},
        {"panel_number": 4, "title": "The Turning Point", "scene_description": "A clever idea helps the hero overcome the main obstacle.", "image_prompt": f"{character_name} having a heroic breakthrough in {setting}, {art_style}"},
        {"panel_number": 5, "title": "A New Beginning", "scene_description": "The adventure ends with a hopeful new beginning.", "image_prompt": f"{character_name} celebrating after the adventure in {setting}, {art_style}"},
    ]
