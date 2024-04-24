# secure-client-server
A simple client-server system that sets up a TLS connection between client and server to handle employee records.  The server performs user authentication as well as authorization checks and input validation for different requests made by clients.  Clients allow a user to login and prompts them to enter information needed to create a request.

# System rundown
This project consists of a client-side application and a server-side application.  The server-side listens for clients, establishes a TLS connection with them, and then listens for requests for them in a separate thread.  The client-side prompts the user to log into the system, sets up the TLS connection with the server, and then sends a login request with the user's credentials.  If the credentials are valid (match the the user info in database of users), the server creates a new session token for the client that it stores with their permissions (that it grabs from the database).  The client then has a menu of options available to them, which they choose by entering the letter or number corresponding to that action into the command line.  The client-side will prompt the user for the information needed to fulfill the request, and then it is sent to the server.  The server parses the request, ensures it is in the proper formatting and is recognized, and then performs authorization checks to see if the user associated with the connection has the proper permissions to perform that action.  If yes, the server performs input validation to ensure the data is the correct type and then performs the action in the database of employee data, sending a result message of the action back to the client.  If a user lacks proper permissions to do an action or submits a request with invalid input, they will receive an error message from the server corresponding to why the action could not be completed.

# Client-side
## Purpose
Interacting with the server to read, modify, add, or delete employee records.

## Running client
Run the client-side application by entering client_main.py in command line.  

## Using client
User interface for client is entirely based in the command line, with selections and inputs typed into the command line and submitted when the Enter key is pressed.

# Server-side

## Purpose
Handling client connections, parsing/handling requests, input validation, authorization, etc.

## Running server
Run client-side application by entering "server_main.py" in command line.  Note: the server only listens for 1 connection, but is capable of listening for more if server_main.py is modified

# Important info
## Databases
The user.db and employee.db files need to be included in the same file as the server.  If they are not, the application will create new ones in the folder, but they will have no records, so no user can log in to the system and no employee records will exist.  This can be fixed by manually inserting data for users into the user.db database through a UserDatabase object.  From there, employees can be added through the client application, or by adding them by creating and using the methods of an EmployeeDatabase object.

## Certificates
In order for the TLS connection to work, the cert.pem and key.pem files must be included in the same folder as server.py and server_certs.pem needs to be in the same folder as client.py.  These files can be generated using openssl.
Here is a link with instructions on how to do it: https://www.baeldung.com/openssl-self-signed-cert
