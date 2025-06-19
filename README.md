# 🚀 Streamlit Process Dashboard

A clean, extensible, and developer-friendly Streamlit application for building internal process dashboards and tools. This boilerplate provides a modular architecture that makes it easy to add new processes and maintain a scalable codebase.

## 📁 Project Structure

```
project_root/
├── src/
│   ├── api/                    # API clients (stubbed)
│   │   ├── __init__.py
│   │   └── api_client.py       # Base API client class
│   ├── processes/              # Modular process logic
│   │   ├── __init__.py
│   │   ├── process_template.py # Base template for all processes
│   │   ├── data_summary.py     # Sample data analysis process
│   │   └── data_cleaner.py     # Sample data processing process
│   ├── utils/                  # Utilities (config, logger)
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration management
│   │   ├── logger.py          # Logging utilities
│   │   └── process_loader.py  # Dynamic process loading
│   └── scheduler/              # Placeholder for scheduling logic
│       ├── __init__.py
│       └── task_scheduler.py  # Background task scheduler
├── streamlit_app/
│   ├── app.py                  # Main entry point
│   ├── components/             # Shared UI components
│   │   ├── __init__.py
│   │   └── charts.py          # Reusable chart components
│   └── static/                 # Static assets (css/images)
│       └── style.css          # Custom CSS styling
├── configs/                    # YAML config files
│   └── app_config.yaml        # Main application configuration
├── requirements.txt
├── README.md
└── .gitignore
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project:**
   ```bash
   git clone <repository-url>
   cd streamlit-process-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run streamlit_app/app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:8501` to see the application.

## 🎯 Features

### ✅ Core Features

- **Multi-page Navigation**: Clean sidebar navigation with categorized processes
- **Dynamic Process Loading**: Auto-loads processes based on configuration
- **Modular Architecture**: Easy to add new processes without modifying core code
- **Configuration Management**: YAML-based configuration for easy customization
- **Logging System**: Comprehensive logging for debugging and monitoring
- **Error Handling**: Graceful error handling with user-friendly messages
- **Export Functionality**: Built-in export options for process results
- **Responsive Design**: Works on desktop and mobile devices

### 📊 Sample Processes

The application comes with two sample processes to demonstrate the architecture:

1. **Data Summary** (`data_summary.py`)
   - Upload CSV files
   - Generate comprehensive statistics
   - Missing value analysis
   - Correlation analysis
   - Interactive visualizations

2. **Data Cleaner** (`data_cleaner.py`)
   - Data preprocessing and cleaning
   - Missing value handling
   - Duplicate removal
   - Outlier detection and handling
   - Data type conversion

## 🛠️ Adding New Processes

### Step 1: Create Process File

Create a new Python file in `src/processes/` directory:

```python
# src/processes/my_process.py
import streamlit as st
from typing import Dict, Any
from .process_template import ProcessTemplate

class MyProcess(ProcessTemplate):
    def __init__(self):
        super().__init__()
        self.name = "My Process"
        self.description = "Description of what this process does"
        self.icon = "🔧"
        self.category = "data_processing"  # Must match config
    
    def render_input_form(self) -> Dict[str, Any]:
        """Render input form for your process."""
        inputs = {}
        
        # Add your input widgets here
        inputs['text_input'] = st.text_input("Enter text")
        inputs['number_input'] = st.number_input("Enter number", min_value=0)
        
        return inputs
    
    def process_data(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process the data based on inputs."""
        # Your processing logic here
        result = f"Processed: {inputs.get('text_input', '')}"
        
        return {
            "result": result,
            "processed_data": inputs
        }
    
    def render_output(self, results: Dict[str, Any]) -> None:
        """Render the output display."""
        st.success("Processing completed!")
        st.write(results["result"])
```

### Step 2: Update Configuration

Add your process to `configs/app_config.yaml`:

```yaml
categories:
  data_processing:
    name: "Data Processing"
    description: "Tools for cleaning and transforming data"
    icon: "🔄"
    processes:
      - data_cleaner
      - my_process  # Add your process here
```

### Step 3: Test Your Process

1. Restart the Streamlit application
2. Navigate to your category in the sidebar
3. Click on your process to test it

## ⚙️ Configuration

### App Configuration (`configs/app_config.yaml`)

The main configuration file controls:

- **App Settings**: Title, description, version
- **Categories**: Process categories and their organization
- **UI Settings**: Theme colors, layout preferences
- **Features**: Logging, error tracking, analytics

### Key Configuration Sections

```yaml
app:
  title: "Process Dashboard"
  description: "A clean and extensible Streamlit application"
  version: "1.0.0"

categories:
  your_category:
    name: "Your Category"
    description: "Description of your category"
    icon: "📊"
    processes:
      - process1
      - process2

ui:
  theme:
    primary_color: "#FF6B6B"
    background_color: "#FFFFFF"
  
  layout:
    sidebar_width: 300
    max_width: 1200
```

## 🎨 Customization

### Styling

Customize the appearance by modifying `streamlit_app/static/style.css`:

```css
/* Custom button styling */
.stButton > button {
    border-radius: 8px;
    border: 1px solid #ddd;
    transition: all 0.3s ease;
}

/* Process header styling */
.process-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem;
    border-radius: 12px;
}
```

### Process Template Customization

The `ProcessTemplate` class provides several methods you can override:

- `render_parameters_panel()`: Add custom sidebar parameters
- `_render_export_section()`: Customize export options
- `render()`: Override the entire rendering logic

## 🔧 Development

### Project Structure Best Practices

1. **Process Organization**: Group related processes in the same category
2. **Naming Conventions**: Use snake_case for file names and process names
3. **Error Handling**: Always include try-catch blocks in process methods
4. **Logging**: Use the logger for debugging and monitoring
5. **Documentation**: Add docstrings to all classes and methods

### Adding Dependencies

1. Add new packages to `requirements.txt`
2. Update the version constraints as needed
3. Document any new dependencies in this README

### Testing

1. Test each process with various input scenarios
2. Verify error handling works correctly
3. Check that exports function properly
4. Test on different screen sizes for responsiveness

## 🚀 Deployment

### Local Development

```bash
streamlit run streamlit_app/app.py
```

### Production Deployment

1. **Streamlit Cloud**: Deploy directly to Streamlit Cloud
2. **Docker**: Create a Dockerfile for containerized deployment
3. **Cloud Platforms**: Deploy to AWS, GCP, or Azure

### Environment Variables

Set these environment variables for production:

```bash
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
```

## 📝 Logging

The application includes comprehensive logging:

- **File Logs**: Stored in `logs/` directory
- **Console Logs**: Displayed in terminal
- **Process Logs**: Track process execution and errors

Log files are automatically created with timestamps and rotated daily.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Test thoroughly
5. Submit a pull request

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Add docstrings to all functions
- Keep functions small and focused

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

1. **Process not loading**: Check that the process class inherits from `ProcessTemplate`
2. **Import errors**: Ensure all dependencies are installed
3. **Configuration errors**: Validate YAML syntax in config files

### Getting Help

- Check the logs in the `logs/` directory
- Enable debug mode in the sidebar
- Review the process template documentation
- Check the Streamlit documentation for widget usage

## 🔮 Future Enhancements

- [ ] User authentication and authorization
- [ ] Database integration for storing results
- [ ] Advanced scheduling capabilities
- [ ] API integrations for external services
- [ ] Real-time data processing
- [ ] Advanced visualization options
- [ ] Process chaining and workflows
- [ ] Performance monitoring and analytics

---

**Happy coding! 🚀**

For questions or support, please open an issue in the repository. 