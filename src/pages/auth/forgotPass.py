# views/forgot_password.py
import flet as ft
from components.base_view import BaseView
from components.authFunctions import reset_password

class ForgotPasswordView(BaseView):
    def __init__(self, page):
        super().__init__(page)
        self.message_text_ref = ft.Ref[ft.Text]()

    def build(self):
        self.email_field = ft.TextField(label="Enter your email", prefix_icon=ft.Icons.EMAIL,
                             border_radius=ft.border_radius.all(16), height=55, color=ft.Colors.WHITE,
                             label_style=ft.TextStyle(color=ft.Colors.WHITE))

        self.bs = ft.BottomSheet(
            ft.Container(
                ft.Column(
                    [
                        ft.Text("Password Reset", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                        ft.Text("Check your email for the password reset link.", size=14, color=ft.Colors.WHITE, ref=self.message_text_ref),
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
            route="/forgotpassword",
            padding=0,
            controls=[
                ft.Stack([
                    ft.Image(src="/images/bgSup2.jpg", fit=ft.ImageFit.COVER, expand=True),
                    ft.Container(
                        expand=True,
                        content=ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    padding=ft.padding.symmetric(horizontal=20, vertical=30),
                                    border_radius=ft.border_radius.all(30),
                                    bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.PURPLE_800),
                                    blur=12,
                                    content=ft.Column(
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        spacing=10,
                                        controls=[
                                            ft.Text("Forgot Password", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
                                            ft.Text("Enter your email to reset password", size=14, color=ft.Colors.WHITE),
                                            self.email_field,
                                            ft.ElevatedButton("Send Reset Link", width=300, on_click=self.handle_reset_password),
                                            self.loading_indicator,
                                            ft.TextButton("Back to Sign In", on_click=lambda _: self.page.go("/signin"))
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ],alignment=ft.alignment.center
                )
            ]
        )

    def bs_dismissed(self):
        self.bs.open = False
        self.page.update()

    def handle_reset_password(self, e):
        email = self.email_field.value

        if not email:
            self.message_text_ref.current.value = "Please enter your email."
            self.bs.open = True
            self.page.update()
            return

        self.loading_indicator.visible = True
        self.page.update()

        success, error = reset_password(email)

        self.loading_indicator.visible = False
        self.page.update()

        if success:
            self.message_text_ref.current.value = "Password reset link sent to your email."
        else:
            self.message_text_ref.current.value = f"Password reset failed: {error}"
        
        self.bs.open = True
        self.page.update()
