from cli_parameters import server_parameters
from responses import host_actions
from bots import bot
import threading
import socket
import random
import time
import json
import sys

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
            # Terminate their connection

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

                print(f"Closing server...")
                time.sleep(2)

                print("Server closed!")
                time.sleep(2)

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


# Generates a suggestion
def generate_server_suggestion():
    reaction = ['negative', 'positive', 'neutral']
    return bot('Host', random.choice(host_actions), random.choice(reaction))


# Generates a server suggestion and converted to a json object
server_suggestion = json.dumps(generate_server_suggestion())
# Run accept
accept()
