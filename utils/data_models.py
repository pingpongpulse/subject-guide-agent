"""
Data Models and Schemas for Agent Outputs

Provides structured data models for all agent responses to ensure consistency, 
validation, and UI integration.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime


class DocumentType(str, Enum):
    """Supported document types."""
    NOTES = "notes"
    TEXTBOOK = "textbook"
    PYQ = "pyq"
    SYLLABUS = "syllabus"
    PRESENTATION = "pptx"
    RESEARCH_PAPER = "research"


class SummaryFormat(str, Enum):
    """Supported summary output formats."""
    STANDARD = "standard"
    LIGHTNING = "lightning"
    DETAILED = "detailed"
    CHECKLIST = "checklist"


class DifficultyLevel(str, Enum):
    """Difficulty levels for answers."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    EXAM = "exam"


# ==================== General Purpose Models ====================

@dataclass
class Citation:
    """Represents a single source citation."""
    source_file: str
    page_number: str
    doc_type: Optional[str] = None
    subject: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def __str__(self) -> str:
        return f"{self.source_file} | Page {self.page_number}"


@dataclass
class CitationGroup:
    """Groups citations for a specific claim or section."""
    claim: str
    citations: List[Citation] = field(default_factory=list)
    
    def add_citation(self, source_file: str, page_number: str, doc_type: Optional[str] = None):
        """Add a citation to this group."""
        self.citations.append(Citation(source_file, page_number, doc_type))


# ==================== Study Plan Models ====================

@dataclass
class StudySession:
    """Represents a single study session within a day."""
    time_period: str  # e.g., "Morning 9:00-12:00"
    duration_hours: float
    topics: List[str]
    activities: List[str]  # e.g., ["read", "practice problems", "summarize"]
    learning_objectives: List[str]
    key_concepts: List[str]


@dataclass
class StudyDay:
    """Represents a single day in the study plan."""
    day_number: int
    date: Optional[str] = None
    main_topic: str = ""
    sessions: List[StudySession] = field(default_factory=list)
    revision_topics: List[str] = field(default_factory=list)
    practice_questions: List[str] = field(default_factory=list)
    estimated_total_hours: float = 0.0
    citations: List[Citation] = field(default_factory=list)
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['citations'] = [c.to_dict() for c in self.citations]
        return data


@dataclass
class StudyPlan:
    """Complete study plan."""
    course_name: str
    total_days: int
    hours_per_day: float
    created_at: datetime = field(default_factory=datetime.now)
    days: List[StudyDay] = field(default_factory=list)
    topics_to_cover: List[str] = field(default_factory=list)
    revision_strategy: Optional[str] = None
    exam_tips: List[str] = field(default_factory=list)
    citations: List[Citation] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['days'] = [d.to_dict() for d in self.days]
        data['citations'] = [c.to_dict() for c in self.citations]
        return data


# ==================== Summary Models ====================

@dataclass
class KeyConcept:
    """A key concept with definition and citations."""
    term: str
    definition: str
    explanation: Optional[str] = None
    citations: List[Citation] = field(default_factory=list)
    related_terms: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['citations'] = [c.to_dict() for c in self.citations]
        return data


@dataclass
class Formula:
    """A formula or theorem with context."""
    name: str
    formula: str
    description: Optional[str] = None
    variables: Dict[str, str] = field(default_factory=dict)  # variable: meaning
    derivation: Optional[str] = None
    citations: List[Citation] = field(default_factory=list)
    use_cases: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['citations'] = [c.to_dict() for c in self.citations]
        return data


@dataclass
class WorkedExample:
    """A complete worked example with citations."""
    title: str
    problem_statement: str
    solution_steps: List[str]
    final_answer: str
    key_insight: Optional[str] = None
    common_mistakes: List[str] = field(default_factory=list)
    citations: List[Citation] = field(default_factory=list)
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['citations'] = [c.to_dict() for c in self.citations]
        data['difficulty'] = self.difficulty.value
        return data


@dataclass
class ExamQuestion:
    """A potential exam question."""
    question_text: str
    expected_points: Optional[int] = None
    estimated_time: Optional[str] = None
    difficulty: DifficultyLevel = DifficultyLevel.INTERMEDIATE
    question_type: Optional[str] = None  # theory, numerical, m-c, short-answer
    citations: List[Citation] = field(default_factory=list)


@dataclass
class Summary:
    """Comprehensive summary with all components."""
    topic: str
    format: SummaryFormat = SummaryFormat.STANDARD
    created_at: datetime = field(default_factory=datetime.now)
    
    # Content components
    key_concepts: List[KeyConcept] = field(default_factory=list)
    formulas: List[Formula] = field(default_factory=list)
    worked_examples: List[WorkedExample] = field(default_factory=list)
    exam_questions: List[ExamQuestion] = field(default_factory=list)
    
    # Text sections
    introduction: Optional[str] = None
    quick_facts: List[str] = field(default_factory=list)
    common_mistakes: List[str] = field(default_factory=list)
    memory_tricks: List[str] = field(default_factory=list)
    
    # Metadata
    all_citations: List[Citation] = field(default_factory=list)
    prerequisites: List[str] = field(default_factory=list)
    related_topics: List[str] = field(default_factory=list)
    revision_priority: Optional[str] = None  # high, medium, low
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['format'] = self.format.value
        data['created_at'] = self.created_at.isoformat()
        data['key_concepts'] = [c.to_dict() for c in self.key_concepts]
        data['formulas'] = [f.to_dict() for f in self.formulas]
        data['worked_examples'] = [e.to_dict() for e in self.worked_examples]
        data['exam_questions'] = [
            {
                'question_text': q.question_text,
                'expected_points': q.expected_points,
                'estimated_time': q.estimated_time,
                'difficulty': q.difficulty.value,
                'question_type': q.question_type,
                'citations': [c.to_dict() for c in q.citations]
            }
            for q in self.exam_questions
        ]
        data['all_citations'] = [c.to_dict() for c in self.all_citations]
        return data


# ==================== Lightning Summary Models ====================

@dataclass
class OneLiner:
    """A single-line fact or definition."""
    text: str
    citations: List[Citation] = field(default_factory=list)
    category: Optional[str] = None  # concept, formula, fact, definition


@dataclass
class LightningSummary:
    """Ultra-concise summary for quick revision."""
    topic: str
    created_at: datetime = field(default_factory=datetime.now)
    
    one_liners: List[OneLiner] = field(default_factory=list)  # Up to 30
    key_definitions: List[KeyConcept] = field(default_factory=list)  # Up to 15
    formulas: List[str] = field(default_factory=list)  # Up to 10
    exam_questions: List[str] = field(default_factory=list)  # Up to 20
    memory_tricks: List[str] = field(default_factory=list)
    
    all_citations: List[Citation] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['one_liners'] = [
            {
                'text': ol.text,
                'citations': [c.to_dict() for c in ol.citations],
                'category': ol.category
            }
            for ol in self.one_liners
        ]
        data['key_definitions'] = [c.to_dict() for c in self.key_definitions]
        data['all_citations'] = [c.to_dict() for c in self.all_citations]
        return data


# ==================== Study Checklist Model ====================

@dataclass
class ChecklistItem:
    """A single checklist item."""
    text: str
    category: str  # concept, formula, problem-type, etc.
    importance: str = "medium"  # high, medium, low
    completed: bool = False
    citations: List[Citation] = field(default_factory=list)


@dataclass
class StudyChecklist:
    """Checklist-style study guide."""
    topic: str
    created_at: datetime = field(default_factory=datetime.now)
    
    prerequisites: List[ChecklistItem] = field(default_factory=list)
    must_know_concepts: List[ChecklistItem] = field(default_factory=list)
    formulas_to_memorize: List[ChecklistItem] = field(default_factory=list)
    problem_types: List[str] = field(default_factory=list)
    practice_questions: List[ExamQuestion] = field(default_factory=list)
    common_pitfalls: List[str] = field(default_factory=list)
    
    # Exam strategy
    time_allocation: Dict[str, int] = field(default_factory=dict)  # part: minutes
    priority_order: List[str] = field(default_factory=list)  # most to least important
    
    all_citations: List[Citation] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['all_citations'] = [c.to_dict() for c in self.all_citations]
        return data


# ==================== Agent Response Models ====================

@dataclass
class AgentResponse:
    """Standard response from any agent."""
    agent_name: str
    query: str
    category: str
    success: bool = True
    
    # Response content
    answer: str  # Primary text answer
    structured_data: Optional[Dict[str, Any]] = None  # Additional structured output
    
    # Metadata
    processing_time_ms: Optional[float] = None
    model_used: str = "llama-3.3-70b-versatile"
    tokens_used: Optional[int] = None
    citations: List[Citation] = field(default_factory=list)
    
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['citations'] = [c.to_dict() for c in self.citations]
        return data


# ==================== Utility Functions ====================

def create_citation_from_doc(doc: Any) -> Citation:
    """
    Create a Citation object from a document (either Document object or dict).
    """
    if hasattr(doc, 'metadata'):
        # ChromaDB Document object
        return Citation(
            source_file=doc.metadata.get("source_file", "unknown"),
            page_number=str(doc.metadata.get("page_number", "?")),
            doc_type=doc.metadata.get("doc_type"),
            subject=doc.metadata.get("subject")
        )
    else:
        # Plain dict
        return Citation(
            source_file=doc.get("source_file", "unknown"),
            page_number=str(doc.get("page_number", "?")),
            doc_type=doc.get("doc_type"),
            subject=doc.get("subject")
        )


def citations_from_docs(docs: List[Any]) -> List[Citation]:
    """Extract unique citations from a list of documents."""
    citations = []
    seen = set()
    
    for doc in docs:
        citation = create_citation_from_doc(doc)
        key = f"{citation.source_file}_{citation.page_number}"
        if key not in seen:
            seen.add(key)
            citations.append(citation)
    
    return citations
