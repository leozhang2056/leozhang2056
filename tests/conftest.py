import pytest
from unittest.mock import patch, MagicMock


def pytest_configure(config):
    """Set up global patches before any module imports."""
    patch(
        'app.backend.generate_cv_html_to_pdf.html_to_pdf',
        MagicMock(),
    ).start()
    patch(
        'app.backend.cv_quality_validator.generate_quality_report',
        MagicMock(),
    ).start()
    patch(
        'app.backend.cv_quality_validator.format_quality_report_markdown',
        MagicMock(),
    ).start()