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
    
    # Load config for category and process names
    config = load_config()
    categories_config = config.get("categories", {})
    
    # Group processes by category
    categories = {}
    for process_name, process_class in processes.items():
        # Get category from class attribute or instance
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
    
    # Category selection
    category_names = list(categories.keys())
    
    if "selected_category" not in st.session_state:
        st.session_state["selected_category"] = category_names[0] if category_names else None
    
    # Create display names for categories
    category_display_names = []
    for category in category_names:
        if category in categories_config:
            display_name = categories_config[category].get("name", category)
        else:
            display_name = category.replace("_", " ").title()
        category_display_names.append(display_name)
    
    selected_category = st.selectbox(
        "📂 Select a Category:",
        category_names,
        format_func=lambda x: category_display_names[category_names.index(x)],
        key="category_selector"
    )
    
    if selected_category:
        st.session_state["selected_category"] = selected_category
        
        # Process selection within category
        category_processes = categories[selected_category]
        
        # Create process options with descriptions
        process_options = []
        for process_name, process_class in category_processes:
            # Get display name from config
            if selected_category in categories_config:
                process_names_config = categories_config[selected_category].get("process_names", {})
                display_name = process_names_config.get(process_name, process_name.replace("_", " ").title())
            else:
                display_name = process_name.replace("_", " ").title()
            
            # Get description from config
            if selected_category in categories_config:
                process_descriptions_config = categories_config[selected_category].get("process_descriptions", {})
                description = process_descriptions_config.get(process_name, "No description available")
            else:
                description = "No description available"
            
            process_options.append((process_name, display_name, description))
        
        # Show process selection
        if process_options:
            selected_option = st.selectbox(
                "🔧 Select a Process:",
                options=[opt[0] for opt in process_options],
                format_func=lambda x: next(opt[1] for opt in process_options if opt[0] == x),
                key="process_selector"
            )
            
            if selected_option:
                st.session_state["selected_process"] = selected_option
        else:
            st.warning("No processes available in this category.")


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