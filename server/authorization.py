from database import UserDatabase
import bcrypt

class Authorization:
    '''
    Class for handling user authorization
    '''
    def __init__(self):
        self.db = UserDatabase()

    def login(self, username, password):
        '''
        Checks to see if the username and password are valid
        '''
        try:
            user = self.db.get(username)
        except ValueError:
            return False
        return bcrypt.checkpw(password.encode(), user[1].encode())
    
    def get_permissions(self, username):
        '''
        Gets the permissions for a user from the user dataabse
        '''
        try:
            user = self.db.get(username)
        except ValueError:
            raise ValueError("User does not exist")
        return user[2]
    
    def check_permissions(self, permissions, permission_name):
        '''
        Takes a string of permissions (1-yes and 0-no associated with index associated with permission) and a permission name and checks if the user has that permission
        '''
        permissions = permissions.split(",")
        if len(permissions) != 4:
            raise Exception("Invalid permissions")
        if permission_name == 'get' and permissions[0]=='1':
            return True
        elif permission_name == 'add' and permissions[1]=='1':
            return True
        elif permission_name == 'update' and permissions[2]=='1':
            return True
        elif permission_name == 'delete' and permissions[3]=='1':
            return True
        return False
