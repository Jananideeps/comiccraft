from pathlib import Path
import os
import re

PANELS_DIR = Path("static/panels")
PANELS_DIR.mkdir(parents=True, exist_ok=True)

def generate_image(prompt, panel_number, art_style="comic book"):
    """Generate an image with Diffusers if enabled; otherwise create a placeholder.
    Set ENABLE_DIFFUSION=1 to use a local Stable Diffusion pipeline.
    """
    output = PANELS_DIR / f"panel_{panel_number}.png"

    if os.getenv("ENABLE_DIFFUSION") == "1":
        try:
            from diffusers import StableDiffusionPipeline
            import torch
            model_id = os.getenv("SD_MODEL", "runwayml/stable-diffusion-v1-5")
            pipe = StableDiffusionPipeline.from_pretrained(model_id)
            if torch.cuda.is_available():
                pipe = pipe.to("cuda")
            image = pipe(f"{prompt}, {art_style}").images[0]
            image.save(output)
            return "/" + output.as_posix()
        except Exception:
            pass

    # Pillow fallback: keeps the demo runnable without a GPU/model download.
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGB", (1200, 750), "white")
    draw = ImageDraw.Draw(img)
    title = f"COMICCRAFT • PANEL {panel_number}"
    draw.rectangle((25, 25, 1175, 725), outline="black", width=8)
    draw.text((60, 65), title, fill="black")
    lines = [prompt[i:i+65] for i in range(0, len(prompt), 65)]
    y = 260
    for line in lines[:6]:
        draw.text((70, y), line, fill="black")
        y += 55
    draw.text((70, 620), "Demo placeholder — enable Stable Diffusion for AI artwork.", fill="black")
    img.save(output)
    return "/" + output.as_posix()
