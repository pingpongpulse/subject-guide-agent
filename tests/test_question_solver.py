import sys
import os
import pytest
from unittest.mock import patch, MagicMock
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.router import route_query

@pytest.mark.parametrize("query,difficulty", [
    ("Explain the Banker's algorithm for deadlock avoidance with example", "intermediate"),
    ("A system has 3 processes and 4 resources. Find if the system is in safe state.", "intermediate"),
    ("Derive the expression for effective access time in demand paging", "exam"),
])
def test_route_query_bankers_algorithm(query, difficulty):
    # Mock the groq client to avoid API calls
    with patch('agents.query_classifier._get_groq_client') as mock_get_client:
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "question_solving"
        mock_client.chat.completions.create.return_value = mock_response
        mock_get_client.return_value = mock_client
        
        # Mock the retriever
        with patch('agents.router.retrieve_docs') as mock_retrieve:
            mock_retrieve.return_value = [
                {"page_content": "Banker's algorithm explanation", "metadata": {"source_file": "os_notes.pdf", "page_number": 23}}
            ]
            
            # Mock the groq_client in question_solver
            with patch('agents.question_solver._get_groq_client') as mock_groq_qs:
                mock_response_qs = MagicMock()
                mock_response_qs.choices[0].message.content = "theory"
                mock_groq_qs.chat.completions.create.return_value = mock_response_qs
                
                # Mock the solve_question to return the formatted answer
                with patch('agents.question_solver.solve_question') as mock_solve:
                    mock_solve.return_value = """**Question Type:** Theory

**Answer:**
The Banker's algorithm is a deadlock avoidance algorithm...

**Key Points:**
- Maintains safe state
- Checks allocation safety

**Citations:**
- os_notes.pdf | Page 23"""
                    
                    result = route_query(query, difficulty=difficulty)
                    
                    assert "agent" in result
                    assert "category" in result
                    assert "answer" in result
                    assert "QuestionSolverAgent" in result["agent"]
                    assert "question_solving" in result["category"]
                    print(f"Test passed for query: {query[:50]}...")