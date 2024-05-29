import pytest
import requests
from src.brainboost_data_source_search.GoogleSearchSerpapi import GoogleSearchSerpapi

@pytest.fixture
def mock_requests_get(mocker):
    return mocker.patch('requests.get')

def test_search_with_valid_query(mock_requests_get):
    # Arrange
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {'results': [{'title': 'Result 1'}, {'title': 'Result 2'}]}

    search_api = GoogleSearchSerpapi()

    # Act
    result = search_api.search(q='Python tutorial')

    # Assert
    mock_requests_get.assert_called_once_with('https://serpapi.com/search', 
                                              params={'q': 'Python tutorial', 'engine': 'google', 'api_key': search_api._api_key})
    assert result is not None
    assert isinstance(result, dict)
    assert 'results' in result
    assert len(result['results']) == 2
    assert result['results'][0]['title'] == 'Result 1'
    assert result['results'][1]['title'] == 'Result 2'

def test_search_with_empty_query(mock_requests_get):
    # Arrange
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 400

    search_api = GoogleSearchSerpapi()

    # Act
    result = search_api.search()

    # Assert
    mock_requests_get.assert_called_once_with('https://serpapi.com/search', params={'q': '', 'engine': 'google', 'api_key': search_api._api_key})
    assert result is None

def test_search_with_request_exception(mock_requests_get):
    # Arrange
    mock_requests_get.side_effect = requests.RequestException("Network error")

    search_api = GoogleSearchSerpapi()

    # Act
    result = search_api.search(q='Error')

    # Assert
    mock_requests_get.assert_called_once()
    assert result is None
