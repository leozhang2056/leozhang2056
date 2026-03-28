import os
import tempfile

import yaml


class TestLoadYaml:
    def test_load_yaml_success(self):
        from app.backend.generate_cv_from_kb import load_yaml

        data = {"key": "value", "number": 42}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(data, f)
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == data
        finally:
            os.unlink(temp_path)

    def test_load_yaml_file_not_found(self):
        from app.backend.generate_cv_from_kb import load_yaml

        result = load_yaml("non_existent_file.yaml")
        assert result == {}

    def test_load_yaml_empty_file(self):
        from app.backend.generate_cv_from_kb import load_yaml

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("")
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_load_yaml_invalid_yaml(self):
        from app.backend.generate_cv_from_kb import load_yaml

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [\n")
            temp_path = f.name

        try:
            result = load_yaml(temp_path)
            assert result == {}
        finally:
            os.unlink(temp_path)

    def test_load_yaml_invalid_file_path_type(self):
        from app.backend.generate_cv_from_kb import load_yaml

        result = load_yaml(123)
        assert result == {}
