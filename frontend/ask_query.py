import streamlit as st

from agents.router import route_query
from utils.context_formatter import format_sources_list
from vectorstore.retriever import retrieve_docs


def render_formula(formula_obj, index):
    """Render a single formula in a nice format."""
    with st.container():
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"**Formula {index}:**")
        with col2:
            st.latex(formula_obj.get("formula", ""))
        
        st.markdown(f"**Variables:** {formula_obj.get('variables', 'N/A')}")
        st.markdown(f"**Meaning:** {formula_obj.get('explanation', 'N/A')}")
        st.markdown(f"**Use Case:** {formula_obj.get('use_case', 'N/A')}")
        st.divider()


def show_query_page():
    st.header("Ask a Question")
    st.write("Ask a question and get an answer based on the documents you uploaded.")

    query = st.text_input("Your question")

    # Subject filter
    subject = st.selectbox(
        "Filter by Subject (optional)",
        ["All", "OS", "DBMS", "CN", "General"],
        help="Filter documents by subject category. Select 'All' to search all subjects."
    )
    subject_filter = None if subject == "All" else subject.lower()

    if not query:
        st.info("Enter a question to get started.")
        return

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            result = route_query(query, subject=subject_filter)
            answer = result.get("answer", "")
            docs = retrieve_docs(query, k=4, subject=subject_filter)

        st.markdown("### Answer")
        st.write(answer)

        # Display formulas if present
        if "formulas" in result and result["formulas"]:
            st.markdown("### Formulas & Equations")
            st.write(f"Found {len(result['formulas'])} formula(s) in the source materials:")
            for i, formula in enumerate(result["formulas"], 1):
                render_formula(formula, i)

        if docs:
            st.markdown("### Sources")
            sources = format_sources_list(docs)
            for i, src in enumerate(sources, start=1):
                st.markdown(f"**{i}. {src}**")

            st.markdown("### Source previews")
            for doc in docs:
                source = doc.metadata.get("source_file", "unknown")
                page = doc.metadata.get("page_number", "?")
                preview = doc.page_content.strip().replace("\n", " ")
                preview = preview[:300] + ("..." if len(preview) > 300 else "")
                st.write(f"**{source} — Page {page}**: {preview}")
        else:
            st.info("No relevant documents found. Try uploading some documents first.")
