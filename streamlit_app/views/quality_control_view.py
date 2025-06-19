import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from src.processes.quality_control_processor import QualityControlProcessor
from src.utils.config import load_config

def render_quality_control_view():
    """Render the dedicated quality control process view (sample)."""
    config = load_config()
    categories_config = config.get("categories", {})
    qc_config = categories_config.get("quality_control", {})
    process_names = qc_config.get("process_names", {})
    process_descriptions = qc_config.get("process_descriptions", {})
    display_name = process_names.get("quality_control_processor", "Quality Control Processor")
    description = process_descriptions.get("quality_control_processor", "Sample quality control process.")
    st.header(f"🔍 {display_name}")
    st.markdown(f"*{description}*")
    st.divider()
    st.subheader("📁 Upload Data for Quality Control")
    uploaded_file = st.file_uploader(
        "Choose a file:",
        type=['csv', 'xlsx', 'json'],
        key="quality_control_upload"
    )
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        data = load_data(uploaded_file)
        if data is not None:
            st.write("### Data Preview")
            st.dataframe(data.head(10), use_container_width=True)
            if st.button("🚦 Run Quality Control", type="primary"):
                show_missing_values(data)

def load_data(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            return pd.read_excel(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            return pd.read_json(uploaded_file)
        else:
            st.error("Unsupported file format")
            return None
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def show_missing_values(data):
    with st.spinner("🔄 Checking missing values..."):
        processor = QualityControlProcessor()
        results = processor.process_data({"data": data})
        if "error" in results:
            st.error(results["error"])
            return
        st.subheader("🧮 Missing Value Counts")
        missing = results.get("missing_values", {})
        if missing:
            st.dataframe(pd.DataFrame(list(missing.items()), columns=["Column", "Missing Values"]))
        else:
            st.info("No missing values found.") 