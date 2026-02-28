from pptx import Presentation
import os

def load_pptx(filepath):
    prs = Presentation(filepath)
    slides = []

    for slide_num, slide in enumerate(prs.slides):
        slide_text = []

        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text.strip():
                slide_text.append(shape.text.strip())

        if slide_text:
            slides.append({
                "text": "\n".join(slide_text),
                "page_number": slide_num + 1,
                "source_file": os.path.basename(filepath),
                "total_pages": len(prs.slides)
            })

    return slides


if __name__ == "__main__":
    result = load_pptx("data/sample_docs/test.pptx")
    for slide in result:
        print(f"--- Slide {slide['page_number']} ---")
        print(slide['text'][:300])# displays 300 character from beginnign remove limit for complete text displaying
        print()