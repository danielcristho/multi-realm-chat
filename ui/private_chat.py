import flet as ft

class PrivateChatPage(ft.Column):
    def __init__(self, page, recipient, chat, send_message_click):
        super().__init__()
        self.page = page
        self.recipient = recipient
        self.chat = chat
        self.send_message_click = send_message_click
        self.build()

    def build(self):
        self.controls = [
            ft.Row(
                controls=[
                    ft.Text(f"Private Chat with {self.recipient}", color=ft.colors.WHITE),
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        tooltip="Back to chat",
                        on_click=self.back_to_chat,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Container(
                content=self.chat,
                border=ft.border.all(1, ft.colors.OUTLINE),
                border_radius=5,
                padding=10,
                expand=True,
            ),
            ft.Row(
                controls=[
                    ft.TextField(
                        hint_text="Write a message...",
                        autofocus=True,
                        shift_enter=True,
                        min_lines=1,
                        max_lines=5,
                        filled=True,
                        expand=True,
                        on_submit=self.send_message_click,
                    ),
                    ft.IconButton(
                        icon=ft.icons.SEND_ROUNDED,
                        tooltip="Send message",
                        on_click=self.send_message_click,
                    ),
                ],
            ),
        ]

    def back_to_chat(self, e):
        self.page.route = "/chat"
        self.page.update()

    def send_message_click(self, e):
        message_text = self.controls[2].controls[0].value
        if message_text:
            self.send_private_message(message_text)
            self.controls[2].controls[0].value = ""

    def send_private_message(self, message_text):
        # Send the message to the recipient (e.g., using a WebSocket or API call)
        # Update the private chat page with the new message
        self.chat.controls.append(
            ft.Text(f"You: {message_text}", color=ft.colors.WHITE)
        )
        self.page.update()