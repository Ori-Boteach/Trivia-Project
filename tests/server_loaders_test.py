"""
Author: Ori Boteach
File Name: server_loaders_test (pytest unnitesting for the client side)
Change Log: creation - 17/10/2023
"""
from unittest.mock import mock_open, patch
from server_data_loaders import load_questions, load_user_database


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

    # Act - call the function to load questions
    result = load_questions()

    # Assert that the function returns the expected questions dictionary
    assert result == expected_result


@patch('builtins.open', side_effect=IOError)
def test_load_questions_io_error(mock_file):
    """
    a test that checks if the load_questions function returns empty dictionary for io error
    :param mock_file: a mock of a JSON file with an io error
    """
    # Act - test when a file with an io error
    result = load_questions()

    # Assert
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

    # Act - test when the JSON content is not valid
    result = load_questions()

    # Assert that the result is an empty dictionary
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

    # Act - call the function to load user database
    result = load_user_database()

    # Assert that the function returns the expected users dictionary
    assert result == expected_result


@patch('builtins.open', side_effect=IOError)
def test_load_user_database_io_error(mock_file):
    """
    a test that checks if the load_user_database function returns empty dictionary for io error
    :param mock_file: a mock of a JSON file with an io error
    """
    # Act - test when an I/O error occurs
    result = load_user_database()

    # Assert that the result is an empty dictionary
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

    # Act - test when the JSON content is not valid
    result = load_user_database()

    # Assert that the result is an empty dictionary
    assert result == {}
