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


def load_web_questions() -> dict:
    """
    the function loads questions from the web api and structures them correctly in the questions' dictionary
    :return: questions dictionary
    """
    url = 'https://opentdb.com/api.php?amount=50&type=multiple'
    try:
        # get data from web url and parse json data to dict
        response = requests.get(url)
        response.raise_for_status()  # raise an exception if the request was not successful
        questions_dict = response.json()

        # format the questions to the correct structure
        questions = questions_dict['results']
        formatted_questions = []
        for question in questions:

            # shuffle the answers
            correct_answer = question["correct_answer"]
            incorrect_answers = question["incorrect_answers"]
            answers = [correct_answer] + incorrect_answers
            random.shuffle(answers)

            # check if the question or answers contain the '#' character and rewrite ''
            if question["question"].count("#") > 0 or answers.count("#") > 0:
                continue
            question["question"] = question["question"].replace("&quot;", "\"")
            answers = [answer.replace("&quot;", "\"") for answer in answers]
            correct_answer = correct_answer.replace("&quot;", "\"")

            formatted_question = {
                "id": len(formatted_questions) + 1,
                "question": question["question"],
                "answers": answers,
                "correct": answers.index(correct_answer) + 1  # Position of the correct answer
            }
            formatted_questions.append(formatted_question)

        # convert questions list to dictionary
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
