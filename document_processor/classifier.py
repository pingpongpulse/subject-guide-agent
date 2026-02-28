import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

KEYWORD_MAP = {
    "pyq": ["question paper", "previous year", "exam paper", "2022", "2023", "2024", "q1", "q2", "q3", "marks", "answer all"],
    "syllabus": ["syllabus", "curriculum", "course outline", "unit 1", "module 1", "credit hours", "course objectives"],
    "lab_manual": ["lab manual", "experiment", "aim", "apparatus", "procedure", "observation", "result", "viva"],
    "textbook": ["chapter", "definition", "theorem", "introduction", "bibliography", "index", "references"],
    "notes": ["notes", "lecture", "class notes", "summary", "topic", "unit"]
}

def rule_based_classify(filepath, text_preview=""):
    filename = os.path.basename(filepath).lower()
    combined = filename + " " + text_preview.lower()

    scores = {doc_type: 0 for doc_type in KEYWORD_MAP}

    for doc_type, keywords in KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword.lower() in combined:
                scores[doc_type] += 1

    best_match = max(scores, key=scores.get)
    best_score = scores[best_match]

    return best_match, best_score


def llm_classify(filepath, text_preview):
    prompt = f"""
Classify this document into exactly ONE of these categories:
pyq / syllabus / lab_manual / textbook / notes

Filename: {os.path.basename(filepath)}
Content preview: {text_preview[:300]}

Reply with ONLY the category label, nothing else.
"""
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    label = response.choices[0].message.content.strip().lower()
    valid_labels = ["pyq", "syllabus", "lab_manual", "textbook", "notes"]
    if label not in valid_labels:
        return "notes"
    return label


def classify_document(filepath, text_preview=""):
    best_match, best_score = rule_based_classify(filepath, text_preview)

    if best_score >= 2:
        print(f"[Rule-based] {os.path.basename(filepath)} → {best_match} (score: {best_score})")
        return best_match
    else:
        print(f"[LLM-based] {os.path.basename(filepath)} → asking LLM...")
        label = llm_classify(filepath, text_preview)
        print(f"[LLM-based] LLM says → {label}")
        return label


if __name__ == "__main__":
    test_cases = [
        ("dbms_2022_question_paper.pdf", "Q1. Explain normalization. Q2. What is ACID? 10 marks"),
        ("os_notes.pdf", "lecture notes on process scheduling and unit 1"),
        ("document1.pdf", "this is some random academic content without clear signals"),
        ("file123.pdf", ""),
    ]

    for filepath, preview in test_cases:
        label = classify_document(filepath, preview)
        print(f"Final: {filepath} → {label}")
        print()