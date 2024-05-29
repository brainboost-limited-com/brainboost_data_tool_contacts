import pytest
from src.EmailProcessor import EmailProcessor

# Fixture to create an instance of EmailProcessor for each test
@pytest.fixture
def email_processor():
    return EmailProcessor()

# Test cases for EmailProcessor class
class TestEmailProcessor:

    # Test case to verify email variations for a specific name and company
    def test_generate_email_variations(self, email_processor):
        name = "John Doe"
        company = "example"
        expected_emails = [
            "john.doe@example.com",
            "j.doe@example.com",
            "john.doe@example.net",
            "j.doe@example.net",
            "john.doe@example.org",
            "j.doe@example.org",
            "john.doe@example.co",
            "j.doe@example.co",
        ]

        # Generate email variations
        actual_emails = email_processor.generate_email_variations(name, company)

        # Assert that the generated email variations match the expected ones
        assert actual_emails == expected_emails

    # Add more test cases as needed...
