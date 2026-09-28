import socket
import threading

HEADER_SZ = 64
PORT = 55050
SERVER = "127.0.0.1" # Cambiar a ip del server
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

def client_start():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
    except Exception as e:
        print("Connection failed!")
        raise e
    
    return client

def receive_message(client):
    while True:
        msg_length = client.recv(HEADER_SZ).decode(FORMAT) # msg_length = header; Recibe de que tamaño sera el mensaje
        msg_length = int(msg_length) # Convierte de byte a int; b'4' -> 4
        message = client.recv(msg_length).decode(FORMAT) # recibe mensaje
        print(f"{message}")

def send_message_protocol(message):
    msg_length = len(message.encode(FORMAT))
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' * (HEADER_SZ - len(msg_length)) # Se asegura que el tamaño de msg_length (HEADER del protocolo) siempre sea de 64 bytes.
    
    return msg_length

def send_message(client, message):
    msg_length = send_message_protocol(message)
    client.sendall(msg_length)
    client.sendall(message.encode(FORMAT))

def write_message(client, username):
    while True:
        message = input(">>")
        message = f"{username}: {message}"
        send_message(client, message)

def main():
    client = client_start()
    username = input("\n[!] Introduce tu nombre de usuario: ")
    send_message(client, username)

    receive_thread = threading.Thread(target=receive_message, args=(client,))
    receive_thread.start()
    send_thread = threading.Thread(target=write_message, args=(client, username))
    send_thread.start()

if __name__ == "__main__":
    main()