"""
Author: Ori Boteach
File Name: server_helpers
Change Log: creation - 15/10/2023
"""
import socket
import chatlib
from constants import MAX_MSG_LENGTH, SERVER_IP, SERVER_PORT, PROTOCOL_SERVER

messages_to_send = []  # a list of messages to send to clients


def build_and_send_message(conn: socket, cmd: str, msg: str) -> None:
    """
    the function builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket
    :param conn: socket object that is used to communicate with the client
    :param cmd: the command name
    :param msg: the message field
    """
    global messages_to_send

    # building a message by protocol with build_message()
    full_message = chatlib.build_message(cmd, msg)
    print("[SERVER] ", full_message)

    # add outgoing message to messages_to_send list
    messages_to_send.append((conn, full_message.encode()))


def send_error(conn: socket, error_msg: str) -> None:
    """
    the function sends an error response with the given message
    :param conn: socket object that is used to communicate with the client
    :param error_msg: a string representing the error
    """
    build_and_send_message(conn, PROTOCOL_SERVER["login_failed_msg"], error_msg)


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


def print_client_sockets(client_sockets: list[socket]) -> None:
    """
    the function prints the currently connected client sockets
    :param client_sockets: a list of the connected client sockets
    """
    for client in client_sockets:
        print("\t", client.getpeername())


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
