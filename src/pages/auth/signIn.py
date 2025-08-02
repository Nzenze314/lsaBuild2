# views/signin.py
import flet as ft
from components.base_view import BaseView
from components.authFunctions import sign_in, on_login_success, get_profile_data

class SignInView(BaseView):
    def __init__(self, page):
        super().__init__(page)
        self.error_message_text_ref = ft.Ref[ft.Text]()
        self.signInBtn = ft.ElevatedButton("Sign In", on_click=self.handle_sign_in, width=300)
        # if credentials exist in session, pre-fill the email and password fields
        

    def build(self):
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.ADAPTIVE

        self.email_field = ft.TextField(
            label="Email", prefix_icon=ft.Icons.EMAIL,
            border_radius=ft.border_radius.all(16),
            border_color=ft.Colors.WHITE,
            height=55,color=ft.Colors.WHITE,
            label_style=ft.TextStyle(color=ft.Colors.WHITE)
        )
        self.password_field = ft.TextField(
            label="Password", password=True, can_reveal_password=True,
            prefix_icon=ft.Icons.LOCK, color=ft.Colors.WHITE,
            border_color=ft.Colors.WHITE,
            border_radius=ft.border_radius.all(16),
            height=55,text_style=ft.TextStyle(color=ft.Colors.WHITE),label_style=ft.TextStyle(color=ft.Colors.WHITE)
        )
        user = self.page.session.get("user")
        if user:
            self.page.go("/home")
        credentials = self.page.client_storage.get("credentials")
        if credentials:
            self.email_field.value = credentials[0]
            self.password_field.value = credentials[1]

        self.bs = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text("There's an error in the sign-in process", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.RED),
                        ft.Text("Please check your email and password and try again", size=14, color=ft.Colors.BLACK, ref=self.error_message_text_ref),
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
            route="/signin",
            controls=[
                ft.Stack(
                    [
                        ft.Image(
                            fit=ft.ImageFit.COVER,
                            width=self.page.window.width,
                            src="/images/bgSup2.jpg",
                            expand=1,
                        ),
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                controls=[
                                    ft.Container(
                                        content=ft.Image(src="/images/botHello.png", fit=ft.ImageFit.CONTAIN),
                                        expand=2,
                                        alignment=ft.alignment.center,
                                    ),
                                    ft.Container(
                                        expand=5,
                                        padding=ft.padding.symmetric(horizontal=19, vertical=20),
                                        border_radius=ft.border_radius.only(top_left=30, top_right=30),
                                        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_800),
                                        blur=12,
                                        content=ft.Column(
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=10,
                                            controls=[
                                                ft.Text("Welcome Back", size=24, weight=ft.FontWeight.BOLD,color=ft.Colors.PRIMARY),
                                                ft.Text("Sign in to continue chating", size=14, color=ft.Colors.WHITE),
                                                self.email_field,
                                                self.password_field,
                                                ft.Row(
                                                    [ft.TextButton("Forgot Password?",style=ft.ButtonStyle(color=ft.Colors.WHITE), on_click=lambda _: self.page.go("/forgotpassword"))],
                                                    alignment=ft.MainAxisAlignment.END
                                                ),
                                                 self.signInBtn,
                                                self.loading_indicator,
                                                ft.Divider(),
                                                ft.TextButton("Don't have an account? Sign Up", on_click=lambda _: self.page.go("/signup"))
                                            ]
                                        )
                                    )
                                ],
                                expand=True,
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                            )
                        )
                    ],expand=True
                ),
            ],padding=0
        )
    
    def bs_dismissed(self):
        self.signInBtn.disabled = False
        self.bs.open = False
        
        self.page.update()

    def handle_sign_in(self, e):
        self.signInBtn.disabled = True
        email = self.email_field.value
        password = self.password_field.value

        if not email or not password:
            self.error_message_text_ref.current.value = "Please enter both email and password."
            self.bs.open = True
            self.page.update()
            return

        self.loading_indicator.visible = True
        self.page.update()

        user, error = sign_in(email, password)

        self.loading_indicator.visible = False
        self.signInBtn.disabled = False
        self.page.update()

        if user:
            self.page.session.set("userId",user.id)
            userProfile = get_profile_data(user.id)
            self.page.session.set("userProfile",userProfile)
            self.page.session.set("email",user.email)
            self.page.client_storage.set("credentials",[email, password])  # Save credentials in session
            on_login_success(self, user.model_dump_json())
        else:
            self.error_message_text_ref.current.value = f"Sign-in failed: {error}"
            self.bs.open = True
            self.page.update()

    
