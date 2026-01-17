from datetime import datetime
from pathlib import Path

from docx import Document
from flask import Flask, render_template, request, send_file

from storage import engagement_artifacts

app = Flask(__name__)
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)


@app.route("/")
def form() -> str:
    return render_template("form.html")


@app.route("/generate", methods=["POST"])
def generate_document():
    form_data = request.form
    client_name = form_data.get("client_name", "").strip() or "[CLIENT_NAME]"
    matter = form_data.get("matter", "").strip() or "[MATTER]"
    retainer_amount = form_data.get("retainer_amount", "").strip() or "[RETAINER_AMOUNT]"

    document = Document()
    document.add_heading("Document Placeholder", level=1)
    document.add_paragraph("This document is a placeholder draft with supplied values.")
    document.add_paragraph(f"Client Name: {client_name}")
    document.add_paragraph(f"Matter: {matter}")
    document.add_paragraph(f"Retainer Amount: {retainer_amount}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"document_{timestamp}.docx"
    file_path = OUTPUT_DIR / filename
    document.save(file_path)

    return send_file(file_path, as_attachment=True, download_name=filename)


def get_engagement_artifacts(engagement_id: str) -> dict:
    return engagement_artifacts(engagement_id, version=1)


if __name__ == "__main__":
    app.run(debug=True)
