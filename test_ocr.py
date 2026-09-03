import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

image = Image.open(r"C:\Users\harsh\test-card.jpg").convert("L")
image = image.resize((image.width * 2, image.height * 2))

text = pytesseract.image_to_string(
    image,
    lang="eng+hin+mar",
    config="--oem 3 --psm 6"
)

print(text)
