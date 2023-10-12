"""
Author: Ori Boteach
File Name: constants
Change Log: creation - 12/10/2023
"""

# Protocol Constants:
CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4  # Exact length of length field (in bytes)

MAX_DATA_LENGTH = 10 ** LENGTH_FIELD_LENGTH - 1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message

DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Other constants:
ERROR_RETURN = None  # What is returned in case of an error

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# Protocol Messages:
# In these dictionaries we will have all the client and server command names
PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT",
    "logged_msg": "LOGGED",
    "get_question_msg": "GET_QUESTION",
    "send_answer_msg": "SEND_ANSWER",
    "my_score_msg": "MY_SCORE",
    "highscore_msg": "HIGHSCORE",
}

PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "logged_answer_msg": "LOGGED_ANSWER",
    "your_question_msg": "YOUR_QUESTION",
    "correct_answer_msg": "CORRECT_ANSWER",
    "wrong_answer_msg": "WRONG_ANSWER",
    "your_score_msg": "YOUR_SCORE",
    "all_score_msg": "ALL_SCORE",
    "login_failed_msg": "ERROR",
    "no_questions_msg": "NO_QUESTIONS"
}
