import socket
import threading
from src.common.common import *

SERVER = "127.0.0.1" # Cambiar a ip del server]
ADDR = (SERVER, PORT)

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def write_message(self, username, client):
        while True:
            message = input(">> ")
            message = f"{username}: {message}"    
            send_message(client, message)

    def print_message(self):
        while True:
            message = receive_message(self.client)
            print(f"\n{message}")

    def start_client(self):
        try:
            self.client.connect(ADDR)
            
        except ConnectionRefusedError:
            print("El Servidor no está disponible")

        receive_thread = threading.Thread(target=self.print_message)
        receive_thread.start()
        send_thread = threading.Thread(target=self.write_message, args=(username, self.client))
        send_thread.start()
        
if __name__ == "__main__":
    client = Client()
    client.start_client()