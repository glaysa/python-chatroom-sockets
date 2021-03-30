# python-sockets-chatroom

## DATA2410 Assigment:
Create a simple 'chat program' where the clients are bots communicating over raw sockets.

## Description of the program:
- CLI parameters can be passed in
- The clients has 3 commands: `quit`, `reply`, and `debug`
  - `quit`: terminates the connection to the server (client leaves the chatroom)
  - `reply`: makes the bot reply more than once, but they cannot reply to their own messages
  - `debug`: shows how the response of bots are formulated
  
- All bots are created from one bot method
  - The bot method creates a new bot with a given alias
  - This method has a variety of responses making it reusable
  - All bots created from the bot method share the same responses and actions to suggest.
    To make the conversation of the bots flow better, bots does not suggest the same action as the previous bot. 
  - The program has a host that also uses the bot method, but with a different set of messages. The host is the one that initiates the conversation.
 
 ## How the program works:
 - First run `server.py`
 - Then run `client.py`. A bot will automatically connect to the server.
 - When connected, the host will send a message and your bot will reply automatically.
 - You can type in the commands: `quit`, `reply`, and `debug`
 - You can run multiple `client.py` to connect multiple bots.
 - When a new bot connects, they first receeive all past conversation before replying to the latest message
 - When all the connection of the clients are terminated, the server will close automatically.
