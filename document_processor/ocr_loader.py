import pytesseract
from PIL import Image
import pdfplumber
import os

# Set tesseract path — update this if yours is different
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def load_image(filepath):
    image = Image.open(filepath)
    text = pytesseract.image_to_string(image)

    return [{
        "text": text.strip(),
        "page_number": 1,
        "source_file": os.path.basename(filepath),
        "total_pages": 1
    }]


def load_scanned_pdf(filepath):
    pages = []

    with pdfplumber.open(filepath) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()

            if not text or len(text.strip()) < 20:
                # fallback to OCR if text extraction fails
                image = page.to_image(resolution=300).original
                text = pytesseract.image_to_string(image)

            if text and text.strip():
                pages.append({
                    "text": text.strip(),
                    "page_number": page_num + 1,
                    "source_file": os.path.basename(filepath),
                    "total_pages": len(pdf.pages)
                })

    return pages


if __name__ == "__main__":
    # Test with any image file you have
    result = load_image("data/sample_docs/test.png")
    print(result[0]['text'][:500])# displays 500 character from beginning remove limit for complete text displaying