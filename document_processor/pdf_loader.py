import PyPDF2
import os

def load_pdf(filepath):
    pages = []
    
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        total_pages = len(reader.pages)
        
        for page_num in range(total_pages):
            page = reader.pages[page_num]
            text = page.extract_text()
            
            if text and text.strip():
                pages.append({
                    "text": text.strip(),
                    "page_number": page_num + 1,
                    "source_file": os.path.basename(filepath),
                    "total_pages": total_pages
                })
    
    return pages


if __name__ == "__main__":
    result = load_pdf("data/sample_docs/test.pdf")
    for page in result:
        print(f"--- Page {page['page_number']} ---")
        print(page['text'][:300])# displays 300 character from beginnign remove limit for complete text displaying
        print()