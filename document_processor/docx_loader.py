from docx import Document
import os

def load_docx(filepath):
    doc = Document(filepath)
    full_text = []

    for para in doc.paragraphs:
        if para.text.strip():
            full_text.append(para.text.strip())

    combined_text = "\n".join(full_text)

    return [{
        "text": combined_text,
        "page_number": 1,
        "source_file": os.path.basename(filepath),
        "total_pages": 1
    }]


if __name__ == "__main__":
    result = load_docx("data/sample_docs/test.docx")
    print(result[0]['text'][:500]) # displays 500 character from beginnign remove limit for complete text displaying