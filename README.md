# secure-client-server
A simple client-server application that sets up a TLS connection between client and server to handle employee records.  Server performs user authentication as well as authorization checks and input validation for different requests made by clients.

# Client-side
## Purpose
Interacting with the server to read, modify, add, or delete employee records.

## Running client
Run client-side application by entering client_main.py in command line.  

## Using client
User interface for client is entirely based in the command line, with selections and inputs typed into the command line and submitted when the Enter key is pressed.

# Server-side

## Purpose
Handling client connections, parsing/handling requests, input validation, authorization, etc.

## Running server
Run client-side application by entering "server_main.py" in command line.  (
Note, the server only listens for 1 connection, but is capable of listeneing for more if serer_main.py is modified)

##
