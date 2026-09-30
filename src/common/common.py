import socket

HEADER_SZ = 64
PORT = 55050
FORMAT = "utf-8"

def receive_message(client_socket):
    try:
        msg_length = client_socket.recv(HEADER_SZ).decode(FORMAT) # msg_length = header; Recibe de que tamaño sera el mensaje y lo convierte a str

        if not msg_length:
            return None

        msg_length = int(msg_length) # Convierte de str a int; '4  ' -> 4
        message = client_socket.recv(msg_length).decode(FORMAT) # recibe mensaje

        return message
    
    except (ConnectionResetError, ConnectionAbortedError):
        return None

def message_protocol(message):
    msg_length = len(message)
    msg_length = str(msg_length).encode(FORMAT)
    msg_length += b' ' * (HEADER_SZ - len(msg_length))

    return msg_length

def send_message(client, message):
    try:
        msg_length = message_protocol(message)
        client.sendall(msg_length)
        client.sendall(message.encode(FORMAT))
        
    except (BrokenPipeError, ConnectionResetError):
        return False

    return True