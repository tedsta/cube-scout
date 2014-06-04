import socket
import select
import time

class CubeScoutServer:

    def __init__(self, port=20000):
        # List to keep track of socket descriptors
        self.connections = []
        self.port = port 

        # Create server socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("0.0.0.0", self.port))
        self.server_socket.listen(10)

        # Add server socket to the list of readable connections
        self.connections.append(self.server_socket)

    def listen(self):
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(self.connections,[],[], 0)

        for sock in read_sockets:
            # New connection
            if sock == self.server_socket:
                sockfd, addr = self.server_socket.accept()
                self.connections.append(sockfd)
                print("Client "+str(addr)+" connected.")
            else: # Incoming data from client
                pass
   
    def broadcast(self, message):
        # Iterate through every socket except server socket, which is the first one
        for sock in self.connections[1:]:
            try:
                sock.send(message)
            except:
                # Broken socket connection
                sock.close()
                self.connections.remove(sock)
