def build_comic_layout(panels):
    return [
        {
            "panel_number": p["panel_number"],
            "title": p["title"],
            "image_path": p["image_path"],
            "scene_description": p.get("scene_description", ""),
            "caption": p.get("caption", ""),
            "narration": p.get("narration", ""),
            "image_prompt": p.get("image_prompt", ""),
        }
        for p in panels
    ]
