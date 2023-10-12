"""
Author: Ori Boteach
File Name: client
Change Log: creation - 12/10/2023
"""

import socket
from asyncio.log import logger

import chatlib
from chatlib import *


def build_and_send_message(conn: socket, cmd: str, data: str):
    """
    the function builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    :param conn: socket object that is used to communicate with the server
    :param cmd: the command name
    :param data: the message field
    :return: Nothing
    """

    # building a message by protocol with build_message()
    full_message = build_message(cmd, data)

    # printing full_message as debug information
    logger.debug(full_message)

    # sending the built message to the server
    conn.send(full_message.encode())


def recv_message_and_parse(conn: socket):
    """
    the function receives a new message from given socket,
    then parses the message using chatlib.
    :param conn: socket object that is used to communicate with the server
    :return: cmd (str) and data (str) of the received message.
             If error occurred, will return None, None
    """
    full_message = conn.recv(1024).decode()

    cmd, data = chatlib.parse_message(full_message)
    return cmd, data


def connect() -> socket:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_IP, SERVER_PORT))
    return client_socket


def error_and_exit(error_msg) -> None:
    """
    the function prints the given error message and exits the program (with built-in function - like specified)
    :param error_msg: the provided error message
    """
    print(error_msg)
    exit()  # CHANGE TO EXCEPTION THAT QUITS!!


def login(conn: socket):
    login_successful = False

    while not login_successful:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")

        message_data = username + "#" + password
        build_and_send_message(conn, PROTOCOL_CLIENT["login_msg"], message_data)

        cmd, data = recv_message_and_parse(conn)
        if cmd == PROTOCOL_SERVER["login_ok_msg"]:
            print("Logged in!")
            login_successful = True
        else:
            print("ERROR! username or password does not exist")


def logout(conn: socket):
    build_and_send_message(conn, PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")


def build_send_recv_parse(conn: socket, cmd: str, data: str):
    build_and_send_message(conn, cmd, data)
    msg_code, data = recv_message_and_parse(conn)
    return msg_code, data


def get_score(conn: socket):
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["my_score_msg"], "")

    if msg_code != PROTOCOL_SERVER["your_score_msg"]:
        error_and_exit("ERROR getting your score!")

    print("Your score is: " + data)


def get_highscore(conn: socket):
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["highscore_msg"], "")

    if msg_code != PROTOCOL_SERVER["all_score_msg"]:
        error_and_exit("ERROR getting high score!")

    print("high scores:\n" + data)


def get_logged_users(conn: socket):
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["logged_msg"], "")

    if msg_code != PROTOCOL_SERVER["logged_answer_msg"]:
        error_and_exit("ERROR getting logged users!")

    print("logged users:\n" + data)


def play_question(conn: socket):
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_question_msg"], "")

    # check if there are no more questions
    if msg_code == PROTOCOL_SERVER["no_questions_msg"]:
        error_and_exit("no more questions! GAME OVER!!!")

    if msg_code != PROTOCOL_SERVER["your_question_msg"]:
        error_and_exit("ERROR getting your question!")

    question_fields = split_data(data, 5)  # CONST!!
    question = question_fields[1]
    print("Your question:\n" + question)
    print(f"\t1.{question_fields[2]}\n\t2.{question_fields[3]}\n\t3.{question_fields[4]}\n\t4.{question_fields[5]}")

    user_answer = input("what do you think is the right answer [1-4]? ")
    full_answer = question_fields[0] + "#" + user_answer
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["send_answer_msg"], full_answer)

    if msg_code == PROTOCOL_SERVER["correct_answer_msg"]:
        print("You are right!")

    if msg_code == PROTOCOL_SERVER["wrong_answer_msg"]:
        print(f"You are wrong! the correct answer is #{data}")


def main():
    """
    the main function in this module
    """

    server_connection = connect()
    login(server_connection)

    user_exit = False
    while not user_exit:
        user_input = input("what do you want to do?\n a. logout\n b. see your current score\n"
                           " c. see high scores\n d. play a question\n e. see logged users\n")

        # CHANGE TO BETTER!!
        if user_input.lower() == "a":
            user_exit = True

        elif user_input.lower() == "b":
            get_score(server_connection)

        elif user_input.lower() == "c":
            get_highscore(server_connection)

        elif user_input.lower() == "d":
            play_question(server_connection)

        elif user_input.lower() == "e":
            get_logged_users(server_connection)

    logout(server_connection)
    server_connection.close()


if __name__ == '__main__':
    main()
