"""
Unified path setup for app/backend modules.

This module ensures consistent import behavior whether modules are imported:
- As a package: `from app.backend.module import func`
- Directly: `from module import func` (when app/backend is in sys.path)

Usage:
    At the top of each backend module that needs sibling imports:
    
    from _path_setup import setup_backend_path
    setup_backend_path()
    
    # Now sibling imports work regardless of how this module was invoked
    from sibling_module import some_function
"""

import sys
from pathlib import Path

_backend_dir = Path(__file__).parent.resolve()
_setup_done = False


def setup_backend_path() -> None:
    """Add app/backend to sys.path if not already present."""
    global _setup_done
    if _setup_done:
        return
    
    backend_str = str(_backend_dir)
    if backend_str not in sys.path:
        sys.path.insert(0, backend_str)
    
    _setup_done = True


def get_repo_root() -> Path:
    """Return the repository root directory (parent of app/)."""
    return _backend_dir.parent.parent
