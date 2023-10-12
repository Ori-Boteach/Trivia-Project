"""
Author: Ori Boteach
File Name: main
Change Log: creation - 12/10/2023
"""

from chatlib import split_data, join_data, build_message, parse_message


def run_initial_tests():
    """
    a function that runs basic tests on the functions it the chatlib module
    """
    answer = split_data("username#password", 1)
    print(answer)

    ans = join_data(["question", "ans1", "ans2", "ans3", "ans4", "correct"])
    print(ans)

    ans = build_message("LOGIN", "aaaa#bbbb")
    print(ans)
    ans = build_message("LOGIN", "aaaabbbb")
    print(ans)
    ans = build_message("LOGIN", "")
    print(ans)
    ans = build_message("0123456789ABCDEFGH", "")
    print(ans)

    ans = parse_message("LOGIN           |   9|aaaa#bbbb")
    print(ans)
    ans = parse_message("LOGIN           |0009|aaaa#bbbb")
    print(ans)
    ans = parse_message("LOGIN           $   9|aaaa#bbbb")
    print(ans)
    ans = parse_message("LOGIN           |   z|aaaa#bbbb")
    print(ans)


def main():
    """
    the main function in the project
    """
    run_initial_tests()


if __name__ == '__main__':
    main()
