"""
Author: Ori Boteach
File Name: server_helpers
Change Log: creation - 15/10/2023
"""
import json
import socket
import chatlib
from constants import MAX_MSG_LENGTH, SERVER_IP, SERVER_PORT


def recv_message_and_parse(conn: socket) -> tuple[str, str]:
    """
    the function receives a new message from given socket,
    then parses the message using chatlib
    :param conn: socket object that is used to communicate with the client
    :return: cmd (str) and data (str) of the received message.
             If error occurred, will return None, None
    """
    full_message = conn.recv(MAX_MSG_LENGTH).decode()

    print("[CLIENT] ", full_message)  # debug print

    cmd, data = chatlib.parse_message(full_message)

    return cmd, data


# File Data Loaders:
def load_questions():
    """
    the function loads the questions list from the file database (json file for structured data!)
    (the questions in the file are in an array for scaling and suitability and converted to a dictionary)
    :return: questions dictionary
    """
    try:
        with open("databases/questions.json", "r") as file:
            questions = json.load(file)
            # convert questions json list to dictionary
            questions_dict = {question["id"]: {
                "question": question["question"],
                "answers": question["answers"],
                "correct": question["correct"]} for question in questions}

    # catch a case where the file is not found or empty
    except IOError as ioe:
        questions_dict = {}
        print(f"An I/O error occurred: {ioe}")

    # catch a case where the json file content is not valid
    except json.JSONDecodeError as e:
        questions_dict = {}
        print(f"Error decoding JSON: {e}")

    return questions_dict


def load_user_database():
    """
    the function loads the users dict from the file database (json file for structured data!)
    :return: user dictionary
    """
    try:
        with open("databases/users.json", "r") as file:
            users_dict = json.load(file)

    # catch a case where the file is not found or empty
    except IOError as ioe:
        users_dict = {}
        print(f"An I/O error occurred: {ioe}")

    # catch a case where the json file content is not valid
    except json.JSONDecodeError as e:
        users_dict = {}
        print(f"Error decoding JSON: {e}")

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
