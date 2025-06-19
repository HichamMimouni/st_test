"""
Processes View - Handles process selection and dynamic loading.
"""
import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from src.utils.process_loader import ProcessLoader
from src.utils.config import load_config


def render_processes_view():
    """Render the processes view with category and process selection."""
    
    # # Page header
    # st.header("⚙️ Process Management")
    # st.markdown("*Select and execute data processing workflows*")
    # st.divider()
    
    process_loader = ProcessLoader()
    try:
        processes = process_loader.get_available_processes()
    except Exception as e:
        st.error(f"Error loading processes: {str(e)}")
        return
    
    # Render process selection
    render_process_selection(processes)
    
    # Render selected process
    if "selected_process" in st.session_state:
        render_selected_process(st.session_state["selected_process"])


def render_process_selection(processes: dict):
    """Render the process selection interface."""
    config = load_config()
    categories_config = config.get("categories") or {}
    categories = {}
    for process_name, process_class in processes.items():
        category = getattr(process_class, 'category', None)
        if not category:
            try:
                instance = process_class()
                category = getattr(instance, 'category', 'Uncategorized')
            except:
                category = 'Uncategorized'
        if category not in categories:
            categories[category] = []
        categories[category].append((process_name, process_class))
    category_names = list(categories.keys())
    category_display_names = [
        categories_config.get(cat, {}).get("name", cat.replace("_", " ").title())
        for cat in category_names
    ]
    category_names_with_empty = [None] + category_names
    category_display_names_with_empty = ["-- Select a Category --"] + category_display_names
    process_options = []
    selected_category = None
    selected_option = None
    col1, col2 = st.columns(2)
    with col1:
        selected_category = st.selectbox(
            "📂 Select a Category:",
            category_names_with_empty,
            format_func=lambda x: category_display_names_with_empty[category_names_with_empty.index(x)] if x in category_names_with_empty else x,
            key="category_selector"
        )
        if not selected_category:
            st.warning("No category selected, please choose one.")
            st.session_state.pop("selected_category", None)
            st.session_state.pop("selected_process", None)
    if selected_category:
        st.session_state["selected_category"] = selected_category
        category_processes = categories[selected_category]
        process_options = [(None, "-- Select a Process --", "")] + [
            (process_name,
             categories_config.get(selected_category, {}).get("process_names", {}).get(process_name, process_name.replace("_", " ").title()),
             categories_config.get(selected_category, {}).get("process_descriptions", {}).get(process_name, "No description available")
            )
            for process_name, process_class in category_processes
        ]
    with col2:
        selected_option = st.selectbox(
            "🔧 Select a Process:",
            options=[opt[0] for opt in process_options] if process_options else [None],
            format_func=lambda x: next(opt[1] for opt in process_options if opt[0] == x) if process_options else "-- Select a Process --",
            key="process_selector"
        )
        if not selected_option:
            st.warning("No process selected, please choose one.")
            st.session_state.pop("selected_process", None)
    if selected_category and selected_option:
        st.session_state["selected_process"] = selected_option


def render_selected_process(process_name: str):
    """Render the selected process interface."""
    
    # Check if this process has a dedicated view
    if process_name == "risk_analysis":
        # Import and use the dedicated view
        from streamlit_app.views.risk_analysis_view import render_risk_analysis_view
        render_risk_analysis_view()
    elif process_name == "quality_control_processor":
        from streamlit_app.views.quality_control_view import render_quality_control_view
        render_quality_control_view()
    else:
        # Show not implemented message
        
        # Load config to get process display name
        config = load_config()
        categories_config = config.get("categories", {})
        
        # Find the process display name
        process_display_name = process_name.replace("_", " ").title()
        
        for category_config in categories_config.values():
            process_names = category_config.get("process_names", {})
            if process_name in process_names:
                process_display_name = process_names[process_name]
                break
        
        # Show not implemented message
        st.info(f"🔧 **{process_display_name}**")
        st.warning("⚠️ **Not Yet Implemented**")
        st.write("This process does not have a dedicated view yet.")
        st.write("Please check back later for updates.") 