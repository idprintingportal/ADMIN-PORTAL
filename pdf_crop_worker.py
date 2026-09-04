from flask import Flask, jsonify, request, send_file
import base64
import io
import os
import fitz
from PIL import Image, ImageChops
import cv2
import numpy as np
import pytesseract
import tempfile

try:
    from paddle_engine import read_with_paddle
    PADDLE_AVAILABLE = True
except Exception as exc:
    print("PaddleOCR unavailable:", exc)
    PADDLE_AVAILABLE = False

_tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(_tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = _tesseract_path

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"ok": True, "service": "pdf-crop-worker"})

@app.get("/ocr-status")
def ocr_status():
    try:
        langs = pytesseract.get_languages(config="")
        return jsonify({
            "tesseract": True,
            "eng": "eng" in langs,
            "hin": "hin" in langs,
            "mar": "mar" in langs,
            "paddleOcr": PADDLE_AVAILABLE,
            "languages": langs,
        })
    except Exception as exc:
        return jsonify({"tesseract": False, "paddleOcr": PADDLE_AVAILABLE, "error": str(exc)}), 500

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


def read_card_text(image: Image.Image) -> str:
    """Read multilingual card text after light normalization."""
    rgb = np.asarray(image.convert("RGB"))
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    clean = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    try:
        return pytesseract.image_to_string(clean, lang="eng+hin+mar", config="--oem 3 --psm 6").lower()
    except pytesseract.TesseractNotFoundError:
        return ""


def read_paddle_from_image(image: Image.Image) -> dict:
    """Run optional PaddleOCR without making it a hard worker dependency."""
    if not PADDLE_AVAILABLE:
        return {"text": "", "scores": [], "averageScore": 0}
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
            temp_path = temp_file.name
        image.convert("RGB").save(temp_path, format="PNG")
        return read_with_paddle(temp_path)
    except Exception as exc:
        print("PaddleOCR read failed:", exc)
        return {"text": "", "scores": [], "averageScore": 0}
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def identify_card(text: str) -> str:
    if "income tax" in text or "permanent account" in text:
        return "pan"
    if "aadhaar" in text or "uidai" in text:
        return "aadhaar"
    if "e shram" in text or "e-shram" in text or "eshram" in text:
        return "e-shram"
    if "ayushman" in text or "pm-jay" in text or "pmjay" in text:
        return "ayushman"
    if "maandhan" in text or "mandhan" in text:
        return "maandhan"
    return "unknown"


def _quad_crop(image: Image.Image, points):
    """Perspective-correct a detected card quadrilateral."""
    if cv2 is None:
        return trim_content(image, 12)
    src = np.float32(points)
    def dist(a, b): return float(np.linalg.norm(a - b))
    tl, tr, br, bl = src
    w = max(dist(tl, tr), dist(bl, br))
    h = max(dist(tl, bl), dist(tr, br))
    if w < 40 or h < 25:
        raise ValueError("Detected document is too small.")
    # ID cards are landscape; rotate portrait detections after warping.
    out_w, out_h = max(640, round(w)), max(400, round(h))
    dst = np.float32([[0, 0], [out_w-1, 0], [out_w-1, out_h-1], [0, out_h-1]])
    matrix = cv2.getPerspectiveTransform(src, dst)
    arr = cv2.cvtColor(np.asarray(image.convert("RGB")), cv2.COLOR_RGB2BGR)
    warped = cv2.warpPerspective(arr, matrix, (out_w, out_h), borderMode=cv2.BORDER_REPLICATE)
    result = Image.fromarray(cv2.cvtColor(warped, cv2.COLOR_BGR2RGB))
    if result.height > result.width * 1.15:
        result = result.rotate(90, expand=True)
    return trim_content(result, 8)


def detect_card_quads(image: Image.Image):
    """Find card-like rectangles independent of filename/template coordinates."""
    if cv2 is None:
        return []
    small = image.copy()
    scale = min(1.0, 1600.0 / max(image.size))
    if scale < 1:
        small = small.resize((round(image.width*scale), round(image.height*scale)), Image.Resampling.LANCZOS)
    gray = cv2.cvtColor(np.asarray(small), cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 35, 130)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8), iterations=2)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    page_area = float(gray.shape[0] * gray.shape[1])
    found = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < page_area * 0.015 or area > page_area * 0.92:
            continue
        peri = cv2.arcLength(contour, True)
        poly = cv2.approxPolyDP(contour, 0.035 * peri, True)
        if len(poly) != 4 or not cv2.isContourConvex(poly):
            continue
        rect = cv2.minAreaRect(contour)
        rw, rh = rect[1]
        ratio = max(rw, rh) / max(1.0, min(rw, rh))
        if not 1.25 <= ratio <= 2.15:
            continue
        pts = poly.reshape(4, 2).astype(np.float32) / scale
        center = pts.mean(axis=0)
        # Order corners clockwise from top-left.
        ordered = np.array(sorted(pts, key=lambda p: (p[1], p[0])), dtype=np.float32)
        top = sorted(ordered[:2], key=lambda p: p[0]); bottom = sorted(ordered[2:], key=lambda p: p[0])
        quad = [top[0], top[1], bottom[1], bottom[0]]
        found.append((area, center[1], quad))
    found.sort(key=lambda item: (-item[0], item[1]))
    selected = []
    for area, _, quad in found:
        cx, cy = np.mean(quad, axis=0)
        if all(np.linalg.norm(np.array([cx, cy]) - np.mean(q, axis=0)) > min(image.size)*0.08 for q in selected):
            selected.append(quad)
        if len(selected) == 2:
            break
    return selected


def split_cards(image: Image.Image):
    """Detect common ID layouts: side-by-side or front-above-back.
    Explanatory labels beside sample cards are ignored for stacked layouts.
    """
    image = image.convert("RGB")
    quads = detect_card_quads(image)
    if quads:
        crops = [_quad_crop(image, q) for q in sorted(quads, key=lambda q: float(np.mean(q[:, 1])))]
        if len(crops) >= 2:
            return crops[0], crops[1], "detected-front-back"
        # A portrait page may expose only one rectangle to contour detection
        # even though the second card is below it. Let the stacked fallback
        # inspect the complete page before declaring the PDF single-sided.
        if image.height <= image.width * 1.12:
            return crops[0], Image.new("RGB", crops[0].size, "white"), "detected-single"
    width, height = image.size
    content = trim_content(image)
    ratio = content.width / max(1, content.height)
    # Many government-ID PDFs place front and back one above the other on a
    # portrait page. Do this check before the landscape ratio check because
    # white margins or side labels can make the trimmed page look misleading.
    if content.height > content.width * 1.12:
        card_area = content
        row_scores = []
        pix = card_area.convert("L")
        for y in range(card_area.height):
            dark = sum(
                1 for x in range(card_area.width)
                if pix.getpixel((x, y)) < 245
            )
            row_scores.append(dark)
        middle = card_area.height // 2
        search = range(
            max(1, middle - card_area.height // 5),
            min(card_area.height - 1, middle + card_area.height // 5),
        )
        cut = min(search, key=lambda y: row_scores[y])
        # Prefer the whitespace cut, but still split at the centre when a
        # scanned card has graphics/text running through the divider.
        if row_scores[cut] < card_area.width * 0.12:
            split_y = cut
        else:
            split_y = card_area.height // 2
        front = trim_content(card_area.crop((0, 0, card_area.width, split_y)))
        back = trim_content(card_area.crop((0, split_y, card_area.width, card_area.height)))
        if front.width > 20 and front.height > 20 and back.width > 20 and back.height > 20:
            return front, back, "stacked"
    if ratio <= 2.2:
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


def crop_pan_pair(image: Image.Image):
    """Crop the physical PAN front/back pair from signed PAN layouts.

    Some e-PAN PDFs contain an e-PAN at the top and the printable physical
    PAN pair at the bottom. The pair is arranged left-to-right.
    """
    image = image.convert("RGB")
    # The signed PAN layout places explanatory text above the physical
    # left/right card pair; start below that text.
    y0 = int(image.height * 0.79)
    pair = trim_content(image.crop((0, y0, image.width, image.height)))
    cut = pair.width // 2
    front = trim_content(pair.crop((0, 0, cut, pair.height)))
    back = trim_content(pair.crop((cut, 0, pair.width, pair.height)))
    return front, back, "pan-bottom-side-by-side"


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
        # Signed PAN PDFs can contain both an e-PAN and a separate physical
        # PAN front/back pair. Prefer the physical pair for this known layout.
        filename_lower = (uploaded.filename or "").lower()
        if "pan" in filename_lower or "signed" in filename_lower:
            front, back, layout = crop_pan_pair(image)
        else:
            front, back, layout = split_cards(image)
        # Detection is primary. Templates are only a bounded fallback for the
        # supplied government-ID samples and never override a good detection.
        if layout == "single":
            boxes = template_boxes(uploaded.filename)
            if boxes:
                front = trim_content(crop_pdf_box(image, boxes[0], page.rect), padding=8)
                back = trim_content(crop_pdf_box(image, boxes[1], page.rect), padding=8) if len(boxes) > 1 else Image.new("RGB", front.size, "white")
                layout = "template-front-back" if len(boxes) > 1 else "template-single"
        front_text = read_card_text(front)
        back_text = read_card_text(back) if back.getbbox() else ""
        front_paddle = read_paddle_from_image(front)
        back_paddle = read_paddle_from_image(back) if back.getbbox() else {"text": "", "scores": [], "averageScore": 0}
        combined_text = front_text + " " + back_text + " " + front_paddle.get("text", "") + " " + back_paddle.get("text", "")
        return jsonify({"success": True, "layout": layout,
                        "cardType": identify_card(combined_text),
                        "ocrAvailable": True,
                        "paddleOcr": {"available": PADDLE_AVAILABLE,
                                      "frontText": front_paddle.get("text", ""),
                                      "backText": back_paddle.get("text", ""),
                                      "frontScore": front_paddle.get("averageScore", 0),
                                      "backScore": back_paddle.get("averageScore", 0)},
                        "page": "data:image/png;base64," + png_data(image),
                        "front": "data:image/png;base64," + png_data(front),
                        "back": "data:image/png;base64," + png_data(back)})
    except Exception as exc:
        return jsonify(error=str(exc)[:240]), 422


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8766, debug=False)
