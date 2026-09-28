import socket
import threading

HEADER_SZ = 64 # Define cuantos bytes se reservan para indicar el tamaño del mensaje; No limita el tamaño del mensaje; solo contiene su longitud.
PORT = 55050
SERVER = "0.0.0.0" # Indica que escuche a través de todas las interfaces
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def broadcast(clients, message):
    for client in clients:
        send_message(client, message)

def receive_message(client_socket):
        #message = client_socket.recv(HEADER_SZ).decode(FORMAT) # Server recibe mensaje de cliente; toma todos los bytes como mensaje.
        msg_length = client_socket.recv(HEADER_SZ).decode(FORMAT) # msg_length = header; Recibe de que tamaño sera el mensaje
        msg_length = int(msg_length) # Convierte de str a int; '4  ' -> 4
        message = client_socket.recv(msg_length).decode(FORMAT) # recibe mensaje

        return msg_length, message

def send_message(client, message):
    msg_length = message_protocol(message)
    client.sendall(msg_length)
    client.sendall(message.encode(FORMAT))

def message_protocol(message):
    msg_length = len(message)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' * (HEADER_SZ - len(msg_length))

    return msg_length

def client_handling(clients, client_socket, usernames):

    msg_length, username = receive_message(client_socket)

    usernames.append(username)

    broadcast(clients, f"{username} se ha unido!")
    print(f"{username} se ha unido!")
    
    while True:
        msg_length, message = receive_message(client_socket)
        if message:
            broadcast(clients, message) # Server envia mensaje a los demas clientes
        else:
            client_socket.close()
            clients.remove(client_socket)

def server_start():
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
    except Exception as e:
        raise e

    return server

def main():
    clients = []
    usernames = []

    server = server_start()

    print("Server waiting connections...")
    while True:
        client_socket, address = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=client_handling, args=(clients, client_socket, usernames))
        thread.start()

if __name__ == "__main__":
    main()