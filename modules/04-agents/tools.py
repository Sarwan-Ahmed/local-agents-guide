"""Shared tools for both graph_agent.py and shortcut_agent.py -- same two tools from module 03."""

from datetime import datetime, timezone
from pathlib import Path

from langchain_core.tools import tool

SANDBOX_DIR = Path(__file__).parent


@tool
def get_current_time() -> str:
    """Get the current UTC date and time."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


@tool
def read_file(filename: str) -> str:
    """Read the contents of a file by name from the current module's folder."""
    path = (SANDBOX_DIR / filename).resolve()
    if SANDBOX_DIR.resolve() not in path.parents and path != SANDBOX_DIR.resolve():
        return "Error: can only read files inside this module's folder."
    if not path.is_file():
        return f"Error: {filename} not found."
    return path.read_text()


TOOLS = [get_current_time, read_file]
