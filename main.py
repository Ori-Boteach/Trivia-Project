from chatlib import split_data, join_data, build_message, parse_message

if __name__ == '__main__':
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

