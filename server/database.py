import sqlite3
import bcrypt
from datetime import datetime

class EmployeeDatabase:
    '''
    Class for handling connection to employee database
    '''
    def __init__(self):
        self.conn = sqlite3.connect('employee.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS employee (id INTEGER PRIMARY KEY, salt TEXT, fname TEXT, lname TEXT, ssn INTEGER, dob TEXT, salary INTEGER)")
        self.conn.commit()

    def add(self, id, fname, lname, ssn, dob, salary):
        '''
        Inserts employee into database if id does not already exist
        '''
        try:
            id = int(id)
            ssn = int(ssn)
            salary = int(salary)
        except ValueError:
            raise ValueError("ID, SSN, and salary must be integers")
        try:
            self.get(id)
        except ValueError:
            self.cur.execute("INSERT INTO employee VALUES (?, ?, ?, ?, ?, ?)", (id, fname, lname, ssn, dob, salary))
            self.conn.commit()
            return
        raise ValueError("Employee already exists")

    def get(self, id):
        '''
        Returns employee data from employee database
        '''
        try:
            id = int(id)
        except ValueError:
            raise ValueError("ID must be an integer")
        self.cur.execute(f"SELECT * FROM employee WHERE id = ?", (id,))
        rows = self.cur.fetchone()
        if rows == None:
            raise ValueError("Employee does not exist")
        return rows

    def delete(self, id):
        '''
        Deletes employee from employee database
        '''
        try:
            id = int(id)
        except ValueError:
            raise ValueError("ID must be an integer")
        try: 
            self.get(id)
        except ValueError as e:
            raise ValueError(e)
        self.cur.execute("DELETE FROM employee WHERE id = ?", (id,))
        self.conn.commit()

    def update(self, id, fname, lname, ssn, dob, salary):
        '''
        Updates employee data in employee database
        '''
        try:
            id = int(id)
            if ssn != "":
                ssn = int(ssn)
            if salary != "":
                salary = int(salary)
        except ValueError:
            raise ValueError("ID, SSN, and salary must be integers")
        try:
            self.get(id)
            if dob != "":
                self.parse_dob(dob)
        except ValueError as e:
            raise ValueError(e)
        if fname != "":
            self.cur.execute("UPDATE employee SET fname = ? WHERE id = ?", (fname, id))
        if lname != "":
            self.cur.execute("UPDATE employee SET lname = ? WHERE id = ?", (lname, id))
        if ssn != "":
            self.cur.execute("UPDATE employee SET ssn = ? WHERE id = ?", (ssn, id))
        if dob != "":
            self.cur.execute("UPDATE employee SET dob = ? WHERE id = ?", (dob, id))
        if salary != "":
            self.cur.execute("UPDATE employee SET salary = ? WHERE id = ?", (salary, id))
        self.conn.commit()

    def parse_dob(self, dob):
        '''
        Parses date of birth to make sure it is in valid mm-dd-yyyy format
        '''
        dob_parts = dob.split("-")
        if len(dob_parts) != 3:
            raise ValueError("Date of birth must be in the format mm-dd-yyyy")
        elif dob_parts[0].isdigit() == False or dob_parts[1].isdigit() == False or dob_parts[2].isdigit() == False:
            raise ValueError("Date of birth must be in the format mm-dd-yyyy")
        elif len(dob_parts[0]) != 2 or len(dob_parts[1]) != 2 or len(dob_parts[2]) != 4:
            raise ValueError("Date of birth must be in the format mm-dd-yyyy")
        elif int(dob_parts[0]) > 12 or int(dob_parts[1]) > 31 or int(dob_parts[2]) > datetime.now().year:
            raise ValueError("Date of birth must be in the format mm-dd-yyyy")
        return

    def __del__(self):
        self.conn.close()

class UserDatabase:
    '''
    Class for handling connection to user database
    '''
    def __init__(self):
        self.conn = sqlite3.connect('user.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS user (username TEXT PRIMARY KEY, password TEXT, permissions TEXT)")
        self.conn.commit()

    def insert_user(self, username, password, permissions):
        '''
        Inserts user into user database if username does not already exist
        '''
        try:
            self.get(username)
        except ValueError:
            self.cur.execute("INSERT INTO user VALUES (?, ?, ?)", (username, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), permissions))
            self.conn.commit()
            return
        raise ValueError("Username already exists")
        

    def get(self, username):
        '''
        Returns user data from user database if user exists
        '''
        self.cur.execute("SELECT * FROM user WHERE username = ?", (username,))
        row = self.cur.fetchone()
        if row == None:
            raise ValueError("User does not exist")
        return row
    
    def get_password(self, username):
        '''
        Returns the hashed password for a user from user database
        '''
        try:
            return self.get(username)[1]
        except ValueError as e:
            raise ValueError(e)

    def delete(self, username):
        '''
        Deletes user from user database
        '''
        if isinstance(username, str) == False:
            raise ValueError("Username must be a string")
        try:
            self.get(username)
        except ValueError as e:
            raise ValueError(e)
        self.cur.execute("DELETE FROM user WHERE username = ?", (username,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
