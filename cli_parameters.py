import getopt
import random
import sys

''' This file handles all cli parameters. '''

# Default param values
default_host = 'localhost'
default_port = 4242
default_bots = ['andrea', 'steven', 'arthur']

# Initial alias
alias = random.choice(default_bots)

client_help_docs = """
-h \t --help        \t shows all command options
-l \t --list_bots   \t shows all bots that can be used


Default Connection Data:
- Default Host: \t 'localhost'
- Default Port: \t 4242
- Default Bot:  \t Random bot from the bot array
    

Change connection data by passing in parameters such as:
-i \t --ip   \t requires an IP address [-i 127.0.0.1]
-p \t --port \t requires a Port number [-p 4242]
-b \t --bot  \t requires a bot name as [-b edward]


Alternatively: Parameters can be passed in with no options like so: 
- client.py [host] [port] [bot]


Bot commands:
[quit]          \t Terminate connection to server
[reply]         \t Make the bot reply to previous message
[debug on/off]  \t enables and disables bot debug mode
"""


server_help_docs = """
-h \t --help \t shows all command options
-p \t --port \t requires a Port number [-p 4242]

Alternatively: Parameters can be passed in with no [options] given like so:
- server.py [port]
- For example: \t server.py 4242
"""


def client_parameters():
    global default_host, default_port, alias

    argument_list = sys.argv[1:]

    if len(argument_list) < 3:

        opt_short = "hli:p:b:"
        opt_long = ["help", "list_bots", "ip=", "port=", "bot="]

        try:
            arguments, values = getopt.getopt(argument_list, opt_short, opt_long)
        except getopt.error as e:
            print(str(e))
            sys.exit(2)

        for curr_arg, curr_val in arguments:
            if curr_arg in ("-h", "--help"):
                print(client_help_docs)
                sys.exit(2)
            elif curr_arg in ("-l", "--list_bots"):
                print(f"Bots: {default_bots}")
                sys.exit(2)
            elif curr_arg in ("-i", "--ip"):
                default_host = str(curr_val)
            elif curr_arg in ("-p", "--port"):
                default_port = int(curr_val)
            elif curr_arg in ("-b", "--bot"):
                alias = str(curr_val)

        return {"host": default_host, "port": default_port, "alias": alias}

    elif len(argument_list) == 3:
        return {"host": sys.argv[1], "port": sys.argv[2], "alias": sys.argv[3]}
    else:
        print(f"\nParameters not recognized.\n"
              f"{client_help_docs}")
        sys.exit(2)


def server_parameters():
    global default_port

    argument_list = sys.argv[1:]

    if len(argument_list) == 1:
        return {"host": default_host, "port": sys.argv[1]}
    if len(argument_list) > 1:
        print(f"\nParameters not recognized.\n"
              f"{server_help_docs}")
        sys.exit(2)
    else:

        opt_short = "hp:"
        opt_long = ["help", "port="]

        try:
            arguments, values = getopt.getopt(argument_list, opt_short, opt_long)
        except getopt.error as e:
            print(str(e))
            sys.exit(2)

        for curr_arg, curr_val in arguments:
            if curr_arg in ("-h", "--help"):
                print(server_help_docs)
                sys.exit(2)
            elif curr_arg in ("-p", "--port"):
                default_port = int(curr_val)

        return {"host": default_host, "port": default_port}
