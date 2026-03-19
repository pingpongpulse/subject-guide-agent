import streamlit as st

from agents.router import route_query
from utils.context_formatter import format_sources_list
from vectorstore.retriever import retrieve_docs


def show_query_page():
    st.header("Ask a Question")
    st.write("Ask a question and get an answer based on the documents you uploaded.")

    query = st.text_input("Your question")

    if not query:
        st.info("Enter a question to get started.")
        return

    if st.button("Ask"):
        with st.spinner("Thinking..."):
            result = route_query(query)
            answer = result.get("answer", "")
            docs = retrieve_docs(query, k=4)

        st.markdown("### Answer")
        st.write(answer)

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
