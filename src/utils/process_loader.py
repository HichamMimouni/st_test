"""
Process loader utility for dynamically loading processes.
"""
import importlib
import sys
from pathlib import Path
import inspect

# Add src to path if not already there
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

class ProcessLoader:
    """Dynamically loads process classes from the processes directory."""
    def get_available_processes(self):
        processes_dir = Path(__file__).parent.parent / "processes"
        available_processes = {}
        if processes_dir.exists():
            for file_path in processes_dir.glob("*.py"):
                if file_path.name.startswith("__") or file_path.name == "process_template.py":
                    continue
                module_name = f"processes.{file_path.stem}"
                try:
                    module = importlib.import_module(module_name)
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if hasattr(obj, 'process_data') and callable(getattr(obj, 'process_data')):
                            available_processes[file_path.stem] = obj
                except Exception:
                    continue
        return available_processes


# Global process loader instance
process_loader = ProcessLoader() 