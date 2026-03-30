from app.backend.role_inference import infer_role_from_text


def test_infer_role_android():
    assert infer_role_from_text("Senior Android Kotlin Jetpack Compose engineer") == "android"


def test_infer_role_ai():
    assert infer_role_from_text("LLM and PyTorch model optimization with ONNX") == "ai"


def test_infer_role_backend():
    assert infer_role_from_text("Java Spring Boot microservice and Redis APIs") == "backend"


def test_infer_role_default_fullstack_for_empty_text():
    assert infer_role_from_text("") == "fullstack"

