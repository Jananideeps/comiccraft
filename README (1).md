# ComicCraft - AI Comic Story Creator

ComicCraft is a FastAPI web application that turns a user prompt into a five-panel comic workflow. It follows the project specification supplied for the assignment: Gemini-based outline/story generation, Stable Diffusion image generation, Jinja2 frontend templates, and FPDF PDF export.

## Features
- Story prompt, character, setting, tone, and art-style inputs
- Five-panel structured comic outline
- Story narration and dialogue generation
- Image generation module with a runnable Pillow demo fallback
- Comic preview in the browser
- PDF export
- JSON API endpoint
- FastAPI Swagger docs at `/docs`

## Project Structure
```text
ComicCraft/
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── gemini_flash.py
│   ├── gemini_pro.py
│   ├── image_generator.py
│   ├── layout_builder.py
│   └── exporters.py
├── templates/
├── static/
│   ├── panels/
│   └── exports/
├── requirements.txt
├── .env.example
└── README.md
```

## Run locally
```bash
python -m venv env
# Windows
env\Scripts\activate
# macOS/Linux
source env/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# or: cp .env.example .env
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000` and use the form.

## Gemini
Set `GEMINI_API_KEY` in `.env`. The code uses Gemini for structured outline/story generation when configured. If the API call is unavailable, the project uses a local demo fallback so the application remains testable.

## Stable Diffusion
The default mode creates placeholder panel images with Pillow, avoiding a large model download. To attempt local Diffusers generation, set:
```text
ENABLE_DIFFUSION=1
```
and ensure your machine has the required model dependencies/GPU resources.

## API
`POST /generate-comic/json`

Example:
```json
{
  "story_prompt": "A brave fox exploring an enchanted forest",
  "character_name": "Luna",
  "setting": "Forest",
  "tone": "Dramatic",
  "art_style": "Anime"
}
```

The project is intended as a student-friendly implementation of the supplied ComicCraft specification and can be extended with user accounts, comic libraries, and multi-page story arcs.
