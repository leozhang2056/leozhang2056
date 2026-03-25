import pytest
import tempfile
import os
from pathlib import Path
import yaml
from unittest.mock import patch, MagicMock


class TestLoadYaml:
    def test_load_yaml_success(self):
        """Test successful YAML loading."""
        from app.backend.generate_cv_from_kb import load_yaml

        # Create a temporary YAML file
        data = {"key": "value", "number": 42}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(data, f)
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == data
        finally:
            os.unlink(temp_path)

    def test_load_yaml_file_not_found(self):
        """Test handling of non-existent file."""
        from app.backend.generate_cv_from_kb import load_yaml

        result = load_yaml("non_existent_file.yaml")
        assert result == {}

    def test_load_yaml_empty_file(self):
        """Test handling of empty YAML file."""
        from app.backend.generate_cv_from_kb import load_yaml

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")  # Empty file
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_load_yaml_invalid_yaml(self):
        """Test handling of invalid YAML syntax."""
        from app.backend.generate_cv_from_kb import load_yaml

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [\n")  # Invalid YAML
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_load_yaml_invalid_file_path_type(self):
        """Test handling of invalid file path type."""
        from app.backend.generate_cv_from_kb import load_yaml

        result = load_yaml(123)  # Invalid type
        assert result == {}

    @patch('app.backend.generate_cv_from_kb.html_to_pdf')
    @patch('app.backend.generate_cv_from_kb.run_enhanced_validation')
    @patch('app.backend.generate_cv_from_kb.format_quality_report_markdown')
    def test_load_yaml_empty_file(self, mock_format, mock_validation, mock_html_to_pdf):
        """Test handling of empty YAML file."""
        from app.backend.generate_cv_from_kb import load_yaml

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("")  # Empty file
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    @patch('app.backend.generate_cv_from_kb.html_to_pdf')
    @patch('app.backend.generate_cv_from_kb.run_enhanced_validation')
    @patch('app.backend.generate_cv_from_kb.format_quality_report_markdown')
    def test_load_yaml_invalid_yaml(self, mock_format, mock_validation, mock_html_to_pdf):
        """Test handling of invalid YAML syntax."""
        from app.backend.generate_cv_from_kb import load_yaml

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [\n")  # Invalid YAML
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    @patch('app.backend.generate_cv_from_kb.html_to_pdf')
    @patch('app.backend.generate_cv_from_kb.run_enhanced_validation')
    @patch('app.backend.generate_cv_from_kb.format_quality_report_markdown')
    def test_load_yaml_invalid_file_path_type(self, mock_format, mock_validation, mock_html_to_pdf):
        """Test handling of invalid file path type."""
        from app.backend.generate_cv_from_kb import load_yaml

        result = load_yaml(123)  # Invalid type
        assert result == {}