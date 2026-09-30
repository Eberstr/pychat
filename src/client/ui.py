import flet as ft
from src.client.client import Client
from src.common.common import *


def main(page: ft.Page):
    client = Client()
    client.start_client()
    
    # Configuracino de la pagina
    page.title = "pyChat"
    page.bgcolor = ft.Colors.WHITE
    page.appbar = ft.AppBar(
        title=ft.Text("pyChat")
    )
    page.bgcolor = ft.Colors.WHITE

    chat = ft.Column()
    new_message = ft.TextField(color=ft.Colors.BLACK)

    username = ft.TextField(lable="Ingresa tu nombre de usuario", color=ft.Colors.BLACK)

    def send_click(e):
        client.send_message(client, new_message.value)
        new_message.value = ""    
        page.update()

    

    page.add(
        chat,
        ft.Row(controls=[new_message, ft.Button("Send", on_click=send_click)])
    )

ft.run(main)