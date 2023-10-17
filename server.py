"""
Author: Ori Boteach
File Name: server
Change Log: creation - 15/10/2023
"""
import random
import socket
import select
import chatlib
from constants import PROTOCOL_CLIENT, ERROR_RETURN, PROTOCOL_SERVER, ERROR_MSG, DATA_DELIMITER
from server_helpers import load_user_database, load_questions, setup_socket, recv_message_and_parse, load_web_questions

# GLOBAL variables
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames
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


def handle_getscore_message(conn: socket, username: str) -> None:
    """
    the function uses the provided socket and username to send the user's score to the client
    :param conn: socket object that is used to communicate with the client
    :param username: a string representing client's username
    """
    user_score = users[username]["score"]
    build_and_send_message(conn, PROTOCOL_SERVER["your_score_msg"], str(user_score))


def handle_highscore_message(conn: socket) -> None:
    """
    the function sends to the client the players score list (from highest to lowest)
    :param conn: socket object that is used to communicate with the client
    """
    # get sorted users, dictionary pairs by their score
    sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)

    # build the message to send to the client
    scores = ""
    for user in sorted_users:
        scores += user[0] + ": " + str(user[1]["score"]) + "\n"

    build_and_send_message(conn, PROTOCOL_SERVER["all_score_msg"], scores)


def handle_logged_message(conn: socket) -> None:
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


def handle_logout_message(conn: socket) -> None:
    """
    the function closes the given socket, in later chapters, it removes the user from logged_users dictionary
    :param conn: socket object that is used to communicate with the client
    """
    global logged_users

    # remove user from logged users and close connection after successful logout
    logged_users.pop(conn.getpeername())
    conn.close()


def validate_login(conn: socket, message_fields: list[str], cmd: str) -> str:
    """
    the function validates the login message from the client
    :param conn: socket object that is used to communicate with the client
    :param message_fields: the fields of the message the client sent
    :param cmd: the command the client sent
    :return: an error message if invalid, nothing otherwise
    """
    # validate the clients login message
    if message_fields == [ERROR_RETURN] or cmd != PROTOCOL_CLIENT["login_msg"]:
        send_error(conn, "error occurred trying to understand your message!")
        return ERROR_MSG

    # check if the user exists
    username = message_fields[0]
    if username not in users:
        send_error(conn, ERROR_MSG + "Username does not exists!")
        return ERROR_MSG

    # check if the password is correct
    password = message_fields[1]
    if password != users[username]["password"]:
        send_error(conn, ERROR_MSG + "Password does not match!")
        return ERROR_MSG


def handle_login_message(conn: socket, data: str) -> None:
    """
    the function gets socket and message data of login message, it checks if the user exists and responds accordingly.
    if invalid - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
    :param conn: socket object that is used to communicate with the client
    :param data: a string representing the data sent by the username according to protocol
    """
    cmd, message = chatlib.parse_message(data)
    message_fields = chatlib.split_data(message, 1)

    # validate the clients login for correct command, username and password
    if validate_login(conn, message_fields, cmd) == ERROR_MSG:
        return

    # successful login
    build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], "")

    # add user's username to logged users after successful login
    logged_users[conn.getpeername()] = message_fields[0]


def create_question(username: str) -> str:
    """
    the function builds a random question (by protocol) from the questions' dictionary
    :return: the random question message field
    """

    # check if the user has been asked all the questions
    if len(users[username]["questions_asked"]) == len(questions):
        return ""

    # get a question the user hasn't been asked yet
    found_question = False
    id, question = random.choice(list(questions.items()))
    while not found_question:
        if id not in users[username]["questions_asked"]:
            found_question = True
        else:
            id, question = random.choice(list(questions.items()))

    # add the question to the user's asked questions
    users[username]["questions_asked"].append(id)

    answers = question["answers"]
    question_message_field = str(id) + DATA_DELIMITER + question["question"] + DATA_DELIMITER + answers[0] \
                             + DATA_DELIMITER + answers[1] + DATA_DELIMITER + answers[2] + DATA_DELIMITER + answers[3]

    return question_message_field


def handle_question_message(conn: socket, username: str) -> None:
    """
    the function sends with provided socket a random question, by protocol, to the client
    :param conn: socket object that is used to communicate with the client
    :param username: a string representing client's username
    """
    question = create_question(username)
    if question == "":  # no more questions to ask
        build_and_send_message(conn, PROTOCOL_SERVER["no_questions_msg"], "")
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["your_question_msg"], question)


def handle_answer_message(conn: socket, data: str) -> None:
    """
    the function checks if the users answer is correct one, responds accordingly and updates the users score
    :param conn: socket object that is used to communicate with the client
    :param data: the message field the user sent with the SEND_ANSWER command
    """
    global users
    split_message = chatlib.split_data(data, 1)

    # validate client's response message field and check for an INTEGER ANSWER
    if split_message == [ERROR_RETURN] or not split_message[1].isdigit():
        send_error(conn, "error occurred trying to understand your message!")
        return

    question_id, user_answer = map(int, split_message[:2])  # apply int() to first two elements of the list
    correct_answer = questions[question_id]["correct"]

    # check if the answer is correct
    if user_answer == correct_answer:
        # update user's score and send correct answer message
        answering_user = logged_users[conn.getpeername()]
        users[answering_user]["score"] += 5
        build_and_send_message(conn, PROTOCOL_SERVER["correct_answer_msg"], "")
    else:  # send wrong answer message
        build_and_send_message(conn, PROTOCOL_SERVER["wrong_answer_msg"], str(correct_answer))


def handle_client_message(conn: socket, cmd: str, data: str) -> None:
    """
    the function gets message code and data and calls the right function to handle command
    :param conn: socket object that is used to communicate with the client
    :param cmd: a string representing the code field in the protocol
    :param data: a string representing the message field in the protocol
    """
    # a dictionary to navigate between the commands and their handlers
    command_handlers = {
        PROTOCOL_CLIENT["logout_msg"]: lambda: handle_logout_message(conn),
        PROTOCOL_CLIENT["my_score_msg"]: lambda: handle_getscore_message(conn, logged_users[conn.getpeername()]),
        PROTOCOL_CLIENT["highscore_msg"]: lambda: handle_highscore_message(conn),
        PROTOCOL_CLIENT["logged_msg"]: lambda: handle_logged_message(conn),
        PROTOCOL_CLIENT["get_question_msg"]: lambda: handle_question_message(conn, logged_users[conn.getpeername()]),
        PROTOCOL_CLIENT["send_answer_msg"]: lambda: handle_answer_message(conn, data),
    }

    # get the full message from the client
    full_message = chatlib.build_message(cmd, data)

    # if user is not logged in
    if conn.getpeername() not in logged_users:
        # handle user login command or send error otherwise
        if cmd == PROTOCOL_CLIENT["login_msg"]:
            handle_login_message(conn, full_message)
        else:
            send_error(conn, "command is not recognized!")
    # if user is logged in
    else:
        # check if the command is recognized and call the corresponding handler
        handler = command_handlers.get(cmd, None)
        if handler:
            handler()
        else:
            send_error(conn, "command is not recognized!")


def print_client_sockets(client_sockets: list[socket]) -> None:
    """
    the function prints the currently connected client sockets
    :param client_sockets: a list of the connected client sockets
    """
    for client in client_sockets:
        print("\t", client.getpeername())


def manage_existing_client(current_socket: socket, client_sockets: list[socket]) -> tuple[socket, list[socket]]:
    """
    the function gets a socket of an existing client and a list of all client sockets and handles the client's message
    :param current_socket: the socket of the client that sent the message
    :param client_sockets: all the connected client sockets
    :return: if needed, the updated sockets list and closed socket
    """
    try:
        # get client message and separate fields
        cmd, data = recv_message_and_parse(current_socket)

        # handle ctrl c (cmd and data are None)
        if cmd is None and data is None:
            logged_users.pop(current_socket.getpeername())
            client_sockets.remove(current_socket)  # remove exiting client from client_sockets list
            current_socket.close()
            print("[SERVER] ", "user has disconnected forcibly, waiting for a new connection")

        elif cmd == PROTOCOL_CLIENT["logout_msg"]:
            handle_client_message(current_socket, cmd, data)  # handle logout message
            client_sockets.remove(current_socket)  # remove exiting client from client_sockets list

            current_socket.close()
            print("[SERVER] ", "user has disconnected, waiting for a new connection")
        # handle client message accordingly
        else:
            handle_client_message(current_socket, cmd, data)

    # handle a case of an existing connection that was forcibly closed by the remote host
    except:
        logged_users.pop(current_socket.getpeername())
        client_sockets.remove(current_socket)  # remove exiting client from client_sockets list
        current_socket.close()
        print("[SERVER] ", "user has disconnected forcibly, waiting for a new connection")

    return current_socket, client_sockets


def main():
    """
    the main function in the server module
    """
    # initializes global users and questions dictionaries using load functions
    global users, questions, logged_users, messages_to_send
    client_sockets = []

    users = load_user_database()
    questions = load_web_questions()

    print("Welcome to Trivia Server!\nStarting up on port 5678")

    # setup server connection
    server_socket = setup_socket()

    while True:
        ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, client_sockets, [])

        for current_socket in ready_to_read:
            # in case a new client tries to connect to the server
            if current_socket is server_socket:
                (client_socket, client_address) = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)

            # an old client needs handling
            else:
                current_socket, client_sockets = manage_existing_client(current_socket, client_sockets)

        # handle messages for ready clients and save for later messages for unready ones
        for message in messages_to_send:
            current_socket, full_message = message
            if current_socket in ready_to_write:
                current_socket.send(full_message)
                messages_to_send.remove(message)


if __name__ == '__main__':
    main()
