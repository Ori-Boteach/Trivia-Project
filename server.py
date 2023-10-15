"""
Author: Ori Boteach
File Name: server
Change Log: creation - 15/10/2023
"""
import random
import socket
import chatlib
from constants import PROTOCOL_CLIENT, ERROR_RETURN, PROTOCOL_SERVER, ERROR_MSG, DATA_DELIMITER
from server_helpers import send_error, build_and_send_message, load_user_database, load_questions, \
    setup_socket, recv_message_and_parse

# GLOBAL variables
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames


# ----------------MESSAGE HANDLING:

def handle_getscore_message(conn: socket, username: str):
    """
    the function uses the provided socket and username to send the user's score to the client
    :param conn: socket object that is used to communicate with the client
    :param username: a string representing client's username
    """
    global users

    user_score = users[username]["score"]
    build_and_send_message(conn, PROTOCOL_SERVER["your_score_msg"], str(user_score))


def handle_highscore_message(conn: socket):
    """
    the function sends to the client the players score list (from highest to lowest)
    :param conn: socket object that is used to communicate with the client
    """
    global users
    # get sorted users, dictionary pairs by their score
    sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)

    # build the message to send to the client
    scores = ""
    for user in sorted_users:
        scores += user[0] + ": " + str(user[1]["score"]) + "\n"

    build_and_send_message(conn, PROTOCOL_SERVER["all_score_msg"], scores)


def handle_logged_message(conn: socket):
    """
    the function sends to the client the players that are currently logged in
    :param conn: socket object that is used to communicate with the client
    """
    global logged_users

    # build the message of current users to send to the client
    logged = ""
    for client_address in logged_users.keys():
        logged += logged_users[client_address] + ", "

    build_and_send_message(conn, PROTOCOL_SERVER["logged_answer_msg"], logged[:-2])


def handle_logout_message(conn: socket):
    """
    the function closes the given socket, in later chapters, it removes the user from logged_users dictionary
    :param conn: socket object that is used to communicate with the client
    """
    global logged_users

    # remove user from logged users after successful logout
    logged_users.pop(conn.getpeername())

    conn.close()


def handle_login_message(conn: socket, data: str) -> None:
    """
    the function gets socket and message data of login message, it checks if the user exists and responds accordingly.
    if invalid - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    :param conn: socket object that is used to communicate with the client
    :param data: a string representing the data sent by the username according to protocol
    """

    global users  # This is needed to access the same users dictionary from all functions
    global logged_users

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
    logged_users[conn.getpeername()] = username


def create_random_question() -> str:
    """
    the function builds a random question (by protocol) from the questions' dictionary
    :return: the random question message field
    """
    global questions
    random_id, random_question = random.choice(list(questions.items()))
    question_message_field = str(random_id) + DATA_DELIMITER + random_question["question"] + DATA_DELIMITER \
                             + random_question["answers"][0] + DATA_DELIMITER + random_question["answers"][1] \
                             + DATA_DELIMITER + random_question["answers"][2] + DATA_DELIMITER + \
                             random_question["answers"][3]

    return question_message_field


def handle_question_message(conn: socket) -> None:
    """
    the function sends with provided socket a random question, by protocol, to the client
    :param conn: socket object that is used to communicate with the client
    """
    build_and_send_message(conn, PROTOCOL_SERVER["your_question_msg"], create_random_question())


def handle_answer_message(conn: socket, data: str) -> None:
    """
    the function checks if the users answer is correct one, responds accordingly and updates the users score
    :param conn: socket object that is used to communicate with the client
    :param data: the message field the user sent with the SEND_ANSWER command
    """
    split_message = chatlib.split_data(data, 1)

    # validate client's response message field
    if split_message == [ERROR_RETURN]:
        send_error(conn, "error occurred trying to understand your message!")
        return

    question_id = int(split_message[0])
    answer = int(split_message[1])

    # check if the answer is correct
    if answer == questions[question_id]["correct"]:
        # update user's score
        answering_user = logged_users[conn.getpeername()]
        users[answering_user]["score"] += 5
        build_and_send_message(conn, PROTOCOL_SERVER["correct_answer_msg"], "")  # send correct answer message
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["wrong_answer_msg"],
                               str(questions[question_id]["correct"]))  # send wrong answer message


def handle_client_message(conn: socket, cmd: str, data: str) -> None:
    """
    the function gets message code and data and calls the right function to handle command
    :param conn: socket object that is used to communicate with the client
    :param cmd: a string representing the code field in the protocol
    :param data: a string representing the message field in the protocol
    """
    global logged_users

    # get the full message from the client
    full_message = chatlib.build_message(cmd, data)

    # if user is not logged in
    if conn.getpeername() not in logged_users:
        # handle user login command
        if cmd == PROTOCOL_CLIENT["login_msg"]:
            handle_login_message(conn, full_message)
        else:
            # send an error message of unrecognized command
            send_error(conn, "command is not recognized!")

    else:  # todo: MAKE BETTER!
        if cmd == PROTOCOL_CLIENT["logout_msg"]:
            handle_logout_message(conn)
        elif cmd == PROTOCOL_CLIENT["my_score_msg"]:
            handle_getscore_message(conn, logged_users[conn.getpeername()])
        elif cmd == PROTOCOL_CLIENT["highscore_msg"]:
            handle_highscore_message(conn)
        elif cmd == PROTOCOL_CLIENT["logged_msg"]:
            handle_logged_message(conn)
        elif cmd == PROTOCOL_CLIENT["get_question_msg"]:
            handle_question_message(conn)
        elif cmd == PROTOCOL_CLIENT["send_answer_msg"]:
            handle_answer_message(conn, data)
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
    global logged_users

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

            # ------handle ctrl c (cmd and data are None)-----
            if cmd is None and data is None:
                logged_users.pop(client_socket.getpeername())
                client_socket.close()
                print("[SERVER] ", "user has disconnected forcibly, waiting for a new connection")

                (client_socket, client_address) = server_socket.accept()
                print("[SERVER] ", "new user has connected")
                continue
            # -----------------------------------------------

            if cmd == PROTOCOL_CLIENT["logout_msg"]:
                # handle logout message
                handle_client_message(client_socket, cmd, data)

                # close logged out socket from server side and wait for another client to login
                client_socket.close()
                print("[SERVER] ", "user has disconnected, waiting for a new connection")

                (client_socket, client_address) = server_socket.accept()
                print("[SERVER] ", "new user has connected")
                continue

            # handle client message accordingly
            handle_client_message(client_socket, cmd, data)

        # handle a case of an existing connection that was forcibly closed by the remote host
        except:
            logged_users.pop(client_socket.getpeername())
            client_socket.close()
            print("[SERVER] ", "user has disconnected forcibly, waiting for a new connection")

            (client_socket, client_address) = server_socket.accept()
            print("[SERVER] ", "new user has connected")


if __name__ == '__main__':
    main()
