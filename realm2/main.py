import flet as ft
from chat_cli import ChatClient
import json

class ChatApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Multi-Realm Chat App"
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.padding = 20
        self.client = None
        self.current_user = None
        self.current_group = None

        # Login components
        self.username_field = ft.TextField(label="Username", autofocus=True)
        self.password_field = ft.TextField(label="Password", password=True)
        self.login_button = ft.ElevatedButton(text="Login", on_click=self.login)
        self.login_view = ft.Column([
            ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
            self.username_field,
            self.password_field,
            self.login_button
        ])

        # Chat components
        self.message_list = ft.ListView(expand=True, spacing=10, auto_scroll=True)
        self.new_message = ft.TextField(label="Type a message...", expand=True)
        self.send_button = ft.IconButton(icon=ft.icons.SEND, on_click=self.send_message)
        self.recipient_field = ft.TextField(label="Recipient (user or group)", expand=True)
        self.file_picker = ft.FilePicker(on_result=self.send_file)
        self.page.overlay.append(self.file_picker)
        self.attach_button = ft.IconButton(icon=ft.icons.ATTACH_FILE, on_click=lambda _: self.file_picker.pick_files())

        # Group management components
        self.create_group_field = ft.TextField(label="New Group Name", expand=True)
        self.create_group_button = ft.ElevatedButton(text="Create Group", on_click=self.create_group)
        self.join_group_field = ft.TextField(label="Group to Join", expand=True)
        self.join_group_button = ft.ElevatedButton(text="Join Group", on_click=self.join_group)

        # Main chat view
        self.chat_view = ft.Column([
            ft.Row([
                self.recipient_field,
                ft.ElevatedButton(text="Inbox", on_click=self.show_inbox),
                ft.ElevatedButton(text="Logout", on_click=self.logout)
            ]),
            self.message_list,
            ft.Row([
                self.new_message,
                self.attach_button,
                self.send_button
            ]),
            ft.Row([
                self.create_group_field,
                self.create_group_button,
                self.join_group_field,
                self.join_group_button
            ])
        ], expand=True)

        # Set initial view
        self.page.add(self.login_view)

    def login(self, e):
        username = self.username_field.value
        password = self.password_field.value
        self.client = ChatClient()
        result = self.client.login(username, password)
        if "logged in" in result:
            self.current_user = username
            self.page.clean()
            self.page.add(self.chat_view)
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Logged in successfully!"))
            self.page.snack_bar.open = True
        else:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Login failed. Please try again."))
            self.page.snack_bar.open = True
        self.page.update()

    def logout(self, e):
        if self.client:
            self.client.logout()
        self.client = None
        self.current_user = None
        self.page.clean()
        self.page.add(self.login_view)
        self.page.update()

    def send_message(self, e):
        recipient = self.recipient_field.value
        message = self.new_message.value
        if recipient and message:
            if recipient.startswith("group:"):
                result = self.client.send_message_group(recipient[6:], message)
            else:
                result = self.client.sendmessage(recipient, message)
            self.message_list.controls.append(ft.Text(f"You to {recipient}: {message}"))
            self.new_message.value = ""
            self.page.update()

    def show_inbox(self, e):
        inbox = self.client.inbox()
        try:
            messages = json.loads(inbox)
            self.message_list.controls.clear()
            for sender, msg_list in messages.items():
                for msg in msg_list:
                    self.message_list.controls.append(ft.Text(f"{sender}: {msg['msg']}"))
            self.page.update()
        except json.JSONDecodeError:
            print(f"Error decoding inbox: {inbox}")

    def create_group(self, e):
        group_name = self.create_group_field.value
        if group_name:
            result = self.client.create_group(group_name)
            self.page.snack_bar = ft.SnackBar(content=ft.Text(result))
            self.page.snack_bar.open = True
            self.create_group_field.value = ""
            self.page.update()

    def join_group(self, e):
        group_name = self.join_group_field.value
        if group_name:
            result = self.client.join_group(group_name)
            self.page.snack_bar = ft.SnackBar(content=ft.Text(result))
            self.page.snack_bar.open = True
            self.join_group_field.value = ""
            self.page.update()

    def send_file(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            recipient = self.recipient_field.value
            if recipient:
                # implementasi logic send file masih belum
                self.message_list.controls.append(ft.Text(f"File sent to {recipient}: {file_path}"))
                self.page.update()

def main(page: ft.Page):
    ChatApp(page)

ft.app(target=main)