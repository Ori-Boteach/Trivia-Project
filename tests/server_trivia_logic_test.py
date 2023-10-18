"""
Author: Ori Boteach
File Name: server_trivia_logic_test (pytest unnitesting for the server side)
Change Log: creation - 18/10/2023
"""
from unittest.mock import Mock, patch
import server
from server import handle_question_message, handle_answer_message
from server_helpers import messages_to_send


@patch('server.create_question')
def test_handle_question_message(mock_create_question):
    """
    test the handle_question_message function and validate that it sends a question message to the client
    :param mock_create_question: a mock of the create_question function
    """
    # Arrange
    mock_socket = Mock()
    username = "test"
    expected_message = "YOUR_QUESTION   |0022|1#What is 2+2?#4#3#5#2"
    mock_create_question.return_value = "1#What is 2+2?#4#3#5#2"

    # Act
    handle_question_message(mock_socket, username)

    # Assert (check if the correct question message was sent)
    assert (mock_socket, expected_message.encode()) in messages_to_send


@patch('server.questions', {1: {"id": 1, "question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2}})
def test_wrong_answer():
    """
    test the handle_answer_message function and validate that it sends a wrong answer message to the client if needed
    """
    # Arrange
    mock_socket = Mock()
    expected_message = "WRONG_ANSWER    |0001|2"

    # Act
    handle_answer_message(mock_socket, "1#incorrect_answer")

    # Assert (check a wrong answer message was sent)
    assert (mock_socket, expected_message.encode()) in messages_to_send


@patch('server.questions', {1: {"id": 1, "question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2}})
@patch('server.users', {"test": {"password": "test", "score": 0, "questions_asked": ["1"]}})
@patch('server.logged_users', {("127.0.0.1", 52116): "test", ("127.0.0.1", 52117): "master"})
def test_right_answer():
    """
    test the handle_answer_message function and validate that it sends a right answer message to the client if needed
    In addition, check that the user score is updated
    """
    # Arrange
    mock_socket = Mock()
    expected_message = "CORRECT_ANSWER  |0000|"

    # Configure the getpeername method on the mock socket
    mock_socket.getpeername.return_value = ("127.0.0.1", 52116)

    # Act
    handle_answer_message(mock_socket, "1#2")

    # Assert (check a right answer message was sent + the user score was updated!)
    assert (mock_socket, expected_message.encode()) in messages_to_send
    assert server.users["test"]["score"] == 5
