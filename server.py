"""
Author: Ori Boteach
File Name: server
Change Log: creation - 15/10/2023
"""

import socket
import chatlib
from constants import PROTOCOL_CLIENT, ERROR_RETURN, SERVER_PORT, PROTOCOL_SERVER, MAX_MSG_LENGTH, SERVER_IP, ERROR_MSG

# GLOBAL variables
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames


# --------------------------------HELPER SOCKET METHODS:

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


# ----------------MESSAGE HANDLING:

def handle_getscore_message(conn: socket, username: str):
    """
    the function COMPLETE
    :param conn: socket object that is used to communicate with the client
    :param username: a string representing client's username
    """

    global users

    # Implement this in later chapters


def handle_logout_message(conn: socket):
    """
    the function closes the given socket, in later chapters, it removes the user from logged_users dictionary
    :param conn: socket object that is used to communicate with the client
    """

    global logged_users

    conn.close()
    logged_users.pop(conn.getpeername())


def handle_login_message(conn: socket, data: str) -> None:
    """
    the function gets socket and message data of login message, it checks if the user exists and responds accordingly.
    if invalid - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    :param conn: socket object that is used to communicate with the client
    :param data: a string representing the data sent by the username according to protocol
    """

    global users  # This is needed to access the same users dictionary from all functions
    global logged_users  # To be used later

    cmd, message = chatlib.parse_message(data)
    message_fields = chatlib.split_data(message, 1)

    # validate the clients login message
    if message_fields == [ERROR_RETURN] or cmd != PROTOCOL_CLIENT["login_msg"]:
        send_error(conn, "error occurred trying to understand your message!")
        return

    # check if the user exists
    username = message_fields[0]
    if username not in users:
        send_error(conn, ERROR_MSG + "Username does not exists!")
        return

    # check if the password is correct
    password = message_fields[1]
    if password != users[username]["password"]:
        send_error(conn, ERROR_MSG + "Password does not match!")
        return

    # successful login
    build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], "")

    # add user to logged users after successful login
    # logged_users[conn.getpeername()] = username


def handle_client_message(conn: socket, cmd: str, data: str) -> None:
    """
    the function gets message code and data and calls the right function to handle command
    :param conn: socket object that is used to communicate with the client
    :param cmd: a string representing the code field in the protocol
    :param data: a string representing the message field in the protocol
    """

    global logged_users  # To be used later

    full_message = chatlib.build_message(cmd, data)

    # handle user login command
    if cmd == PROTOCOL_CLIENT["login_msg"]:
        handle_login_message(conn, full_message)

    elif cmd == PROTOCOL_CLIENT["logout_msg"]:
        handle_logout_message(conn)
    else:
        # send an error message of unrecognized command
        send_error(conn, "command is not recognized!")


def main():
    """
    the main function in the server module
    """

    # Initializes global users and questions dictionaries using load functions, will be used later
    global users
    global questions

    users = load_user_database()
    questions = load_questions()

    print("Welcome to Trivia Server!")
    print("starting up on port 5678")

    # setup server connection
    server_socket = setup_socket()
    (client_socket, client_address) = server_socket.accept()
    print("[SERVER] ", "new user has connected")

    while True:
        try:
            # get client message and separate fields
            cmd, data = recv_message_and_parse(client_socket)

            if cmd == PROTOCOL_CLIENT["logout_msg"]:
                # handle logout message
                handle_client_message(client_socket, cmd, data)

                # close logged out socket from server side and wait for another client to login
                client_socket.close()
                print("[SERVER] ", "user has disconnected, waiting for a new connection")

                (client_socket, client_address) = server_socket.accept()
                print("[SERVER] ", "new user has connected")

            # handle client message accordingly
            handle_client_message(client_socket, cmd, data)

        # handle a case of an existing connection that was forcibly closed by the remote host (cmd and data are None)
        except:
            client_socket.close()
            print("[SERVER] ", "user has disconnected, waiting for a new connection")

            (client_socket, client_address) = server_socket.accept()
            print("[SERVER] ", "new user has connected")


if __name__ == '__main__':
    main()
