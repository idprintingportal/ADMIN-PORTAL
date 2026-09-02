from flask import Flask, jsonify, request, send_file
import base64
import io
import fitz
from PIL import Image, ImageChops

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
    """Detect common ID layouts: side-by-side or front-above-back.
    Explanatory labels beside sample cards are ignored for stacked layouts.
    """
    image = image.convert("RGB")
    width, height = image.size
    content = trim_content(image)
    ratio = content.width / max(1, content.height)
    if ratio <= 2.2:
        # e-Shram/MahaSarathi/Aadhaar samples are commonly two cards stacked
        # vertically on an A4 page. Keep the left card column and split near
        # the widest whitespace between the two cards.
        if content.height > content.width * 1.18:
            card_area = content.crop((0, 0, max(1, int(content.width * 0.70)), content.height))
            row_scores = []
            pix = card_area.convert("L")
            for y in range(card_area.height):
                dark = sum(1 for x in range(card_area.width) if pix.getpixel((x, y)) < 245)
                row_scores.append(dark)
            middle = card_area.height // 2
            search = range(max(1, middle - card_area.height // 5), min(card_area.height - 1, middle + card_area.height // 5))
            cut = min(search, key=lambda y: row_scores[y])
            if row_scores[cut] < card_area.width * 0.08:
                front = trim_content(card_area.crop((0, 0, card_area.width, cut)))
                back = trim_content(card_area.crop((0, cut, card_area.width, card_area.height)))
                return front, back, "stacked"
        blank = Image.new("RGB", content.size, "white")
        return content, blank, "single"
    cut = width // 2
    front = trim_content(image.crop((0, 0, cut, height)))
    back = trim_content(image.crop((cut, 0, width, height)))
    return front, back, "side-by-side"


def template_boxes(filename: str):
    """Return verified PDF-point boxes for known sample layouts.
    Coordinates are converted to pixels after rendering; they are not raw
    1200-DPI pixel values.
    """
    name = (filename or "").lower().replace("_", " ").replace("-", " ")
    if "e shram" in name or "eshram" in name:
        return [(35, 45, 560, 340)]
    if "maandhan" in name or "mandhan" in name:
        return [(40, 50, 555, 350)]
    if "aadhaar" in name or "eaadhaar" in name or "aadhar" in name:
        return [(35, 715, 295, 970), (510, 715, 770, 970)]
    if "pan" in name or "signed" in name:
        return [(50, 380, 545, 625), (50, 680, 545, 925)]
    return None


def crop_pdf_box(image: Image.Image, box, page_rect):
    """Crop a PDF-point rectangle from a rendered image."""
    sx = image.width / max(1, float(page_rect.width))
    sy = image.height / max(1, float(page_rect.height))
    x0, y0, x1, y1 = box
    px = (round(x0 * sx), round(y0 * sy), round(x1 * sx), round(y1 * sy))
    px = (max(0, px[0]), max(0, px[1]), min(image.width, px[2]), min(image.height, px[3]))
    if px[2] <= px[0] or px[3] <= px[1]:
        raise ValueError("Configured card box is outside this PDF page.")
    return image.crop(px)


def png_data(image: Image.Image) -> str:
    out = io.BytesIO()
    # Low compression level is materially faster for temporary API previews;
    # the source pixels remain lossless and the final PVC export is handled by
    # the browser canvas.
    image.save(out, "PNG", optimize=False, compress_level=1)
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
        # Keep the source detail for the crop/export pipeline. The worker must
        # not reduce the downloaded card quality, so the normal path remains
        # 1200 DPI; 600 DPI is only an emergency fallback for large pages.
        try:
            pixmap = page.get_pixmap(dpi=1200, alpha=False)
        except Exception:
            pixmap = page.get_pixmap(dpi=600, alpha=False)
        image = Image.open(io.BytesIO(pixmap.tobytes("png"))).convert("RGB")
        boxes = template_boxes(uploaded.filename)
        if boxes:
            front = trim_content(crop_pdf_box(image, boxes[0], page.rect), padding=8)
            if len(boxes) > 1:
                back = trim_content(crop_pdf_box(image, boxes[1], page.rect), padding=8)
                layout = "template-front-back"
            else:
                back = Image.new("RGB", front.size, "white")
                layout = "template-single"
        else:
            front, back, layout = split_cards(image)
        return jsonify({"success": True, "layout": layout,
                        "page": "data:image/png;base64," + png_data(image),
                        "front": "data:image/png;base64," + png_data(front),
                        "back": "data:image/png;base64," + png_data(back)})
    except Exception as exc:
        return jsonify(error=str(exc)[:240]), 422


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8766, debug=False)
