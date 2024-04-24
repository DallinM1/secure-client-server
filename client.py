import socket
import ssl
from os.path import join
from os import getcwd

class Client:
    '''
    Class for setting up client socket and connecting to server
    '''
    def __init__(self):
        self.HOST = 'localhost'
        self.PORT = 8080
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cafile=join(getcwd(), 'server_certs.pem'))
        self.socket = context.wrap_socket(self.sock, server_hostname=self.HOST)

    def connect(self):
        '''
        Connects client socket to server
        '''
        print("Attempting to connect to server")
        try:
            self.socket.connect((self.HOST, self.PORT))
            print("Established secure connection to server\n")
            return True
        except socket.error as e:
            print(f"Error connecting to server: {e}")
            return False

    def send_and_recv(self, message):
        '''
        Sends a message to the server, waits for a response, and returns the response
        '''
        self.socket.send(message.encode("utf-8"))
        response = self.socket.recv(1024)
        return response.decode("utf-8")
