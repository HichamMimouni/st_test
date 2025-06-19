"""
Main Streamlit application for the Process Dashboard.
"""
import streamlit as st
import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add src to path for imports
src_path = Path(__file__).parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# Import views
from streamlit_app.views.home_view import render_home_view
from streamlit_app.views.processes_view import render_processes_view

# --- Custom Navigation ---
PAGES = {
    "Home": render_home_view,
    "Processes": render_processes_view,
}

def main():
    st.set_page_config(
        page_title="Process Dashboard",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Sidebar navigation
    st.sidebar.title("🚀 Process Dashboard")
    page = st.sidebar.radio(
        "Navigation",
        list(PAGES.keys()),
        key="main_nav_radio"
    )

    # Render selected page
    PAGES[page]()

if __name__ == "__main__":
    main() 