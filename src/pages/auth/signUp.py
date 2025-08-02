# views/signup.py
import flet as ft
from components.base_view import BaseView
from components.authFunctions import sign_up, on_login_success

class SignUpView(BaseView):
    def __init__(self, page):
        super().__init__(page)
        self.error_message_text_ref = ft.Ref[ft.Text]()

    def build(self):
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.ADAPTIVE

        self.email_field = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL,
                             border_radius=ft.border_radius.all(16), height=55, color=ft.Colors.WHITE, border_color=ft.Colors.WHITE,
                             label_style=ft.TextStyle(color=ft.Colors.WHITE))
        
        self.name_field = ft.TextField(label="User name", prefix_icon=ft.Icons.PERSON,
                             border_radius=ft.border_radius.all(16), height=55, color=ft.Colors.WHITE, border_color=ft.Colors.WHITE,
                             label_style=ft.TextStyle(color=ft.Colors.WHITE))

        self.password_field = ft.TextField(label="Password", password=True, can_reveal_password=True,
                                prefix_icon=ft.Icons.LOCK, border_radius=ft.border_radius.all(16),
                                height=55, color=ft.Colors.WHITE, border_color=ft.Colors.WHITE,
                                text_style=ft.TextStyle(color=ft.Colors.WHITE),
                                label_style=ft.TextStyle(color=ft.Colors.WHITE))

        self.confirm_password_field = ft.TextField(label="Confirm Password", password=True, can_reveal_password=True,
                                        prefix_icon=ft.Icons.LOCK_OUTLINE,
                                        border_radius=ft.border_radius.all(16), border_color=ft.Colors.WHITE,
                                        height=55, color=ft.Colors.WHITE,
                                        text_style=ft.TextStyle(color=ft.Colors.WHITE),
                                        label_style=ft.TextStyle(color=ft.Colors.WHITE))
        
        self.bs = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text("There's an error in the sign-up process", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                        ft.Text("Please check your details and try again", size=14, color=ft.Colors.BLACK, ref=self.error_message_text_ref),
                        ft.ElevatedButton("Dismiss", on_click=lambda _: self.page.close(self.bs)),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    tight=True,
                ),
                padding=20,
            ),
            open=False,
            on_dismiss=self.bs_dismissed,
        )
        self.page.overlay.append(self.bs)

        self.loading_indicator = ft.ProgressBar(width=300, visible=False)

        return ft.View(
            route="/signup",
            controls=[
                ft.Stack([
                    ft.Image(src="/images/bgSup2.jpg", fit=ft.ImageFit.COVER, expand=True, width=self.page.window.width,),
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            controls=[
                                ft.Container(
                                    
                                    content=ft.Image(src="/images/botHello.png", fit=ft.ImageFit.CONTAIN),
                                    alignment=ft.alignment.center,expand=2
                                ),
                                ft.Container(
                                    expand=8,
                                    padding=ft.padding.symmetric(horizontal=19, vertical=20),
                                    border_radius=ft.border_radius.only(top_left=30, top_right=30),
                                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_800),
                                    blur=18,
                                    content=ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=5,
                                        controls=[
                                            ft.Text("Create Account", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                                            ft.Text("Fill in your details", size=14, color=ft.Colors.WHITE),
                                            self.name_field,self.email_field, self.password_field, self.confirm_password_field,
                                            ft.Container(height=10),
                                            ft.ElevatedButton("Sign Up", on_click=self.handle_sign_up, width=300 ,),
                                            self.loading_indicator,
                                            ft.Divider(),
                                            ft.TextButton("Already have an account? Sign In", on_click=lambda _: self.page.go("/signin"))
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ],expand=True
                )
            ],padding=0
        )

    def bs_dismissed(self):
        self.bs.open = False
        self.page.update()

    def handle_sign_up(self, e):
        name = self.name_field.value
        email = self.email_field.value
        password = self.password_field.value
        confirm_password = self.confirm_password_field.value

        if not email or not password or not confirm_password:
            self.error_message_text_ref.current.value = "All fields are required."
            self.bs.open = True
            self.page.update()
            return
        
        if password != confirm_password:
            self.error_message_text_ref.current.value = "Passwords do not match."
            self.bs.open = True
            self.page.update()
            return

        self.loading_indicator.visible = True
        self.page.update()

        user, error = sign_up(email, password,name)

        self.loading_indicator.visible = False
        self.page.update()

        if user:
            self.page.go('/signin')
        else:
            self.error_message_text_ref.current.value = f"Sign-up failed: {error}"
            print(f"Sign-up error: {error}")
            self.bs.open = True
            self.page.update()
