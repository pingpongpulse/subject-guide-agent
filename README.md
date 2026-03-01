Multi-Agent RAG Academic Assistant
Overview

This project implements a Multi-Agent Retrieval-Augmented Generation (RAG) Academic Assistant that enables students to query their academic materials and receive structured, citation-grounded answers. The system processes uploaded textbooks, notes, presentations, and previous year question papers (PYQs), stores them in a vector database, and uses specialized LLM agents to provide explanations, solve questions, analyze trends, and generate study plans.

Unlike traditional chatbots, this system ensures responses are grounded in the user’s own academic documents using semantic retrieval and metadata filtering, significantly reducing hallucinations.

Objectives

The primary objectives of this project are:

• Build a robust document ingestion and retrieval pipeline
• Implement a vector database using semantic embeddings
• Develop multiple specialized LLM agents with clear responsibilities
• Provide structured academic answers with source citations
• Enable PYQ analysis and study plan generation
• Deploy an interactive academic assistant interface

High-Level Architecture
System Architecture Flow
                ┌────────────────────┐
                │  User Uploads Docs │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Document Processor │
                │ (PDF/DOCX/PPTX)   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Text Chunking     │
                │ + Metadata       │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Embedding Model   │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ ChromaDB Vector   │
                │ Database          │
                └─────────┬──────────┘
                          │
                          ▼
                    User Query
                          │
                          ▼
                ┌────────────────────┐
                │ Query Classifier   │
                └──────┬─────┬──────┘
                       │     │
                       ▼     ▼
              Topic Explainer   Question Solver
                  Agent             Agent
                       │
                       ▼
                ┌────────────────────┐
                │ Retrieval Pipeline │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ LLM Generation     │
                └─────────┬──────────┘
                          │
                          ▼
                ┌────────────────────┐
                │ Streamlit UI       │
                └────────────────────┘
Core System Components
1. Document Processing Layer

Responsible for extracting text from uploaded files.

Supported formats:

• PDF (PyPDF2)
• DOCX (python-docx)
• PPTX (python-pptx)
• Image / scanned PDFs (OCR — optional)

Functions:

• Extract text content
• Preserve page numbers
• Assign document metadata
• Classify document type automatically

Metadata generated:

{
  source_file,
  doc_type,
  page_number,
  subject,
  upload_time
}
2. Chunking Pipeline

Purpose: Split large text into manageable semantic units.

Configuration:

• Chunk size: 500 tokens
• Overlap: 50 tokens

Why overlap is used:

Prevents context loss across chunk boundaries.

Output:

{
 chunk_text,
 metadata
}
3. Embedding and Vector Store

Embedding Model:

• OpenAI embeddings or Gemini embeddings

Vector Database:

• ChromaDB

Purpose:

• Convert text chunks into vector representations
• Enable semantic similarity search

Advantages of ChromaDB:

• Fast retrieval
• Lightweight
• Persistent storage
• Metadata filtering support

4. Retrieval Pipeline

Function:

retrieve(query, filters=None)

Steps:

Convert query to embedding

Search ChromaDB for similar chunks

Apply metadata filters if needed

Return top-k relevant chunks

Supports:

• Semantic search
• Metadata filtered retrieval
• Multi-document referencing

5. Multi-Agent Layer

The system uses specialized agents, each responsible for specific tasks.

Agent 1: Query Classifier Agent

Purpose:

Classifies user query into appropriate category.

Categories:

• Topic explanation
• Question solving
• PYQ analysis
• Study plan generation
• Revision

This enables modular multi-agent architecture.

Agent 2: Topic Explainer Agent

Purpose:

Explains academic topics using retrieved document content.

Workflow:

User Query
→ Retrieval
→ LLM
→ Structured Answer

Output format:

• Definition
• Explanation
• Example
• Related concepts
• Sources

Agent 3: Question Solver Agent

Purpose:

Solves exam-style questions using retrieved academic content.

Capabilities:

• Theory question solving
• Numerical question solving
• Step-by-step derivations
• Structured answers

Agent 4: PYQ Analyzer Agent (Planned)

Purpose:

Analyze previous year question papers.

Capabilities:

• Topic extraction
• Frequency analysis
• Topic importance ranking
• Heatmap visualization

Agent 5: Study Plan Agent (Planned)

Purpose:

Generate personalized study plans.

Input:

• Syllabus
• Available documents

Output:

• Week-wise study schedule
• Prioritized topics
• Revision planning

Key Features
Completed Features

• Document ingestion pipeline
• Multi-format document support
• Text chunking with metadata
• Vector database integration
• Semantic retrieval pipeline

Features In Progress

• Topic Explainer Agent
• Query Classifier Agent
• Streamlit UI

Planned Features

• Question Solver Agent
• PYQ Analyzer Agent
• Study Plan Generator
• Hybrid search (BM25 + semantic)
• Revision agent
• Citation tracking

Technical Stack

Programming Language:

• Python

Vector Database:

• ChromaDB

LLM Framework:

• LangChain

LLM Providers:

• OpenAI / Google Gemini

Document Processing:

• PyPDF2
• python-docx
• python-pptx
• pytesseract (OCR)

Frontend:

• Streamlit
