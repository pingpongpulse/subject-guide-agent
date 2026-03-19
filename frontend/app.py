import os
import sys

import streamlit as st

# Ensure project root is on sys.path when running via `streamlit run frontend/app.py`
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from frontend.ask_query import show_query_page
from frontend.upload_docs import show_upload_page


def main():
    st.set_page_config(page_title="Subject Guide Agent", layout="wide")

    st.sidebar.title("Subject Guide Agent")
    page = st.sidebar.radio("Go to", ["Upload Documents", "Ask Question"])

    if page == "Upload Documents":
        show_upload_page()
    else:
        show_query_page()


if __name__ == "__main__":
    main()
