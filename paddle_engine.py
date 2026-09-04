from paddleocr import PaddleOCR

ocr_engine = PaddleOCR(
    enable_mkldnn=False,
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,
)


def read_with_paddle(image_path):
    result = ocr_engine.predict(image_path)
    texts = []
    scores = []

    for page in result:
        data = page.json
        res = data.get("res", {})
        texts.extend(res.get("rec_texts", []))
        scores.extend(res.get("rec_scores", []))

    numeric_scores = [float(score) for score in scores]
    return {
        "text": " ".join(str(text) for text in texts),
        "scores": numeric_scores,
        "averageScore": sum(numeric_scores) / len(numeric_scores) if numeric_scores else 0,
    }
