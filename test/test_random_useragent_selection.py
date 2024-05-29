import os
from unittest.mock import patch
from brainboost_data_source_requests_package.UserAgentPool import UserAgentDatabase

def test_get_random_line():
    # Mock the file content and file path
    file_content = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3\n",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36\n",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0\n"
    ]
    file_path = '/path/to/your/test_file.txt'

    # Create a temporary file with mock content
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(file_content)

    # Create an instance of UserAgentDatabase
    user_agent_db = UserAgentDatabase()

    # Patch the open function to mock file reading
    with patch('builtins.open', side_effect=lambda *args, **kwargs: open(file_path, *args, **kwargs)) as mock_open:
        # Test case: Random line is retrieved successfully
        random_line = user_agent_db.get_random_line()
        assert random_line in file_content

        # Test case: Empty file handling
        empty_file_path = '/path/to/empty_file.txt'
        with patch('builtins.open', side_effect=lambda *args, **kwargs: open(empty_file_path, *args, **kwargs)):
            empty_line = user_agent_db.get_random_line()
            assert empty_line == "File is empty"

        # Test case: File not found handling
        non_existing_file_path = '/path/to/non_existing_file.txt'
        file_not_found_line = user_agent_db.get_random_line()
        assert file_not_found_line.startswith("File not found")

    # Clean up: Delete the temporary file
    os.remove(file_path)

    # Clean up: Delete any potentially created empty file
    if os.path.exists(empty_file_path):
        os.remove(empty_file_path)
