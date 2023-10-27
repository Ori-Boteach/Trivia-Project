"""
Author: Ori Boteach
File Name: server_loaders_test (pytest unnitesting for the server side)
Change Log: creation - 17/10/2023
"""
import requests
from unittest.mock import mock_open, patch, Mock
from server_data_loaders import load_questions, load_user_database, load_web_questions


# ----------- load_questions tests:
@patch('builtins.open', new_callable=mock_open)
def test_load_questions_valid_file(mock_file):
    """
    a test that checks if the load_questions function returns the expected dictionary for valid JSON file
    :param mock_file: a mock of a valid JSON file
    """
    # Arrange - mock the file content
    questions_json = '[{"id": 1, "question": "What is 1+1?", "answers": ["1", "2"], "correct": 2}]'
    expected_result = {1: {"question": "What is 1+1?", "answers": ["1", "2"], "correct": 2}}

    # configure the mock file's read method to return the mock JSON data
    mock_file.return_value.read.return_value = questions_json

    # Act
    result = load_questions()

    # Assert that the function returns as expected
    assert result == expected_result


@patch('builtins.open', side_effect=IOError)
def test_load_questions_io_error(mock_file):
    """
    a test that checks if the load_questions function returns empty dictionary for an io error
    :param mock_file: a mock of a JSON file with an io error
    """
    # Act - test for a file with an io error
    result = load_questions()

    # Assert that the result is an empty dictionary because of the error
    assert result == {}


@patch('builtins.open', new_callable=mock_open)
def test_load_questions_invalid_json(mock_file):
    """
    a test that checks if the load_questions function returns empty dictionary for invalid JSON file
    :param mock_file: a mock of a JSON file
    """
    # Arrange - mock the file content with invalid JSON
    invalid_json = 'not a valid JSON'
    mock_file.return_value.read.return_value = invalid_json

    # Act - test for a file with invalid JSON content
    result = load_questions()

    # Assert that the result is an empty dictionary because of the error
    assert result == {}


# ----------- load_users tests:
@patch('builtins.open', new_callable=mock_open)
def test_load_user_database_valid_file(mock_file):
    """
    a test that checks if the load_user_database function returns the expected dictionary for valid JSON file
    :param mock_file: a mock of a valid JSON file
    """
    # Arrange - mock the file content
    users_json = '{"test": {"password": "test", "score": 0, "questions_asked": []},' \
                 '"yossi": {"password": "123", "score": 50, "questions_asked": []}}'
    expected_result = {"test": {"password": "test", "score": 0, "questions_asked": []},
                       "yossi": {"password": "123", "score": 50, "questions_asked": []}}

    # configure the mock file's read method to return the mock JSON data
    mock_file.return_value.read.return_value = users_json

    # Act
    result = load_user_database()

    # Assert that the function returns as expected
    assert result == expected_result


@patch('builtins.open', side_effect=IOError)
def test_load_user_database_io_error(mock_file):
    """
    a test that checks if the load_user_database function returns empty dictionary for io error
    :param mock_file: a mock of a JSON file with an io error
    """
    # Act - test for a file with an I/O error
    result = load_user_database()

    # Assert that the result is an empty dictionary because of the error
    assert result == {}


@patch('builtins.open', new_callable=mock_open)
def test_load_user_database_invalid_json(mock_file):
    """
    a test that checks if the load_user_database function returns empty dictionary for invalid JSON file
    :param mock_file: a mock of a JSON file
    """
    # Arrange - mock the file content with invalid JSON
    invalid_json = 'not a valid JSON'
    mock_file.return_value.read.return_value = invalid_json

    # Act - test for a file with invalid JSON content
    result = load_user_database()

    # Assert that the result is an empty dictionary because of the error
    assert result == {}


# ----------- load_web_questions tests:
@patch('requests.get')
def test_load_web_questions_successful(mock_get):
    """
    a test to checks if the load_web_questions function returns an expected dictionary length
    for a successful request (checks correct invalid questions reduction)
    :param mock_get: a mock of the requests.get() function
    """
    # Arrange - prepare the mock response
    mock_response = Mock()
    mock_response.json.return_value = {
        'results': [
            {'question': 'Question 1', 'correct_answer': 'A', 'incorrect_answers': ['D', 'B', 'C']},
            {'question': 'Question 2', 'correct_answer': 'X', 'incorrect_answers': ['W', 'Y', 'Z']},
            {'question': 'should&be&reduced', 'correct_answer': 'A', 'incorrect_answers': ['D', 'B', 'C']},
        ]
    }
    # simulate a successful request
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Act
    questions_dict = load_web_questions()

    # Assert
    assert len(questions_dict) == 2


@patch('requests.get')
def test_load_web_questions_request_exception(mock_get):
    """
    a test to checks if the load_web_questions function returns an empty dictionary for an invalid API request
    :param mock_get: a mock of the requests.get() function
    """
    # Arrange - create a mock response that raises a RequestException
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException('mocked request exception')
    mock_get.return_value = mock_response

    # Act
    result = load_web_questions()

    # Assert that the result is an empty dictionary because of the error
    assert result == {}
