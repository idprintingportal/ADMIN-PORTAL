from flask import Flask, jsonify, request, send_file
import base64
import io
import fitz
from PIL import Image, ImageChops
import os
import subprocess
import tempfile
from flask import send_file
app = Flask(__name__)

@app.after_request
def allow_local_portal(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


def trim_content(image: Image.Image, padding: int = 18) -> Image.Image:
    """Remove page-white margins while preserving the complete visible card."""
    rgb = image.convert("RGB")
    bg = Image.new("RGB", rgb.size, (255, 255, 255))
    diff = ImageChops.difference(rgb, bg)
    diff = diff.point(lambda value: 255 if value > 10 else 0)
    box = diff.getbbox()
    if not box:
        return rgb
    left, top, right, bottom = box
    left = max(0, left - padding)
    top = max(0, top - padding)
    right = min(rgb.width, right + padding)
    bottom = min(rgb.height, bottom + padding)
    return rgb.crop((left, top, right, bottom))


def split_cards(image: Image.Image):
    """Split only a clearly side-by-side page; otherwise keep one whole card."""
    image = image.convert("RGB")
    width, height = image.size
    content = trim_content(image)
    ratio = content.width / max(1, content.height)
    if ratio <= 2.2:
        blank = Image.new("RGB", content.size, "white")
        return content, blank, "single"
    cut = width // 2
    front = trim_content(image.crop((0, 0, cut, height)))
    back = trim_content(image.crop((cut, 0, width, height)))
    return front, back, "side-by-side"


def png_data(image: Image.Image) -> str:
    out = io.BytesIO()
    image.save(out, "PNG", optimize=True)
    return base64.b64encode(out.getvalue()).decode("ascii")


@app.post("/crop-card")
def crop_card():
    uploaded = request.files.get("file")
    if not uploaded:
        return jsonify(error="PDF file is required."), 400
    password = request.form.get("password", "")
    try:
        document = fitz.open(stream=uploaded.read(), filetype="pdf")
        if document.needs_pass and not document.authenticate(password):
            return jsonify(error="PDF password required or incorrect."), 401
        if document.page_count == 0:
            return jsonify(error="PDF has no pages."), 400
        page = document.load_page(0)
        # Render at print quality. A source PDF cannot gain new detail, but this
        # preserves the maximum available detail for the downstream PVC export.
        try:
            pixmap = page.get_pixmap(dpi=1200, alpha=False)
        except Exception:
            pixmap = page.get_pixmap(dpi=600, alpha=False)
        image = Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGB")
        front, back, layout = split_cards(image)
        return jsonify({"success": True, "layout": layout,
                        "page": "data:image/png;base64," + png_data(image),
                        "front": "data:image/png;base64," + png_data(front),
                        "back": "data:image/png;base64," + png_data(back)})
    except Exception as exc:
        return jsonify(error=str(exc)[:240]), 422

@app.route("/convert-office", methods=["POST"])
def convert_office():
    if "file" not in request.files:
        return {"success": False, "error": "File missing"}, 400

    uploaded_file = request.files["file"]
    output_format = request.form.get("format", "docx").lower()

    allowed_formats = {
        "docx": "docx",
        "xlsx": "xlsx",
        "pptx": "pptx"
    }

    if output_format not in allowed_formats:
        return {"success": False, "error": "Invalid output format"}, 400

    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, "input.pdf")
        uploaded_file.save(input_path)

        command = [
            "libreoffice",
            "--headless",
            "--convert-to",
            allowed_formats[output_format],
            "--outdir",
            temp_dir,
            input_path
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120
        )

        output_path = os.path.join(temp_dir, f"input.{output_format}")

        if result.returncode != 0 or not os.path.exists(output_path):
            return {
                "success": False,
                "error": result.stderr or "Conversion failed"
            }, 500

        return send_file(
            output_path,
            as_attachment=True,
            download_name=f"converted.{output_format}"
        )
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8766, debug=False)
