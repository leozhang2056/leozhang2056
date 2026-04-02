import pytest
from unittest.mock import patch, MagicMock

# Store active patches for proper cleanup
_active_patches = []


def pytest_configure(config):
    """Set up global patches before any module imports."""
    patches = [
        patch('app.backend.generate_cv_html_to_pdf.html_to_pdf', MagicMock()),
        patch('app.backend.cv_quality_validator.generate_quality_report', MagicMock()),
        patch('app.backend.cv_quality_validator.format_quality_report_markdown', MagicMock()),
    ]
    for p in patches:
        p.start()
        _active_patches.append(p)


def pytest_unconfigure(config):
    """Clean up patches after all tests complete."""
    for p in _active_patches:
        p.stop()
    _active_patches.clear()