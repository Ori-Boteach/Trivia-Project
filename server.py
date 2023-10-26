"""
Author: Ori Boteach
File Name: server
Change Log: creation - 15/10/2023, extensions usage - 17/10/2023
"""
# importing server_menu_handlers module to use its global variables
import server_menu_handlers
import select

# importing server_menu_handlers functions
from server_menu_handlers import *
from server_data_loaders import load_user_database, load_web_questions


def handle_client_message(conn: socket, cmd: str, data: str) -> None:
    """
    the function gets a message code and data and calls the right function to handle the command
    :param conn: socket object that is used to communicate with the client
    :param cmd: a string representing the code field in the protocol
    :param data: a string representing the message field in the protocol
    """
    # a dictionary to navigate between the commands and their handlers
    command_handlers = {
        PROTOCOL_CLIENT["logout_msg"]: lambda: handle_logout_message(conn),
        PROTOCOL_CLIENT["my_score_msg"]: lambda: handle_getscore_message(conn, server_menu_handlers.logged_users[conn.getpeername()]),
        PROTOCOL_CLIENT["highscore_msg"]: lambda: handle_highscore_message(conn),
        PROTOCOL_CLIENT["logged_msg"]: lambda: handle_logged_message(conn),
        PROTOCOL_CLIENT["get_question_msg"]: lambda: handle_question_message(conn, server_menu_handlers.logged_users[conn.getpeername()]),
        PROTOCOL_CLIENT["send_answer_msg"]: lambda: handle_answer_message(conn, data),
    }

    # get the full message from the client
    full_message = build_message(cmd, data)

    # if user is not logged in, handle user login command or send error otherwise
    if conn.getpeername() not in server_menu_handlers.logged_users:
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


def manage_existing_client(current_socket: socket, client_sockets: list[socket]) -> tuple[socket, list[socket]]:
    """
    the function gets a socket of an existing client and a list of all client sockets and handles the client's message
    :param current_socket: the socket of the client that sent the message
    :param client_sockets: all the connected client sockets
    :return: the client socket (closed or not) and the updated sockets list
    """
    try:
        # get client message and separate fields
        cmd, data = recv_message_and_parse(current_socket)

        # handle ctrl c (cmd and data are None)
        if cmd is None and data is None:
            server_menu_handlers.logged_users.pop(current_socket.getpeername())
            client_sockets.remove(current_socket)  # remove exiting client from client_sockets list
            current_socket.close()
            print("[SERVER] ", "user has disconnected forcibly, waiting for a new connection")

        elif cmd == PROTOCOL_CLIENT["logout_msg"]:
            handle_client_message(current_socket, cmd, data)  # handle logout message
            client_sockets.remove(current_socket)
            current_socket.close()
            print("[SERVER] ", "user has disconnected, waiting for a new connection")

        # handle client message accordingly
        else:
            handle_client_message(current_socket, cmd, data)

    # handle a case of an existing connection that was forcibly closed by the remote host
    # a broad exception in order to catch all possible exceptions and prevent the server from crashing
    except:
        server_menu_handlers.logged_users.pop(current_socket.getpeername())
        client_sockets.remove(current_socket)
        current_socket.close()
        print("[SERVER] ", "user has disconnected forcibly, waiting for a new connection")

    return current_socket, client_sockets


def start_server() -> socket:
    """
    the function loads relevant data and starts the server
    :return: the server socket connection
    """
    # load data to the global dictionaries from the imported module
    # *** handling ALL GLOBAL variables in server.py with module prefix for valid usage ***
    server_menu_handlers.users = load_user_database()
    server_menu_handlers.questions = load_web_questions()

    print("Welcome to Trivia Server!\nStarting up on port 5678")

    # setup server connection and return it
    return setup_socket()


def main():
    """
    the main function in the server module
    """
    # start server function - load data and start the server
    server_socket = start_server()
    client_sockets = []

    # check for a valid database load and terminate server if not
    if len(server_menu_handlers.users) == 0 or len(server_menu_handlers.questions) == 0:
        print("Error loading users or questions from database")
        return

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
