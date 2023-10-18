"""
Author: Ori Boteach
File Name: server_data_loaders
Change Log: creation - 17/10/2023
"""
import json
import random
import requests


def load_questions() -> dict:
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


def format_web_question(question: dict, answers: list, correct_answer: str, formatted_questions: list) -> dict:
    """
    The function formats a single question from the web API to the correct structure
    :param question: the question to format
    :param answers: the answers to the question
    :param correct_answer: the correct answer to the question
    :param formatted_questions: the list of already formatted questions
    :return: the formatted question
    """
    question["question"] = question["question"].replace("&quot;", "\"")
    answers = [answer.replace("&quot;", "\"") for answer in answers]
    correct_answer = correct_answer.replace("&quot;", "\"")

    # check if the question or answers contain the '#' character and remove it
    question["question"] = question["question"].replace("#", "")
    answers = [answer.replace("#", "") for answer in answers]
    correct_answer = correct_answer.replace("#", "")

    formatted_question = {
        "id": len(formatted_questions) + 1,
        "question": question["question"],
        "answers": answers,
        "correct": answers.index(correct_answer) + 1  # position of the correct answer
    }

    return formatted_question


def handle_web_question(question: dict, formatted_questions: list) -> list:
    """
    The function handles a single question and adds it to the formatted questions list
    :param question: the current question from the web
    :param formatted_questions: the list of formatted questions
    :return: the new formatted questions list
    """
    # shuffle the answers
    correct_answer = question["correct_answer"]
    incorrect_answers = question["incorrect_answers"]
    answers = [correct_answer] + incorrect_answers
    random.shuffle(answers)

    # format the question
    formatted_question = format_web_question(question, answers, correct_answer, formatted_questions)

    # don't add a question if it contains the '&' character
    if formatted_question["question"].count("&") == 0 and all(
            answer.count("&") == 0 for answer in formatted_question["answers"]):
        formatted_questions.append(formatted_question)

    return formatted_questions


def load_web_questions() -> dict:
    """
    Load questions from the web API and structure them correctly in the questions' dictionary.
    :return: Questions dictionary
    """
    url = 'https://opentdb.com/api.php?amount=50&type=multiple'
    try:
        # get data from the web URL and parse JSON data to a dictionary
        response = requests.get(url)
        response.raise_for_status()  # raise an exception if the request was not successful
        questions_dict = response.json()

        # format the questions to the correct structure
        questions = questions_dict['results']
        formatted_questions = []
        for question in questions:
            formatted_questions = handle_web_question(question, formatted_questions)

        # convert questions list to a dictionary
        formatted_questions_dict = {question["id"]: question for question in formatted_questions}

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        formatted_questions_dict = {}

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        formatted_questions_dict = {}

    return formatted_questions_dict


def load_user_database() -> dict:
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
