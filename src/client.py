import socket
import select

class CubeScoutClient:

    def __init__(self, host, port):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(5)

        # connect to remote host
        try :
            self.client_socket.connect((host, port))
        except Exception as error:
            print('Unable to connect because: '+str(error))
            exit()

        print("Successfully connected to server.")
        self.client_socket.setblocking(0)

    def receive(self):
        try:
            data = self.client_socket.recv(1024) # I hope nobody's name is longer than 1024 letters
            return data
        except socket.error:
            return ""
