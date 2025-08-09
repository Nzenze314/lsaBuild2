import flet as ft
from components.base_view import BaseView

class AboutView(BaseView):
    def __init__(self, page):
        super().__init__(page)
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.bgcolor = ft.Colors.SURFACE_TINT
        self.font = "Bungee-Regular"
        self.font2 = "Grand Hotel"
        self.defultFont = "Roboto"

    def build(self):
        return ft.View(
            route="/about",
            appbar=ft.AppBar(
                title=ft.Text("About ", font_family=self.font,
                          weight=ft.FontWeight.W_100, size=20,color=ft.Colors.with_opacity(0.5,ft.Colors.PRIMARY),
                          style=ft.TextStyle(shadow=ft.BoxShadow(spread_radius=1,
                            blur_radius=2,color="white",
                            offset=ft.Offset(0, 0.4),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ))),
                leading=ft.IconButton(
                    icon=ft.Icons.ARROW_BACK,
                    on_click=lambda _: self.page.go("/profile")
                )
            ),
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "LSA Chatbot App",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                font_family=self.font
                            ),
                            ft.Text(
                                "Version 0.9.5",
                                size=16,
                                color=ft.Colors.GREY_600
                            ),
                            ft.Divider(),
                            ft.Text(
                                "This application is designed to provide an interactive chat experience powered by AI for the sharing of institutional knowleage and assist in research.",
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Text(
                                "Developed with Flet v 0.28.3 and Supabase. \n By Engr. Nzenze Lovis of LSS",
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Divider(),
                            ft.Text(
                                "For support or feedback, please contact us. \n +237652028930 \n lsasupport@gmail.com",
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=20
                )
            ]
        )
