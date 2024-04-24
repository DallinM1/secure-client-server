from database import EmployeeDatabase, UserDatabase
from authorization import Authorization
from secrets import token_urlsafe

class RequestManager:
    '''
    Class for managing requests and calling the appropriate methods to handle the requests
    '''
    def __init__(self):
        self.employee_db = EmployeeDatabase()
        self.sessions = {}
        self.authorizer = Authorization()

    def parse_request(self, request, conn):
        '''
        Parses the request and calls the appropriate method to handle the request
        '''
        header_body = request.split("//")
        if len(header_body) != 2:
            conn.send("Invalid Request".encode("utf-8"))
            return
        request_parts = header_body[1].split(': ')
        if len(request_parts) != 2:
            conn.send("Invalid Request".encode("utf-8"))
            return
        if request_parts[0] == "logon":
            self.logon(request_parts[1], conn)
            return
        elif request_parts[0] == "get":
            if header_body[0] in self.sessions:
                if self.authorizer.check_permissions(self.sessions[header_body[0]][1], "get"):
                    try:
                        response = str(self.employee_db.get(request_parts[1]))
                        conn.send(response.encode("utf-8"))
                    except ValueError as e:
                        conn.send(str(e).encode("utf-8"))
                    return
            conn.send("Invalid permissions".encode("utf-8"))
        elif request_parts[0] == "update":
            if header_body[0] in self.sessions:
                if self.authorizer.check_permissions(self.sessions[header_body[0]][1], "update"):
                    try:
                        employee = self.parse_employee(request_parts[1])
                    except ValueError as e:
                        conn.send(str(e).encode("utf-8"))
                        return
                    try:
                        self.employee_db.update(employee[0], employee[1], employee[2], employee[3], employee[4], employee[5])
                        response = f"Employee #{employee[0]} successfully updated"
                        conn.send(response.encode("utf-8"))
                    except ValueError as e:
                        conn.send(str(e).encode("utf-8"))
                    return 
            conn.send("Invalid permissions".encode("utf-8"))
        elif request_parts[0] == "add":
            if header_body[0] in self.sessions:
                if self.authorizer.check_permissions(self.sessions[header_body[0]][1], "add"):
                    try:
                        employee = self.parse_employee(request_parts[1])
                        self.employee_db.add(employee[0], employee[1], employee[2], employee[3], employee[4], employee[5])
                        response = f"Employee #{employee[0]} successfully added"
                        conn.send(response.encode("utf-8"))
                    except ValueError as e:
                        conn.send(str(e).encode("utf-8"))
                    return
            conn.send("Invalid permissions".encode("utf-8"))
        elif request_parts[0] == "delete":
            if header_body[0] in self.sessions:
                if self.authorizer.check_permissions(self.sessions[header_body[0]][1], "delete"):
                    try:
                        self.employee_db.delete(request_parts[1])
                        response = f"Employee #{request_parts[1]} successfully deleted"
                        conn.send(response.encode("utf-8"))
                    except ValueError as e:
                        conn.send(str(e).encode("utf-8"))
                    return
            conn.send("Invalid permissions".encode("utf-8"))
        else:
            conn.send("Invalid request".encode("utf-8"))
            return

    def logon(self, credentials, conn):
        '''
        Checks to see if credentials are valid and creates a session if they are
        '''
        credentials = credentials.split(',')
        if len(credentials) != 2:
            conn.send("Invalid credentials".encode("utf-8"))
            return
        username = credentials[0]
        password = credentials[1]
        if self.authorizer.login(username, password):
            permissions = self.authorizer.get_permissions(username)
            session_id = self.create_session(username, permissions)
            conn.send(f"SUCCESS: {session_id}".encode('utf-8'))
            print(f"{username} successfully logged in")
        else:
            conn.send("Invalid credentials".encode("utf-8"))

    def create_session(self, username, permissions):
        '''
        Creates a session for a user, adds it to sessions dictionary, and returns the session id
        '''
        session_id = token_urlsafe(16)
        while session_id in self.sessions:
            session_id = token_urlsafe(16)
        self.sessions[session_id] = [username, permissions]
        return session_id
    
    def parse_employee(self, input):
        '''
        Parses the employee data from a request
        '''
        values = input.split(",")
        if len(values) != 6:
            raise ValueError("Invalid number of arguments")
        return values
