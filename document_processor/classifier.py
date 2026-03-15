import os
from groq import Groq
from dotenv import load_dotenv

# We keep the map at the top level as it is a constant
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
    return best_match, scores[best_match]

def llm_classify(filepath, text_preview):
    # FIXED: Initializing inside the function to ensure load_dotenv() has run
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("⚠️ Warning: GROQ_API_KEY not found. Defaulting to 'notes'.")
        return "notes"
        
    groq_client = Groq(api_key=api_key)

    prompt = f"""
Classify this document into exactly ONE of these categories:
pyq / syllabus / lab_manual / textbook / notes

Filename: {os.path.basename(filepath)}
Content preview: {text_preview[:300]}

Reply with ONLY the category label, nothing else.
"""
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        label = response.choices[0].message.content.strip().lower()
        valid_labels = ["pyq", "syllabus", "lab_manual", "textbook", "notes"]
        return label if label in valid_labels else "notes"
    except Exception as e:
        print(f"❌ Groq Error: {e}")
        return "notes"

def classify_document(filepath, text_preview=""):
    best_match, best_score = rule_based_classify(filepath, text_preview)
    if best_score >= 2:
        return best_match
    return llm_classify(filepath, text_preview)