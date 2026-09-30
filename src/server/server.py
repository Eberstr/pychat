import socket
import threading
from src.common.common import *

SERVER = "0.0.0.0"
ADDR = (SERVER, PORT)

class Server:

    def __init__(self):
        self.clients = []
        self.usernames = []
        self.server = socket.create_server(ADDR)

    def broadcast(self, message):
        for client in self.clients:
            try:
                send_message(client, message)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                client.close()
                self.clients.remove(client)

    def client_handling(self, client_socket):
        username = receive_message(client_socket)
        self.usernames.append(username)

        self.broadcast(f"{username} se ha unido!")
        print(f"{username} se ha unido!")

        while True:
            message = receive_message(client_socket)
            if message is not None:
                self.broadcast(message)
            
            else:
                client_socket.close()
                self.clients.remove(client_socket)
                self.usernames.remove(username)
                self.broadcast(f"{username} se ha ido!")
                print(f"{username} se ha ido!")

                break

    def start_server(self):
        print("\nServer waiting for connections... ")

        while True:
            client_socket, address = self.server.accept()
            self.clients.append(client_socket)
            thread = threading.Thread(target=self.client_handling, args=(client_socket, ))
            thread.start()

if __name__ == "__main__":
    server = Server()
    server.start_server()