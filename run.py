#!/usr/bin/env python3
"""
Simple run script for the Streamlit Process Dashboard.
"""
import subprocess
import sys
import os
from pathlib import Path

def main():
    """Run the Streamlit application."""
    # Get the directory of this script
    script_dir = Path(__file__).parent
    
    # Set the working directory
    os.chdir(script_dir)
    
    # Check if requirements are installed
    try:
        import streamlit
        import pandas
        import plotly
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Please install requirements: pip install -r requirements.txt")
        sys.exit(1)
    
    # Run the Streamlit app
    app_path = script_dir / "streamlit_app" / "app.py"
    
    if not app_path.exists():
        print(f"❌ App file not found: {app_path}")
        sys.exit(1)
    
    print("🚀 Starting Streamlit Process Dashboard...")
    print("📱 Open your browser to: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            str(app_path), "--server.port=8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 