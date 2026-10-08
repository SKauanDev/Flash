"""Built-in Flash tools.

Importing this module registers the built-in tools with the global registry.
"""
from app.tools import tasks as _tasks  # noqa: F401

__all__ = ["_tasks"]
