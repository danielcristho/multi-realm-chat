import flet as ft
from signin_form import *
from signup_form import *
from users_db import *
from chat_message import *
import socket
import json
import base64
import os
import time

server_ip = '127.0.0.1'
server_port = 8889

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

def send_to_server(message):
    client_socket.sendall((message + '\r\n').encode())
    response = ""
    while True:
        data = client_socket.recv(32)
        if data:
            response += data.decode()
            if response[-2:] == '\r\n':
                break
    return response.strip()

def main(page: ft.Page):
    page.title = "Multi Realm Chat"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Functions
    def dropdown_changed(e):
        new_message.value = new_message.value + emoji_list.value
        page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

    def open_dlg():
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dlg(e):
        dlg.open = False
        page.route = "/"
        page.update()

    def sign_in(user: str, password: str):
        db = UsersDB()
        if not db.read_db(user, password):
            print("User no exist ...")
            page.banner.open = True
            page.update()
        else:
            print("Redirecting to chat...")
            page.session.set("user", user)
            page.route = "/chat"
            page.pubsub.send_all(
                Message(
                    user=user,
                    text=f"{user} has joined the chat.",
                    message_type="login_message",
                )
            )
            send_to_server(json.dumps({"type": "login", "user": user}))
            page.update()

    def sign_up(user: str, password: str):
        db = UsersDB()
        if db.write_db(user, password):
            print("Successfully Registered User...")
            open_dlg()
            send_to_server(json.dumps({"type": "signup", "user": user}))

    def on_message(message: Message):
        if message.message_type == "chat_message":
            m = ChatMessage(message)
        elif message.message_type == "login_message":
            m = ft.Text(message.text, italic=True, color=ft.colors.WHITE, size=12)
        elif message.message_type == "file_message":
            m = ft.Column([
                ft.Text(f"{message.user} sent a file:", italic=True, color=ft.colors.WHITE, size=12),
                ft.ElevatedButton(
                    text=f"Download {message.text}",
                    on_click=lambda _: download_file(message.file_content, message.text)
                )
            ])
        chat.controls.append(m)
        page.update()

    page.pubsub.subscribe(on_message)

    def send_message_click(e):
        message = new_message.value
        page.pubsub.send_all(
            Message(
                user=page.session.get("user"),
                text=message,
                message_type="chat_message",
            )
        )
        send_to_server(json.dumps({"type": "message", "user": page.session.get("user"), "message": message}))
        new_message.value = ""
        page.update()

    def send_file(e: ft.FilePickerResultEvent):
        print("send_file called")
        if e.files:
            print(f"Number of files: {len(e.files)}")
            for f in e.files:
                print(f"File info: {f}")
                file_name = f.name
                
                if f.path:
                    with open(f.path, "rb") as file:
                        file_bytes = file.read()
                    
                    file_contents = base64.b64encode(file_bytes).decode('utf-8')
                    
                    page.pubsub.send_all(
                        Message(
                            user=page.session.get("user"),
                            text=file_name,
                            message_type="file_message",
                            file_content=file_contents
                        )
                    )
                    send_to_server(json.dumps({
                        "type": "file",
                        "user": page.session.get("user"),
                        "filename": file_name,
                        "file_content": file_contents
                    }))
                else:
                    upload_files = [
                        ft.FilePickerUploadFile(
                            f.name,
                            upload_url=page.get_upload_url(f.name, 600),
                        )
                    ]
                    upload_result = file_picker.upload(upload_files)
                    
                    if upload_result:
                        while not upload_result.completed:
                            time.sleep(0.1)
                        
                        # Get the uploaded file path
                        uploaded_file_path = os.path.join(page.upload_dir, f.name)
                        with open(uploaded_file_path, "rb") as file:
                            file_bytes = file.read()
                        
                        file_contents = base64.b64encode(file_bytes).decode('utf-8')
                        
                        page.pubsub.send_all(
                            Message(
                                user=page.session.get("user"),
                                text=file_name,
                                message_type="file_message",
                                file_content=file_contents
                            )
                        )
                        send_to_server(json.dumps({
                            "type": "file",
                            "user": page.session.get("user"),
                            "filename": file_name,
                            "file_content": file_contents
                        }))
                    else:
                        print("Upload failed or was cancelled.")
        
        page.update()


    def download_file(file_content, filename):
        decoded_content = base64.b64decode(file_content)
        if page.web:  # For web environment
            page.launch_url(page.get_download_url(filename, decoded_content))
        else:  # For desktop environment
            download_path = os.path.join(os.path.expanduser("~"), "Downloads", filename)
            with open(download_path, "wb") as f:
                f.write(decoded_content)
        
        page.snack_bar = ft.SnackBar(content=ft.Text(f"File {filename} downloaded successfully!"))
        page.snack_bar.open = True
        page.update()

    file_picker = ft.FilePicker(on_result=send_file)
    page.overlay.append(file_picker)


    def btn_signin(e):
        page.route = "/"
        page.update()

    def btn_signup(e):
        page.route = "/signup"
        page.update()

    def btn_exit(e):
        page.session.remove("user")
        page.route = "/"
        page.update()

    """
    Application UI
    """
    principal_content = ft.Column(
        [
            ft.Text(value="Multi Realm Chat", size=50, color=ft.colors.WHITE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    emoji_list = ft.Dropdown(
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("😃"),
            ft.dropdown.Option("😊"),
            ft.dropdown.Option("😂"),
            ft.dropdown.Option("🤔"),
            ft.dropdown.Option("😭"),
            ft.dropdown.Option("😉"),
            ft.dropdown.Option("🤩"),
            ft.dropdown.Option("🥰"),
            ft.dropdown.Option("😎"),
            ft.dropdown.Option("❤️"),
            ft.dropdown.Option("🔥"),
            ft.dropdown.Option("✅"),
            ft.dropdown.Option("✨"),
            ft.dropdown.Option("👍"),
            ft.dropdown.Option("🎉"),
            ft.dropdown.Option("👉"),
            ft.dropdown.Option("⭐"),
            ft.dropdown.Option("☀️"),
            ft.dropdown.Option("👀"),
            ft.dropdown.Option("👇"),
            ft.dropdown.Option("🚀"),
            ft.dropdown.Option("🎂"),
            ft.dropdown.Option("💕"),
            ft.dropdown.Option("🏡"),
            ft.dropdown.Option("🍎"),
            ft.dropdown.Option("🎁"),
            ft.dropdown.Option("💯"),
            ft.dropdown.Option("💤"),
        ],
        width=50,
        value="😃",
        alignment=ft.alignment.center,
        border_color=ft.colors.AMBER,
        color=ft.colors.AMBER,
    )

    signin_UI = SignInForm(sign_in, btn_signup)
    signup_UI = SignUpForm(sign_up, btn_signin)

    chat = ft.ListView(
        expand=True,
        spacing=10,
        auto_scroll=True,
    )

    new_message = ft.TextField(
        hint_text="Write a message...",
        autofocus=True,
        shift_enter=True,
        min_lines=1,
        max_lines=5,
        filled=True,
        expand=True,
        on_submit=send_message_click,
    )

    page.banner = ft.Banner(
        bgcolor=ft.colors.BLACK45,
        leading=ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=40),
        content=ft.Text("Log in failed, Incorrect User Name or Password"),
        actions=[
            ft.TextButton("Ok", on_click=close_banner),
        ],
    )

    dlg = ft.AlertDialog(
        modal=True,
        title=ft.Container(
            content=ft.Icon(
                name=ft.icons.CHECK_CIRCLE_OUTLINED, color=ft.colors.GREEN, size=100
            ),
            width=120,
            height=120,
        ),
        content=ft.Text(
            value="Congratulations,\n your account has been successfully created\n Please Sign In",
            text_align=ft.TextAlign.CENTER,
        ),
        actions=[
            ft.ElevatedButton(
                text="Continue", color=ft.colors.WHITE, on_click=close_dlg
            )
        ],
        actions_alignment="center",
        on_dismiss=lambda e: print("Dialog dismissed!"),
    )

    """
    Routes
    """
    def route_change(route):
        if page.route == "/":
            page.clean()
            page.add(
                ft.Column(
                    [
                        principal_content,
                        signin_UI
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        if page.route == "/signup":
            page.clean()
            page.add(
                ft.Column(
                    [
                        principal_content,
                        signup_UI
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        if page.route == "/chat":
            if page.session.contains_key("user"):
                page.clean()
                page.add(
                    ft.Row(
                        [
                            ft.Text(value="Multi Realm Chat", color=ft.colors.WHITE),
                            ft.ElevatedButton(
                                text="Log Out",
                                bgcolor=ft.colors.RED_800,
                                on_click=btn_exit,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    )
                )
                page.add(
                    ft.Container(
                        content=chat,
                        border=ft.border.all(1, ft.colors.OUTLINE),
                        border_radius=5,
                        padding=10,
                        expand=True,
                    )
                )
                page.add(
                    ft.Row(
                        controls=[
                            emoji_list,
                            new_message,
                            ft.IconButton(
                                icon=ft.icons.ATTACH_FILE,
                                tooltip="Send file",
                                on_click=lambda _: file_picker.pick_files(allow_multiple=True)
                            ),
                            ft.IconButton(
                                icon=ft.icons.SEND_ROUNDED,
                                tooltip="Send message",
                                on_click=send_message_click,
                            ),
                        ],
                    )
                )
            else:
                page.route = "/"
                page.update()

    page.on_route_change = route_change
    page.add(
        ft.Column(
            [
                principal_content,
                signin_UI
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    os.environ["FLET_SECRET_KEY"] = os.urandom(16).hex()
    
    ft.app(
        target=main,
        view=ft.WEB_BROWSER,
        upload_dir="uploads"
    )