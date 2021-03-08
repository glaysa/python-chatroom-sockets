from cli_parameters import server_parameters
from bots import grammar_fixer
import threading
import socket
import random
import time
import json
import sys
import re

try:
    # Connection Data
    host = str(server_parameters().get("host"))
    port = int(server_parameters().get("port"))

    # Initializing Connection
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Server is running on ({host}: {port})")

except ValueError as v:
    print("Given parameters are not valid.")
    print(v)
    sys.exit(2)
except ConnectionError as c:
    print("Cannot connect to the given address.")
    print(c)
    sys.exit(2)
except Exception as e:
    print("Something went wrong.")
    print(e)
    sys.exit(2)

# Dynamic Data
aliases = []
clients = []
history = []


def receive(client):
    while True:

        try:

            message = client.recv(1024)

            # When clients send a message with the keyword quit
            # They are disconnected from the server

            if 'quit' in message.decode():
                client_to_quit = message.decode()[5:]
                if client_to_quit in aliases:
                    index = aliases.index(client_to_quit)
                    client_quitting = clients[index]
                    client_quitting.close()
                    continue

            # A message from one client will be sent to all the other clients
            # These messages are stored in an array as bytes
            # With this, newly connected clients will be able to read past conversations

            else:
                history.append(message)
                broadcast(message, None)

        except:

            # If the client disconnects, remove them from the clients array
            index = clients.index(client)
            clients.remove(client)
            client.close()

            # Sends feedback to other clients that a client has left the chat room
            alias = aliases[index]
            broadcast_msg = f"({get_time()}) - [{alias}] left the chat!"
            broadcast(broadcast_msg.encode(), None)
            history.append(broadcast_msg.encode())
            print(f"\n[{alias}] terminated the connection!")
            aliases.remove(alias)

            # If all clients disconnects, close the server
            if not clients:
                print("\nAll clients has been disconnected.")
                print("Server closed!")
                server.close()

            break


def accept():
    while True:

        try:

            # Accept Connections
            client, address = server.accept()
            print(f"\nA connection to {address} has been established.")

            # Request and store an alias
            client.send('alias'.encode())
            alias = client.recv(1024).decode()

            # Request a new alias if the given alias is already taken
            while alias in aliases:
                client.send(f"{alias} taken".encode())
                alias = client.recv(1024).decode()
                if alias not in aliases:
                    break
                elif alias == 'error':
                    break

            # Terminates connection to invalid clients
            if alias == 'error' or not alias:
                print(f"The Connection to {address} has been terminated.")
                client.close()
                continue

            # Adds valid clients to the following lists
            else:
                aliases.append(alias)
                clients.append(client)

            # Displays connection feedback to the server and the new client
            print(f"The client at {address} connected to the server with the alias [{alias}].")
            client.send(f"\nYou are now online with the alias [{alias}].\n".encode())
            time.sleep(.5)

            # Send a suggestion
            client.send(server_suggestion.encode())
            time.sleep(.5)

            # Send connection feedback to other clients
            connection_msg = f"({get_time()}) - [{alias}] joined the chat!".encode()
            broadcast(connection_msg, client)

            # Send past conversations to newly connected clients
            send_history(client)
            time.sleep(.5)

            client.send('end of history'.encode())
            history.append(connection_msg)

            # Handles every clients' message on a thread
            receive_thread = threading.Thread(target=receive, args=(client,))
            receive_thread.setName('Receive Thread')
            receive_thread.start()

        except:

            # If something goes wrong, break the loop
            break


# Sends the past conversations of other clients
def send_history(client):
    for conversation in history:
        client.send(conversation)
        time.sleep(.5)


# Sends messages from one client to all the other clients
def broadcast(message, client_to_skip):
    for client in clients:
        if client == client_to_skip:
            continue
        client.send(message)


# Returns current time
def get_time():
    return time.strftime("%H:%M", time.localtime())


# Server action choices
server_choices = ['eat', 'cook', 'fight', 'paint', 'complain', 'swim@d', 'party', 'camp', 'jog@d', 'dive', 'craft']
# Server chosen actions
server_actions = []
# Placeholder
suggestion_char = wtr = '@'


# Generates a suggestion
def generate_server_suggestion():
    reaction = ['negative', 'positive', 'neutral']

    # Dynamic Host names
    hosts = ['Troublemaker Friend', 'Hyper Friend', 'Sassy Friend', 'Grumpy Friend', 'Sweet Friend']

    # Dynamic suggestions
    suggestion = random.choice([
        f"Wanna {wtr} or {wtr}, maybe {wtr}? Anything's fine ... just pick and save me from boredom!",
        f"Hey! I'm free this weekend, wanna {wtr} and {wtr}? Invite the others.",
        f"This is out out of nowhere, but wanna {wtr}?",
        f"I heard {wtr} and {wtr} can deepen our friendship. You guys up for it?",
        f"No matter what you guys say, you're coming. We're gonna {wtr} together!"])

    counter = count(suggestion, wtr)
    suggestion = replace_placeholder(suggestion, counter)

    return {"sender": random.choice(hosts),
            "message": suggestion,
            "actions": server_actions,
            "reaction": random.choice(reaction)}


# Generates a random action
def generate_actions():
    action = server_choices.pop(random.choice(range(len(server_choices))))
    if action not in server_choices:
        server_actions.append(action)
    return action


# replaces the placeholder with random actions
def replace_placeholder(sentence, limit):
    for i in range(limit):
        action = generate_actions()
        sentence = re.sub(wtr, action, sentence, 1)
        sentence = grammar_fixer(sentence, action)
    return sentence


# Counds the number of placeholders needed to be replaced
def count(text, word_to_replace):
    counter = 0
    for _ in re.finditer(word_to_replace, text):
        counter += 1
    return counter

# Generates a server suggestion and converted to a json object
server_suggestion = json.dumps(generate_server_suggestion())
# Run accept
accept()
