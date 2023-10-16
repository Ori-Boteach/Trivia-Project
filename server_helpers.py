"""
Author: Ori Boteach
File Name: server_helpers
Change Log: creation - 15/10/2023
"""

import socket
import chatlib
from constants import MAX_MSG_LENGTH, SERVER_IP, SERVER_PORT


# HELPER SOCKET METHOD:
def recv_message_and_parse(conn: socket) -> tuple[str, str]:
    """
    the function receives a new message from given socket,
    then parses the message using chatlib
    :param conn: socket object that is used to communicate with the client
    :return: cmd (str) and data (str) of the received message.
             If error occurred, will return None, None
    """
    full_message = conn.recv(MAX_MSG_LENGTH).decode()

    print("[CLIENT] ", full_message)  # Debug print

    cmd, data = chatlib.parse_message(full_message)

    return cmd, data


# Data Loaders:
def load_questions():
    """
    the function loads questions bank
    :return: questions dictionary
    """

    questions_dict = {
        2313: {"question": "How much is 2+2", "answers": ["3", "4", "2", "1"], "correct": 2},
        4122: {"question": "What is the capital of France?", "answers": ["Lion", "Marseille", "Paris", "Montpellier"],
               "correct": 3}
    }

    return questions_dict


def load_user_database():
    """
    the function loads users list
    :return: user dictionary
    """

    users_dict = {
        "test": {"password": "test", "score": 0, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []}
    }
    return users_dict


# SOCKET CREATOR:
def setup_socket() -> socket:
    """
    the function creates new listening socket and returns it
    :return: the socket object
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    return server_socket
