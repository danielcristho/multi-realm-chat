import flet as ft

# SignIn Form
class CreateGroup(ft.UserControl):
    def __init__(self, submit_values,btn_join):
        super().__init__()
        #Return values group name
        self.submit_values = submit_values
        #Route to join group
        self.btn_join = btn_join

    def btn_create(self, e):
        if not self.group_name.value:
            self.group_name.error_text="Group name is required!"
            self.group_name.update()
        else:
            #Return values group_name as argument
            self.submit_values(self.group_name.value)

    def build(self):
        self.title_form=ft.Text(value="Create Group",text_align=ft.TextAlign.CENTER,size=30, )

        self.group_name = ft.TextField(label="Group Name")

        self.text_join=ft.Row(controls=[ft.Text(value="Already have a group?"),ft.TextButton(text="Join here",on_click=self.btn_join)],alignment=ft.MainAxisAlignment.CENTER)

        self.text_create=ft.ElevatedButton(text="Create Group",color=ft.colors.WHITE,width=150,height=50,on_click= self.btn_create)
        return ft.Container(
            width=500,
            height=600,
            bgcolor=ft.colors.TEAL_400,
            padding=30,
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Column(
                [
                    self.title_form,
                    self.group_name,
                    ft.Container(height=10),
                    self.text_join,
                    ft.Container(height=20),
                    self.text_create,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )