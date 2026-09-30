import json
from pathlib import Path
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.layout_builder import build_comic_layout
from app.exporters import save_pdf

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class PromptRequest(BaseModel):
    story_prompt: str
    character_name: str
    setting: str
    tone: str
    art_style: str

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
):
    try:
        outline = generate_outline(story_prompt, character_name, setting, tone, art_style)
        story = generate_story(outline, character_name, tone)
        panels = []
        for panel in outline:
            image_path = generate_image(panel["image_prompt"], panel["panel_number"], art_style)
            panel_story = story[panel["panel_number"] - 1] if panel["panel_number"] - 1 < len(story) else {}
            panels.append({
                **panel,
                "image_path": image_path,
                "scene_description": panel_story.get("scene_description", panel.get("scene_description", "")),
                "caption": panel_story.get("caption", ""),
                "narration": panel_story.get("narration", ""),
            })
        layout = build_comic_layout(panels)
        pdf_path = save_pdf(layout)
        return templates.TemplateResponse(
            "comic_preview.html",
            {"request": request, "layout": layout, "pdf_path": pdf_path}
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": str(exc)}
        )

@router.post("/generate-comic/json")
async def generate_json(payload: PromptRequest):
    try:
        outline = generate_outline(payload.story_prompt, payload.character_name, payload.setting, payload.tone, payload.art_style)
        story = generate_story(outline, payload.character_name, payload.tone)
        panels = []
        for panel in outline:
            image_path = generate_image(panel["image_prompt"], panel["panel_number"], payload.art_style)
            panel_story = story[panel["panel_number"] - 1] if panel["panel_number"] - 1 < len(story) else {}
            panels.append({
                **panel,
                "image_path": image_path,
                "scene_description": panel_story.get("scene_description", panel.get("scene_description", "")),
                "caption": panel_story.get("caption", ""),
                "narration": panel_story.get("narration", ""),
            })
        layout = build_comic_layout(panels)
        pdf_path = save_pdf(layout)
        return JSONResponse({"layout": layout, "pdf_path": pdf_path})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

@router.get("/test-image")
async def test_image(prompt: str = "A brave fox in an enchanted forest, comic book style"):
    path = generate_image(prompt, 1, "comic book")
    return {"image_path": path}

@router.get("/export-success", response_class=HTMLResponse)
async def export_success(request: Request):
    return templates.TemplateResponse("export_success.html", {"request": request})
