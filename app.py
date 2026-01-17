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

    client_name = form_data.get("client_name", "").strip()
    client_type = form_data.get("client_type", "").strip()
    matter_type = form_data.get("matter_type", "").strip()
    payment_method = form_data.get("payment_method", "").strip()
    matter_description = form_data.get("matter_description", "").strip()
    instructing_officer_name = form_data.get("instructing_officer_name", "").strip()
    retainer_amount = form_data.get("retainer_amount", "").strip()

    if not client_name:
        return "Client name is required.", 400
    if not client_type:
        return "Client type is required.", 400
    if not matter_type:
        return "Matter type is required.", 400
    if not payment_method:
        return "Payment method is required.", 400
    if not matter_description:
        return "Matter description is required.", 400

    if client_type == "Corporation" and not instructing_officer_name:
        return "Instructing officer name is required for corporations.", 400
    if matter_type == "Hourly Strategy" and not retainer_amount:
        return "Retainer amount is required for Hourly Strategy matters.", 400

    document = Document()
    document.add_paragraph(f"Client name: {client_name}")
    document.add_paragraph(f"Client type: {client_type}")
    document.add_paragraph(
        f"Instructing officer: {instructing_officer_name or 'N/A'}"
    )
    document.add_paragraph(f"Matter type: {matter_type}")
    document.add_paragraph(f"Retainer amount: {retainer_amount or 'N/A'}")
    document.add_paragraph(f"Payment method: {payment_method}")
    document.add_paragraph(f"Matter description: {matter_description}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"document_{timestamp}.docx"
    file_path = OUTPUT_DIR / filename
    document.save(file_path)

    return send_file(file_path, as_attachment=True, download_name=filename)


def get_engagement_artifacts(engagement_id: str) -> dict:
    return engagement_artifacts(engagement_id, version=1)


if __name__ == "__main__":
    app.run(debug=True)
