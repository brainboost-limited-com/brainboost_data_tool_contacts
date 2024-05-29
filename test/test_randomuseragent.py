import pytest
from unittest.mock import mock_open, patch
from src.UserAgentPool import UserAgentDatabase

@pytest.fixture
def user_agent_database():
    return UserAgentDatabase()

def test_get_random_line_existing_file(user_agent_database):
    # Mocking the open function to return specific lines
    lines = [
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36\n",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36\n",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240\n",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0\n",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko\n",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36\n",
        "Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko\n",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0\n"
    ]
    
    with patch("builtins.open", mock_open(read_data=''.join(lines))) as mock_file:
        random_line = user_agent_database.get_random_line()
        assert random_line

def test_get_random_line_empty_file(user_agent_database):
    with patch("builtins.open", mock_open(read_data="")) as mock_file:
        random_line = user_agent_database.get_random_line()
        assert random_line == "File is empty"

def test_get_random_line_file_not_found(user_agent_database):
    with patch("builtins.open", side_effect=FileNotFoundError()):
        random_line = user_agent_database.get_random_line()
        assert random_line.startswith("File not found")

def test_get_random_line_other_exceptions(user_agent_database):
    with patch("builtins.open", side_effect=Exception("Some error occurred")):
        random_line = user_agent_database.get_random_line()
        assert random_line.startswith("Error occurred")
