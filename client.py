"""
Author: Ori Boteach
File Name: client
Change Log: creation - 12/10/2023
"""
import socket
from chatlib import split_data
from client_helpers import build_send_recv_parse, error_and_exit, connect, login, logout
from constants import PROTOCOL_SERVER, PROTOCOL_CLIENT, QUESTION_FIELDS_NUMBER


def get_score(conn: socket) -> None:
    """
    the function gets and prints the user's score
    :param conn: socket object that is used to communicate with the server
    """
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["my_score_msg"], "")

    # validate that the received command from server is as expected
    if msg_code != PROTOCOL_SERVER["your_score_msg"]:
        error_and_exit("ERROR getting your score!")

    print("Your score is: " + data)


def get_highscore(conn: socket) -> None:
    """
    the function gets and prints the high score list
    :param conn: socket object that is used to communicate with the server
    """
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["highscore_msg"], "")

    # validate that the received command from server is as expected
    if msg_code != PROTOCOL_SERVER["all_score_msg"]:
        error_and_exit("ERROR getting high score!")

    print("high scores:\n" + data)


def get_logged_users(conn: socket) -> None:
    """
    the function gets and prints the currently logged users
    :param conn: socket object that is used to communicate with the server
    """
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["logged_msg"], "")

    # validate that the received command from server is as expected
    if msg_code != PROTOCOL_SERVER["logged_answer_msg"]:
        error_and_exit("ERROR getting logged users!")

    print("logged users:\n" + data)


def play_question_validation(msg_code: str) -> None:
    """
    the function checks if there are no more questions or if there was an error in the response
    :param msg_code: the returned message command
    """
    # check for a case where there are no more questions left
    if msg_code == PROTOCOL_SERVER["no_questions_msg"]:
        error_and_exit("no more questions! GAME OVER!!!")

    # validate that the received command from server is as expected
    if msg_code != PROTOCOL_SERVER["your_question_msg"]:
        error_and_exit("ERROR getting your question!")


def print_question(data: str) -> list[str]:
    """
    the function prints the trivia question
    :param data: the question data from the server
    :return: the different parts of the question
    """
    question_fields = split_data(data, QUESTION_FIELDS_NUMBER)
    question = question_fields[1]

    print("Your question:\n" + question)
    print(f"\t1.{question_fields[2]}\n\t2.{question_fields[3]}\n\t3.{question_fields[4]}\n\t4.{question_fields[5]}")

    return question_fields


def send_user_answer(conn, question_fields) -> bool:
    """
    the function send user's answer and print a correlating response
    :param conn: socket object that is used to communicate with the server
    :param question_fields: the different parts of the question
    :return: True if the user's answer was correct, False otherwise -> ONLY for testing
    """
    user_answer = input("what do you think is the right answer [1-4]? ")
    full_answer = question_fields[0] + "#" + user_answer
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["send_answer_msg"], full_answer)

    if msg_code == PROTOCOL_SERVER["correct_answer_msg"]:
        print("You are right!")
        return True

    if msg_code == PROTOCOL_SERVER["wrong_answer_msg"]:
        print(f"You are wrong! the correct answer is #{data}")
        return False


def play_question(conn: socket) -> bool:
    """
    the function lets the user answer a question, shows correct answer if wrong and updates score if not
    :param conn: socket object that is used to communicate with the server
    :return: True if the user's answer was correct, False otherwise -> for testing
    """
    # get the trivia question from the server
    msg_code, data = build_send_recv_parse(conn, PROTOCOL_CLIENT["get_question_msg"], "")

    # check if there are no more questions
    play_question_validation(msg_code)

    question_fields = print_question(data)

    return send_user_answer(conn, question_fields)


def manage_game() -> None:
    """
    the function manages the game, gets user input and calls the relevant functions
    raises an exception if there was a problem with the connection to the server or a keyboard interrupt
    """
    try:
        server_connection = connect()
        login(server_connection)

        menu_options = {
            'b': lambda: get_score(server_connection),
            'c': lambda: get_highscore(server_connection),
            'd': lambda: play_question(server_connection),
            'e': lambda: get_logged_users(server_connection)
        }

        user_exit = False
        while not user_exit:
            user_input = input("what do you want to do?\n a. logout\n b. see your current score\n"
                               " c. see high scores\n d. play a question\n e. see logged users\n").lower()
            # if user chose to exit
            if user_input.lower() == "a":
                user_exit = True
            elif user_input in menu_options:
                menu_options[user_input]()
            else:
                print("Invalid choice! Please choose a valid option")

        logout(server_connection)
        server_connection.close()

    except KeyboardInterrupt:
        error_and_exit("you have exited the game! please come back soon!")
    # using a general exception to catch all possible errors and prevent the client from crashing without explanation
    except Exception as e:
        error_and_exit("there was a problem with the connection to the server, please try again:\n" + str(e))


def main():
    """
    the main function in the client module
    """
    manage_game()


if __name__ == '__main__':
    main()
