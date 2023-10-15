"""
Author: Ori Boteach
File Name: server_helpers
Change Log: creation - 15/10/2023
"""

# --------------------------------HELPER SOCKET METHODS:
import socket

import chatlib
from constants import MAX_MSG_LENGTH, SERVER_IP, SERVER_PORT, PROTOCOL_SERVER


def build_and_send_message(conn: socket, cmd: str, msg: str) -> None:
    """
    the function builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket
    :param conn: socket object that is used to communicate with the client
    :param cmd: the command name
    :param msg: the message field
    :return: Nothing
    """

    # building a message by protocol with build_message()
    full_message = chatlib.build_message(cmd, msg)

    print("[SERVER] ", full_message)  # Debug print

    # sending the built message to the server
    conn.send(full_message.encode())


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


# --------------------------------Data Loaders:

def load_questions():
    """
    the function loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
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
    the function loads users list from file ## FILE SUPPORT TO BE ADDED LATER
    :return: user dictionary
    """

    users_dict = {
        "test": {"password": "test", "score": 0, "questions_asked": []},
        "yossi": {"password": "123", "score": 50, "questions_asked": []},
        "master": {"password": "master", "score": 200, "questions_asked": []}
    }
    return users_dict


# -------------------------SOCKET CREATOR:

def setup_socket() -> socket:
    """
    the function creates new listening socket and returns it
    :return: the socket object
    """

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()

    return server_socket


def send_error(conn: socket, error_msg: str):
    """
    the function sends an error response with the given message
    :param conn: socket object that is used to communicate with the client
    :param error_msg: a string representing the error
    """

    build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], error_msg)