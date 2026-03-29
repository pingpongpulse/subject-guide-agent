from pypdf import PdfReader
import pdfplumber
import os

def load_pdf(filepath):
    """
    Smart PDF loader that handles:
    - Normal text PDFs
    - Mixed content PDFs
    - PPT-converted PDFs
    Falls back to pdfplumber for better extraction on complex layouts.
    """
    pages = []

    # First attempt with pdfplumber — better than PyPDF2 for complex layouts
    try:
        with pdfplumber.open(filepath) as pdf:
            total_pages = len(pdf.pages)

            for page_num, page in enumerate(pdf.pages):
                text = ""

                # Try extracting normal text first
                extracted = page.extract_text()
                if extracted:
                    text += extracted.strip()

                # Also try extracting tables if present
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        for row in table:
                            row_text = " | ".join(
                                [str(cell) if cell else "" for cell in row]
                            )
                            text += "\n" + row_text

                if text.strip():
                    pages.append({
                        "text": text.strip(),
                        "page_number": page_num + 1,
                        "source_file": os.path.basename(filepath),
                        "total_pages": total_pages,
                        "extraction_method": "pdfplumber"
                    })

    except Exception as e:
        print(f"  pdfplumber failed: {e} — trying PyPDF2")

        # Fallback to PyPDF2
        try:
            with open(filepath, "rb") as file:
                reader = PdfReader(file)
                total_pages = len(reader.pages)

                for page_num in range(total_pages):
                    page = reader.pages[page_num]
                    text = page.extract_text()

                    if text and text.strip():
                        pages.append({
                            "text": text.strip(),
                            "page_number": page_num + 1,
                            "source_file": os.path.basename(filepath),
                            "total_pages": total_pages,
                            "extraction_method": "pypdf"
                        })
        except Exception as e2:
            print(f"  pypdf also failed: {e2}")

    return pages


if __name__ == "__main__":
    result = load_pdf("data/sample_docs/test.pdf")
    for page in result:
        print(f"--- Page {page['page_number']} ({page['extraction_method']}) ---")
        print(page['text'][:300])
        print()