import flet as ft
import threading
from src.client.client import Client
from src.common.common import *

def main(page: ft.Page):
    client_socket = Client()
    client_socket.start_client()
    
    # Configuracino de la pagina
    page.title = "pyChat"
    page.bgcolor = ft.Colors.WHITE
    page.appbar = ft.AppBar(
        title=ft.Text("pyChat")
    )
    page.bgcolor = ft.Colors.WHITE

    chat = ft.Column()
    new_message = ft.TextField(color=ft.Colors.BLACK)

    username = ft.TextField(label="Ingresa tu nombre de usuario", color=ft.Colors.BLACK)

    def receive():
        message = receive_message(client_socket.client)
        chat.controls.append(message)
        page.update()
        return message
    
    def send_click(e):
        send_message(client_socket.client, new_message.value)
        new_message.value = ""    
        page.update()

    def join_click(e):
        if not username.value:
            username.error = "El nombre no puede estar en blanco"
            username.update()
        else:
            send_message(client_socket.client, username.value)
            page.pop_dialog()

    page.show_dialog(
        ft.AlertDialog(
            bgcolor=ft.Colors.WHITE,
            open=True,
            modal=True,
            title=ft.Text("Bienvenido!", color=ft.Colors.BLACK),
            content=ft.Column([username], tight=True),
            actions=[ft.Button(content="Unirse", on_click=join_click, color=ft.Colors.BLUE_300, bgcolor=ft.Colors.WHITE)],
            actions_alignment=ft.MainAxisAlignment.END
        )
    )

    page.add(
        chat,
        ft.Row(controls=[new_message, ft.Button("Send", on_click=send_click)])
    )

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

ft.run(main)