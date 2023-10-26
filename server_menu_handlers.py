"""
Author: Ori Boteach
File Name: server_menu_handlers
Change Log: creation - 25/10/2023
"""
import random
from chatlib import split_data
from server_helpers import *

# GLOBAL variables:
users = {}
questions = {}
logged_users = {}  # a dictionary of client hostnames to usernames


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
    # get sorted users dictionary pairs by their score
    sorted_users = sorted(users.items(), key=lambda x: x[1]["score"], reverse=True)

    # build the message and send to the client
    scores = ""
    for user in sorted_users:
        scores += user[0] + ": " + str(user[1]["score"]) + "\n"

    build_and_send_message(conn, PROTOCOL_SERVER["all_score_msg"], scores)


def handle_logged_message(conn: socket) -> None:
    """
    the function sends to the client the players that are currently logged in
    :param conn: socket object that is used to communicate with the client
    """
    logged = ""
    for client_address in logged_users.keys():
        logged += logged_users[client_address] + ", "

    build_and_send_message(conn, PROTOCOL_SERVER["logged_answer_msg"], logged[:-2])


def handle_logout_message(conn: socket) -> None:
    """
    the function closes the given socket and removes the user from logged_users dictionary
    :param conn: socket object that is used to communicate with the client
    """
    global logged_users  # declaring the global variable when modifying it

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
    the function gets a socket and a login message, it checks if the user exists and responds accordingly.
    if invalid - sends an error. If all ok, sends OK message and adds the user to logged_users
    :param conn: socket object that is used to communicate with the client
    :param data: a string representing the data sent by the username according to protocol
    """
    cmd, message = parse_message(data)
    message_fields = split_data(message, 1)

    # validate the clients login for correct command, username and password
    if validate_login(conn, message_fields, cmd) == ERROR_MSG:
        return

    # send successful login message and add user's username to logged users
    build_and_send_message(conn, PROTOCOL_SERVER["login_ok_msg"], "")
    logged_users[conn.getpeername()] = message_fields[0]


def return_unseen_questions(username: str) -> tuple[int, dict]:
    """
    the function returns a random question that the user hasn't been asked yet
    :param username: the username of the asking client
    :return: question id and dictionary
    """
    found_question = False
    id, question = random.choice(list(questions.items()))
    while not found_question:
        if id not in users[username]["questions_asked"]:
            found_question = True
        else:
            id, question = random.choice(list(questions.items()))

    return id, question


def create_question(username: str) -> str:
    """
    the function builds a random question (by protocol) from the questions' dictionary
    :return: the random question message field
    """
    # check if the user has been asked all the questions
    if len(users[username]["questions_asked"]) == len(questions):
        return ""

    # get a question the user hasn't been asked yet
    id, question = return_unseen_questions(username)

    # add the question to the user's asked questions and return it
    users[username]["questions_asked"].append(id)

    answers = question["answers"]
    question_message_field = str(id) + DATA_DELIMITER + question["question"] + DATA_DELIMITER + answers[0] \
                             + DATA_DELIMITER + answers[1] + DATA_DELIMITER + answers[2] + DATA_DELIMITER + answers[3]

    return question_message_field


def handle_question_message(conn: socket, username: str) -> None:
    """
    the function sends with the provided socket a random question to the client, by protocol
    :param conn: socket object that is used to communicate with the client
    :param username: a string representing client's username
    """
    question = create_question(username)
    if question == "":  # no more questions to ask
        build_and_send_message(conn, PROTOCOL_SERVER["no_questions_msg"], "")
    else:
        build_and_send_message(conn, PROTOCOL_SERVER["your_question_msg"], question)


def return_answer_response(conn, user_answer: str, correct_answer: str) -> None:
    """
    the function checks if the users answer is correct, responds accordingly and updates the users score if needed
    :param conn: socket object that is used to communicate with the client
    :param user_answer: the users answer to the question
    :param correct_answer: the correct answer to the question
    """
    global users  # declaring the global variable when modifying it

    if user_answer == correct_answer:
        # update user's score and send correct answer message
        answering_user = logged_users[conn.getpeername()]
        users[answering_user]["score"] += 5
        build_and_send_message(conn, PROTOCOL_SERVER["correct_answer_msg"], "")

    else:  # send wrong answer message
        build_and_send_message(conn, PROTOCOL_SERVER["wrong_answer_msg"], correct_answer)


def handle_answer_message(conn: socket, data: str) -> None:
    """
    the function checks if the users answer is correct one, responds accordingly and updates the users score
    :param conn: socket object that is used to communicate with the client
    :param data: the message field the user sent with the SEND_ANSWER command
    """
    split_message = split_data(data, 1)

    # validate client's response message field
    if split_message == [ERROR_RETURN]:
        send_error(conn, "error occurred trying to understand your message!")
        return

    question_id = int(split_message[0])
    user_answer = split_message[1]
    correct_answer = str(questions[question_id]["correct"])

    # check if the answer is correct and respond accordingly
    return_answer_response(conn, user_answer, correct_answer)
