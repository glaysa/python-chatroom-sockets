from cli_parameters import client_parameters
from bots import *
import threading
import socket
import random
import json
import time

# Status indicators
stop_thread = False
replied = False

# Dynamic Data
list_of_bots = ['andrea', 'steven', 'arthur']
extracted_actions = []
extracted_reaction = ''
msg_sender = ''

host, port, alias = None, None, None
try:
    # Connection Data
    host = str(client_parameters().get("host"))
    port = int(client_parameters().get("port"))
    alias = str(client_parameters().get("alias"))

    # When given alias is not in the bots list, assign them a random bot
    if alias not in list_of_bots:
        print(f"A bot will be automatically assigned with this alias [{alias}].")

    # Initializing Connection
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

except ValueError as v:
    print("Given parameters are not valid. [host] [port] [bot]")
    print(v)
    stop_thread = True
except ConnectionError as c:
    print(f"Cannot connect to the given address: ({host}: {port})")
    print(c)
    stop_thread = True
except Exception as e:
    print("Something went wrong.")
    print(e)
    stop_thread = True


def generate_bots():
    return random.choice(list_of_bots)


def receive():
    global alias, extracted_actions, replied, stop_thread, extracted_reaction, msg_sender

    while True:
        if stop_thread:
            break

        # Try block used to check if we can still received data from the server,
        # otherwise runs the except block, meaning the server is no longer running

        try:
            incoming_msg = client.recv(1024)

            # Try block used to check if incoming message is a json object or string,
            # if message is string, it runs the except block

            try:
                parsed_msg = json.loads(incoming_msg)
                msg_sender = parsed_msg["sender"]
                msg_content = parsed_msg["message"]
                extracted_actions = parsed_msg["actions"]
                extracted_reaction = parsed_msg["reaction"]

                # Any json object incoming message will be printed
                print(f"> {msg_sender}: {msg_content}")
                print(f"(Expecting a {parsed_msg['reaction']} response)\n")

            # If message is simply a string,
            # they are evaluated and/or printed out

            except:

                # When the server asks for an alias
                if incoming_msg.decode() == 'alias':
                    client.send(alias.encode())

                # When the server says that the alias is already taken
                elif 'taken' in incoming_msg.decode():
                    bot_taken = incoming_msg.decode()[:-6]
                    print(f"Server: [{bot_taken}] is already in use.")
                    if bot_taken in list_of_bots:
                        list_of_bots.remove(bot_taken)
                    print(f"Looking for available bots...")

                    # As long as there are available bots, assign them
                    if list_of_bots:
                        alias = generate_bots()
                        client.send(alias.encode())

                    # If all bots are in use, ask to run a new server or connect with a new alias
                    else:
                        print(f"\nBots on server ({host}: {port}) are all online."
                              f"\nEither connect to a new server or connect with a different alias."
                              f"\nA bot will be automatically assigned.")

                        answer = input('Do you want to connect with a different alias? [y/n]: ')

                        # If user connects with a new alias,
                        # a bot will be assigned automatically with the alias they've given

                        if answer.lower() == 'y':
                            alias = input("Enter an alias: ")
                            client.send(alias.encode())

                        # If user does not want to connect,
                        # Send error to server and the server will terminate the connection

                        elif answer.lower() == 'n':
                            client.send('error'.encode())
                            stop_thread = True

                        # If input is invalid,
                        # Send error to server and the server will terminate the connection

                        else:
                            print('Invalid input')
                            client.send('error'.encode())
                            stop_thread = True

                # The bot can only reply, when all passed conversations are sent
                elif incoming_msg.decode() == 'end of history':
                    if not replied:
                        respond(extracted_reaction)
                        command_thread = threading.Thread(target=client_command)
                        command_thread.start()

                # Any string incoming message will be printed, other than of the above
                else:
                    print(incoming_msg.decode())

        # If server is no longer running, stop receiving thread
        except Exception as err:

            print(f"\nServer is no longer running."
                  f"You can terminate the connection with 'quit' keyword.")
            print(err)
            stop_thread = True
            client.close()


def respond(reaction):
    global replied

    while not replied:

        # Shows that the bot is formulating a reply
        print(f"\t[Actions found from previous reply: {extracted_actions} ]")
        print(f"\t[(Your bot is formulating a {reaction} response...)]\n")
        time.sleep(2)

        response = bot(alias, extracted_actions, reaction)
        bot_response = json.dumps(response)
        client.send(bot_response.encode())
        replied = True


def client_command():
    global stop_thread, replied

    # A bot can terminate connection to server with the keyword quit
    while True:
        if stop_thread:
            break

        try:
            command = input('').lower()
            if command == 'quit':
                client.send(f'quit {alias}'.encode())
                stop_thread = True
                break
            elif command == 'reply':
                '''if msg_sender == alias:
                    print(f"\t[You can't reply to your own message.]\n")
                    continue
                else:'''
                replied = False
                respond(extracted_reaction)
            else:
                print(f"Commands: \n"
                      f"quit: \t terminate connection to server\n"
                      f"reply: \t make the bot reply to the previous response")
        except:
            stop_thread = True
            client.close()
            break


receive_thread = threading.Thread(target=receive)
receive_thread.setName('Receive Thread')
receive_thread.start()
