from pathlib import Path
from datetime import datetime
from fpdf import FPDF

EXPORT_DIR = Path("static/exports")
EXPORT_DIR.mkdir(parents=True, exist_ok=True)

def save_pdf(layout):
    filename = EXPORT_DIR / f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in layout:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.multi_cell(0, 12, f"Panel {panel['panel_number']}: {panel['title']}")
        image_path = panel["image_path"].lstrip("/")
        if Path(image_path).exists():
            pdf.image(image_path, x=15, y=40, w=180)
            pdf.ln(125)
        pdf.set_font("Helvetica", "", 11)
        for label, value in [
            ("Scene", panel["scene_description"]),
            ("Caption", panel["caption"]),
            ("Narration", panel["narration"]),
        ]:
            pdf.set_font("Helvetica", "B", 11)
            pdf.write(6, f"{label}: ")
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 6, value or "")
            pdf.ln(2)

    pdf.output(str(filename))
    return "/" + filename.as_posix()
