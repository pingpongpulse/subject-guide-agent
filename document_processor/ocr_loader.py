import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import pdfplumber
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def preprocess_image(image):
    """
    Preprocesses image for better OCR accuracy.
    Converts to grayscale, increases contrast, removes noise.
    """
    image = image.convert("L")  # grayscale
    image = ImageEnhance.Contrast(image).enhance(2.0)  # increase contrast
    image = image.filter(ImageFilter.SHARPEN)  # sharpen
    return image


def load_image(filepath):
    """
    Extracts text from image files using OCR.
    Supports PNG, JPG, JPEG, BMP, TIFF.
    """
    try:
        image = Image.open(filepath)
        image = preprocess_image(image)
        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(image, config=custom_config)

        return [{
            "text": text.strip(),
            "page_number": 1,
            "source_file": os.path.basename(filepath),
            "total_pages": 1,
            "extraction_method": "ocr_image"
        }]
    except Exception as e:
        print(f"  OCR image failed: {e}")
        return []


def load_scanned_pdf(filepath):
    """
    Handles scanned PDFs, image-based PDFs and mixed PDFs.
    For each page tries text extraction first.
    If text is too short falls back to OCR on that page.
    """
    pages = []

    try:
        with pdfplumber.open(filepath) as pdf:
            total_pages = len(pdf.pages)

            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text() or ""

                if len(text.strip()) < 50:
                    # Text extraction failed — use OCR on this page
                    try:
                        image = page.to_image(resolution=300).original
                        image = preprocess_image(image)
                        custom_config = r"--oem 3 --psm 6"
                        text = pytesseract.image_to_string(
                            image, config=custom_config
                        )
                        method = "ocr"
                    except Exception as e:
                        print(f"  OCR failed on page {page_num+1}: {e}")
                        text = ""
                        method = "failed"
                else:
                    method = "pdfplumber"

                if text.strip():
                    pages.append({
                        "text": text.strip(),
                        "page_number": page_num + 1,
                        "source_file": os.path.basename(filepath),
                        "total_pages": total_pages,
                        "extraction_method": method
                    })

    except Exception as e:
        print(f"  Scanned PDF loading failed: {e}")

    return pages


if __name__ == "__main__":
    result = load_scanned_pdf("data/sample_docs/test.pdf")
    for page in result:
        print(f"--- Page {page['page_number']} ({page['extraction_method']}) ---")
        print(page['text'][:300])
        print()