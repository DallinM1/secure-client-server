from client import Client
from datetime import datetime


#TODO Add logout functionality to remove session from server
class credentials:
    def __init__(self, username, password):
        self.username = username
        self.password = password

def prompt_password():
    print("Hello! Please enter username and password below")
    username = input("Username: ")
    password = input("Password: ")
    return username, password

def get_credentials():
    '''
    Prompts user for username and password and confirms the input
    '''
    username, password = prompt_password()
    print(f"You entered: Username= {username}, Password= {password}")
    response = input("Is this correct? (Enter y/n): ")
    if response == "y":
        return credentials(username, password)
    else:
        print("Please try again\n")
        return None
    
def create_employee_prompt():
    '''
    Prompts user for input to create a new employee record
    '''
    print("Enter the following information for the new employee record:")
    while True:
        id = input("\tEmployee ID: ")
        if id.isdigit() == False:
            print("Employee ID must be a number.  Please try again\n")
            continue
        else:
            break
    while True:
        fname = input("\tEnter first name: ")
        if fname.isalpha() == False:
            print("First name must contain only letters.  Please try again\n")
            continue
        else:
            break
    while True:
        lname = input("\tEnter last name: ")
        if lname.isalpha() == False:
            print("Last name must contain only letters.  Please try again\n")
            continue
        else:
            break
    while True:
        ssn = input("\tEnter SSN (Numbers only, no dashes): ")
        if ssn.isdigit() == False:
            print("SSN must only be numbers.  Please try again\n")
        elif len(ssn) != 9:
            print("SSN must be 9 digits.  Please try again\n")
        else:
            break
    while True:
        dob = input("\tEnter date of birth (mm-dd-yyyy): ")
        dob_parts = dob.split("-")
        if len(dob_parts) != 3:
            print("Date of birth must be in the format mm-dd-yyyy.  Please try again\n")
        elif dob_parts[0].isdigit() == False or dob_parts[1].isdigit() == False or dob_parts[2].isdigit() == False:
            print("Date of birth fields must only include numbers.  Please try again\n")
        elif len(dob_parts[0]) != 2 or len(dob_parts[1]) != 2 or len(dob_parts[2]) != 4:
            print("Date of birth must be in the format mm-dd-yyyy.  Please try again\n")
        elif int(dob_parts[0]) > 12 or int(dob_parts[1]) > 31 or int(dob_parts[2]) > datetime.now().year:
            print("Date of birth is invalid.  Please try again\n")
        else:
            break
    while True:
        salary = input("\tEnter salary: ")
        if salary.isdigit() == False:
            print("Salary must only be numbers.  Please try again\n")
        else:
            break
    print(f"You entered:\n\tID= {id}\n\tFirst Name= {fname}\n\tLast Name= {lname}\n\tSSN= {ssn}\n\tDOB= {dob}\n\tSalary= {salary}")
    while True:
        confirm = input("\nIs this correct? (Enter y/n): ")
        if confirm == "y":
            employee = [id, fname, lname, ssn, dob, salary]
            return employee
        if confirm == "n":
            print("Please try again\n")
            return None
            

def update_employee_prompt():
    '''
    Prompts user for input to update an employee record
    '''
    print("Enter ID of employee you want to update")
    while True:
        id = input("\tEmployee ID: ")
        if id == "" or id.isdigit() == True:
            break
        else:
            print("Employee ID must be a number.  Please try again\n")
            continue
    print(f"For information you want updated for employee #{id}, enter the new value.  For information you want to keep the same, leave blank (press enter)")
    while True:
        fname = input("\tEnter first name: ")
        if fname == "" or fname.isalpha() == True:
            break
        else:
            print("First name must contain only letters.  Please try again\n")
            continue
    while True:
        lname = input("\tEnter last name: ")
        if lname == "" or lname.isalpha() == True:
            break
        else:
            print("Last name must contain only letters.  Please try again\n")
            continue
    while True:
        ssn = input("\tEnter SSN (Numbers only, no dashes): ")
        if ssn == "" or ssn.isdigit() == True:
            break
        else:
            print("SSN must only be numbers.  Please try again\n")
            continue
    while True:
        dob = input("\tEnter date of birth (mm-dd-yyyy): ")
        dob_parts = dob.split("-")
        if dob == "":
            break
        elif len(dob_parts) != 3:
            print("Date of birth must be in the format mm-dd-yyyy.  Please try again\n")
        elif dob_parts[0].isdigit() == False or dob_parts[1].isdigit() == False or dob_parts[2].isdigit() == False:
            print("Date of birth fields must only include numbers.  Please try again\n")
        elif len(dob_parts[0]) != 2 or len(dob_parts[1]) != 2 or len(dob_parts[2]) != 4:
            print("Date of birth must be in the format mm-dd-yyyy.  Please try again\n")
        elif int(dob_parts[0]) > 12 or int(dob_parts[1]) > 31 or int(dob_parts[2]) > datetime.now().year:
            print("Date of birth is invalid.  Please try again\n")
        else:
            break
    while True:
        salary = input("\tEnter salary: ")
        if salary == "" or salary.isdigit() == True:
            break
        else:
            print("Salary must only be numbers.  Please try again\n")
            continue
    print(f"You entered:\n\tID= {id}\n\tFirst Name= {fname}\n\tLast Name= {lname}\n\tSSN= {ssn}\n\tDOB= {dob}\n\tSalary= {salary}")
    confirm = input("Is this correct? (Enter y/n): ")
    if confirm == "y":
        employee = [id, fname, lname, ssn, dob, salary]
        return employee
    else:
        print("Please try again\n")
        return None

def main():
    client = Client()
    if client.connect() is False:
        print("Connection failed.  Please try again\n")
        return
    login = False
    while login is False:
        credentials = None
        while credentials is None:
            credentials = get_credentials()
        message = f"-//logon: {credentials.username},{credentials.password}"
        session = client.send_and_recv(message)
        if "SUCCESS" in session:
            login = True
            session = session.split(": ")[1]
        else:
            print("Invalid credentials.  Please try again\n")
    print(f"{credentials.username} successfully logged in\n")
    selection = None
    while True:
        print("Enter the character for desired action\n'q' : logout\n'1' : Request a record\n'2' : Add a record\n'3' : Update a record\n'4' : Delete a record")
        selection = input()
        if selection == "q":
            break
        elif selection == "1":
            id = input("Enter ID of employee for desired record: ")
            response = client.send_and_recv(f"{session}//get: {id}")
            print(response)
        elif selection == "2":
            employee = None
            while employee is None:
                employee = create_employee_prompt()
            employee_data = ",".join(employee)
            response = client.send_and_recv(f"{session}//add: {employee_data}")
            print(response)
        elif selection == "3":
            employee = None
            while employee is None:
                employee = update_employee_prompt()
            employee_data = ",".join(employee)
            response = client.send_and_recv(f"{session}//update: {employee_data}")
            print(response)
        elif selection == "4":
            id = input("Enter ID of employee to be deleted: ")
            response = client.send_and_recv(f"{session}//delete: {id}")
            print(response)
        else:
            print("Invalid selection.  Please try again")
        print()
    print("You have successfully logged out.  Goodbye.\n")
    
if __name__ == "__main__":
    main()
