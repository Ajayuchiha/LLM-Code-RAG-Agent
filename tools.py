from langchain_core.tools import Tool
from langchain_experimental.tools import PythonREPLTool
from file_manager import FileManager


# --------------------
# RAW PYTHON FUNCTIONS
# --------------------

def list_files(_=None):
    """List all files inside the project codebase."""
    return FileManager.list_files()


def read_file(path: str):
    """Read a file from the project codebase."""
    return FileManager.read(path)


def write_file(data: dict):
    """Write content to a file. Requires: path, content."""
    return FileManager.write(data["path"], data["content"])


def apply_diff(data: dict):
    """Apply a unified diff patch to an existing file."""
    return FileManager.apply_diff(data["path"], data["diff"])


# Python execution tool (already a LC tool)
python_repl = PythonREPLTool()
