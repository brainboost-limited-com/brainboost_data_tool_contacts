import os
import json
import pytest
import update_companydomains_database

@pytest.fixture
def tmp_output_file(tmpdir):
    return os.path.join(tmpdir, 'output.json')

@pytest.fixture
def tmp_checkpoint_file(tmpdir):
    return os.path.join(tmpdir, 'checkpoint.json')

def test_process_contacts_resumes_from_checkpoint(tmp_output_file, tmp_checkpoint_file):
    # Simulate existing checkpoint with processed_count = 2
    initial_progress = {'processed_count': 2}
    with open(tmp_checkpoint_file, 'w') as f:
        json.dump(initial_progress, f)

    # Mock contacts data (for testing purposes)
    contacts = [
        {'name': 'John Doe', 'company': 'XYZ Corp'},
        {'name': 'Jane Smith', 'company': 'ABC Inc'},
        {'name': 'Alex Johnson', 'company': '123 Co'},
        {'name': 'Sarah Brown', 'company': '456 Ltd'}
    ]

    # Test the processing function
    processed_contacts = update_companydomains_database.process_contacts_with_progress(contacts, tmp_output_file, tmp_checkpoint_file)

    # Verify the processed contacts list has expected length
    assert len(processed_contacts) == 2  # Only contacts from index 2 onwards should be processed

    # Verify the output file has expected content
    with open(tmp_output_file, 'r') as f:
        processed_data = json.load(f)
        assert len(processed_data) == 2  # Output file should contain 2 processed contacts

    # Verify the checkpoint file is deleted after processing
    assert not os.path.exists(tmp_checkpoint_file)
