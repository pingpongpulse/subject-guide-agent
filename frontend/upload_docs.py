import os

import streamlit as st

from vectorstore.chunker import chunk_document
from vectorstore.store import add_documents


UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")


def ensure_upload_dir():
    os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_uploaded_file(uploaded_file) -> str:
    ensure_upload_dir()
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def show_upload_page():
    st.header("Upload Documents")
    st.write("Upload PDF / DOCX / PPTX / PNG files to add them to the knowledge base.")

    # Subject selection
    subject = st.selectbox(
        "Select Subject",
        ["OS", "DBMS", "CN", "General"],
        help="Choose the subject category for these documents."
    )

    uploaded_files = st.file_uploader(
        "Select files",
        type=["pdf", "docx", "pptx", "png"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        st.info("Upload one or more documents to get started.")
        return

    if st.button("Process Documents"):
        with st.spinner("Processing documents..."):
            total_chunks = 0
            for uploaded in uploaded_files:
                file_path = save_uploaded_file(uploaded)
                chunks = chunk_document(file_path, subject=subject.lower())
                add_documents(chunks)
                total_chunks += len(chunks)

        st.success(
            f"✅ Processed {len(uploaded_files)} file(s) and stored {total_chunks} chunks in vector DB."
        )
        st.write("You can now ask questions in the **Ask Question** tab.")
