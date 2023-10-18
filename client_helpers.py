"""
Author: Ori Boteach
File Name: client_helpers
Change Log: creation - 12/10/2023
"""
import socket
from asyncio.log import logger
from chatlib import build_message, parse_message
from constants import CLIENT_IP, SERVER_PORT, PROTOCOL_CLIENT, PROTOCOL_SERVER


def build_and_send_message(conn: socket, cmd: str, data: str) -> None:
    """
    the function builds a new message with given command and message.
    prints debug info and sends it to the given socket
    :param conn: socket object that is used to communicate with the server
    :param cmd: the command name
    :param data: the message field
    :return: Nothing
    """
    # building a message by protocol with build_message()
    full_message = build_message(cmd, data)

    # printing full_message as debug information, course requirement!
    logger.debug(full_message)

    # sending the built message to the server
    conn.send(full_message.encode())


def recv_message_and_parse(conn: socket) -> tuple[str, str]:
    """
    the function receives a new message from given socket, then parses the message using chatlib
    :param conn: socket object that is used to communicate with the server
    :return: the command and data fields of the received message.
             If error occurred, will return None, None
    """
    full_message = conn.recv(1024).decode()

    return parse_message(full_message)


def build_send_recv_parse(conn: socket, cmd: str, data: str) -> tuple[str, str]:
    """
    the function sends a message to the server by the known protocol and returns the answer
    :param conn: socket object that is used to communicate with the server
    :param cmd: the command of the message
    :param data: the data of the message
    :return: the answer from the server (command and data)
    """
    build_and_send_message(conn, cmd, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data


def connect() -> socket:
    """
    the function connects to a server with a specified ip and port
    :return: the connection between the server and the client
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((CLIENT_IP, SERVER_PORT))
    return client_socket


def error_and_exit(error_msg: str) -> None:
    """
    the function prints the given error message and exits the program
    (SPECIFIED TO DO WITH exit()!)
    :param error_msg: the provided error message
    """
    print(error_msg)
    exit()


def login(conn: socket) -> None:
    """
    the function receives a username and password from the user and tries to
    log in to the server until success
    :param conn: socket object that is used to communicate with the server
    :return: prints an indicative message
    """
    login_successful = False

    while not login_successful:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")

        # try to log in with the provided username and password
        message_data = username + "#" + password
        build_and_send_message(conn, PROTOCOL_CLIENT["login_msg"], message_data)

        # check if the login was successful and act accordingly
        cmd, data = recv_message_and_parse(conn)
        if cmd == PROTOCOL_SERVER["login_ok_msg"]:
            print("Logged in!")
            login_successful = True
        else:
            print("ERROR! username or password does not exist")


def logout(conn: socket) -> None:
    """
    the function logs out the client from the server
    :param conn: socket object that is used to communicate with the server
    """
    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")
