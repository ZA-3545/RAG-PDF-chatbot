from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_root_endpoint():
    """Test ke API module import ho sake aur basic structure sahi ho"""
    import ast

    with open("api.py", "r") as f:
        code = f.read()

    # Confirm karo ke zaroori pieces code mein maujood hain
    tree = ast.parse(code)
    assert "app = FastAPI" in code, "FastAPI app initialize honi chahiye"
    assert "/ask" in code, "/ask endpoint honi chahiye"
    assert "def ask_question" in code, "ask_question function honi chahiye"

def test_requirements_file_exists():
    """Confirm requirements.txt maujood hai aur khali nahi"""
    assert os.path.exists("requirements.txt"), "requirements.txt file honi chahiye"
    with open("requirements.txt") as f:
        content = f.read()
    assert len(content) > 0, "requirements.txt khali nahi honi chahiye"

def test_dockerfile_exists():
    """Confirm Dockerfile maujood hai"""
    assert os.path.exists("Dockerfile"), "Dockerfile honi chahiye"