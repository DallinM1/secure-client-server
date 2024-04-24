import socket
import ssl
from os.path import join
from os import getcwd
from request_manager import RequestManager
import threading

class Server:
    '''
    Class for setting up server socket and connecting to clients
    '''
    def __init__(self):
        print("Starting server")
        self.HOST = 'localhost'
        self.PORT = 8080
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=join(getcwd(), 'cert.pem'), keyfile=join(getcwd(), 'key.pem'), password='password')
        context.check_hostname = False
        self.socket = context.wrap_socket(self.sock, server_side=True)
        self.socket.bind((self.HOST, self.PORT))
        self.manager = RequestManager()
        print("Server successfully started")

    def listen(self, num):
        '''
        Listens for [num] connections and creates a thread for each connection to handle the requests
        '''
        print("Ready for connections")
        self.socket.listen(num)
        while True:
            try:
                conn, addr = self.socket.accept()
            except socket.error as e:
                print("Error accepting connection: ", e)
                continue
            print('Connected to', addr)
            threading.Thread(target=self.handle_request, args=(conn,)).start()
    
    def handle_request(self, conn):
        '''
        Reads in request from a connection and sends it to the request manager to be parsed
        '''
        while True:
            data = conn.recv(1024).decode("utf-8")
            if not data:
                break
            self.manager.parse_request(data, conn)
        conn.close()
