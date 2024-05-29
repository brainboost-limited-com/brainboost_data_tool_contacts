from datetime import datetime
import os
import json
import pytest
from src.brainboost_data_source_processing.JSonProcessor import JSonProcessor  # Update this import with your module name
from pytest_mock import mocker

# Your other imports...


# Define the test directory path containing sample JSON files
TEST_DIR = '/brainboost/brainboost_data/data_tools/tools_goldenthinkerextractor_dataprocessing/resources/resources_data/data_subjective'

# Define a fixture to set up and tear down resources for testing
@pytest.fixture(scope="module")
def json_processor_instance():
    # Instantiate JSonProcessor
    json_processor = JSonProcessor()
    yield json_processor
    # Clean up: Delete the default output file if it was generated
    default_output_file = os.path.join(os.getcwd(), f"{os.path.basename(os.getcwd())}-{json_processor._generate_default_filename()}")
    if os.path.exists(default_output_file):
        os.remove(default_output_file)



@pytest.fixture
def mock_records():
    # Mocked records data for testing
    return [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        {"id": 3, "value": 30},
    ]


# Test function to verify write with default filename
def test_output_merged_json_default_filename(json_processor_instance):

    def generate_default_filename():
        # Get the name of the last folder in the current directory path
        last_folder_name = os.path.basename(os.getcwd())

        # Generate filename with current timestamp
        timestamp = datetime.now().strftime('%Y%m%d%H%M')
        default_filename = f"{last_folder_name}-{timestamp}.json"

        return default_filename
    # Get JSonProcessor instance from fixture
    json_processor = json_processor_instance

    # Call load_json_files_recursively to load and merge JSON arrays
    json_data = json_processor.load_json_files_recursively(TEST_DIR)

    #Assert that the operation was successful
    assert len(json_data) > 0
    

    # Call write without specifying output_file_path (using default filename)
    result = json_processor.write(json_data)

    # Assert that the operation was successful
    assert result is True

    # Assert that the default output file was generated
    default_output_file = generate_default_filename()
    assert os.path.exists(default_output_file)

# Test function to verify write with custom filename
def test_output_merged_json_custom_filename(json_processor_instance):
    # Get JSonProcessor instance from fixture
    json_processor = json_processor_instance

    # Call load_json_files_recursively to load and merge JSON arrays
    json_data = json_processor.load_json_files_recursively(TEST_DIR)

    # Specify a custom output file path
    custom_output_file = 'custom_merged_data.json'

    # Call write with custom output_file_path
    result = json_processor.write(json_data, custom_output_file)

    # Assert that the operation was successful
    assert result is True

    # Assert that the custom output file was generated
    assert os.path.exists(custom_output_file)



def test_add_calculated_field_to_objects(json_processor_instance):
    # Mock input data (list of dictionary objects representing records)
    mock_records = [
        {'name': 'Alice', 'hourly_rate': 25, 'hours_worked': 40},
        {'name': 'Bob', 'hourly_rate': 30, 'hours_worked': 45},
        {'name': 'Charlie', 'hourly_rate': 20, 'hours_worked': 50}
    ]

    # Mock calculation function (for example, compute total salary)
    def mock_calculation(record):
        hourly_rate = record['hourly_rate']
        hours_worked = record['hours_worked']
        total_salary = hourly_rate * hours_worked
        return total_salary

    # Define the field name for the new calculated field
    field_name = 'total_salary'

    # Call the method under test with the mocked input data and calculation function
    updated_records = json_processor_instance.add_calculated_field_to_the_objects_from_an_array(
        mock_records,
        field_name,
        mock_calculation
    )

    # Assert that the method returns the updated list of records
    assert isinstance(updated_records, list)
    assert len(updated_records) == len(mock_records)

    # Assert that each record in the updated list contains the new calculated field
    for record in updated_records:
        assert field_name in record
        assert isinstance(record[field_name], (int, float))  # Ensure the calculated value is numeric

        # Perform additional assertions based on the specific calculation and expected values
        # For example, assert the correctness of the calculated total salary based on input data

        # Example assertion:
        # Calculate expected total salary for comparison
        expected_total_salary = mock_calculation(record)
        assert record[field_name] == expected_total_salary



# Test function to verify add_calculated_field_to_objects
def test_add_calculated_field_to_objects(json_processor_instance):
    # Mock input data (list of dictionary objects representing records)
    mock_records = [
        {'name': 'Alice', 'hourly_rate': 25, 'hours_worked': 40},
        {'name': 'Bob', 'hourly_rate': 30, 'hours_worked': 45},
        {'name': 'Charlie', 'hourly_rate': 20, 'hours_worked': 50}
    ]

    # Mock calculation function (for example, compute total salary)
    def mock_calculation(record):
        hourly_rate = record['hourly_rate']
        hours_worked = record['hours_worked']
        total_salary = hourly_rate * hours_worked
        return total_salary

    # Define the field name for the new calculated field
    field_name = 'total_salary'

    # Call the method under test with the mocked input data and calculation function
    updated_records = json_processor_instance.add_calculated_field_to_the_objects_from_an_array(
        mock_records,
        field_name,
        mock_calculation
    )

    # Assert that the method returns the updated list of records
    assert isinstance(updated_records, list)
    assert len(updated_records) == len(mock_records)

    # Assert that each record in the updated list contains the new calculated field
    for record in updated_records:
        assert field_name in record
        assert isinstance(record[field_name], (int, float))  # Ensure the calculated value is numeric

        # Perform additional assertions based on the specific calculation and expected values
        # For example, assert the correctness of the calculated total salary based on input data

        # Example assertion:
        # Calculate expected total salary for comparison
        expected_total_salary = mock_calculation(record)
        assert record[field_name] == expected_total_salary