import pytest
from src.brainboost_data_person_names.NameProcessor import NameProcessor

# Define test cases using pytest
@pytest.mark.parametrize("full_name, expected_first_name, expected_last_name", [
    ("John Doe", "John", "Doe"),  # Simple case with two names
    ("Gabriel Tomas Borda Gomez", "Gabriel Tomas", "Borda Gomez"),  # Multiple names and last names
    ("Pablo Tomas Borda Di Berardino", "Pablo Tomas","Borda Di Berardino"),  # Single name (full name treated as first name)
    ("Vanessa Lewis", "Vanessa", "Lewis"),  # Two-part full name
    ("Johann Wolfgang von Goethe", "Johann Wolfgang", "von Goethe"),  # Compound last name
    ("", "", "")  # Empty full name
])
def test_extract_first_last_name_class(full_name, expected_first_name, expected_last_name):
    # Create an instance of NameProcessor
    name_processor = NameProcessor()
    
    # Call the method to extract first and last names
    first_name, last_name = name_processor.extract_first_last_name(full_name)
    
    # Assert that the extracted names match the expected names
    assert first_name == expected_first_name
    assert last_name == expected_last_name
