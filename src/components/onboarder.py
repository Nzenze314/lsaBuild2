import flet as ft
from .base_view import BaseView

class OnboardingView(BaseView):
    def __init__(self, page: ft.Page):
        super().__init__(page)

        # Declare internal onboarding content and images
        self.content = [
           ["Welcome to the LSA app", "Your AI-powered guide for all things Landmark and research"],
            ["Powered by cutting-edge AI and cloud technologies","Meet Zylla, Your personal assitant and research buddy"],
            ["Got a question", "Zylla's got you covered! Fast, reliable, and always up-to-date"],
            ["Now then", "Let's begin"]
        ]
        self.images = [
            "images/onBoard1.jpg",
            "images/onBoard1.jpg",
            "images/onBoard1.jpg",
            "images/onBoard1.jpg"
        ]
        self.total_pages = len(self.content)
        self.index = 0
        self.font = "Bungee-Regular"

        # UI Elements
        self.title_text = ft.Text(self.content[0][0], size=24, font_family=self.font, weight=ft.FontWeight.W_100,text_align=ft.TextAlign.CENTER)
        self.subtitle_text = ft.Text(self.content[0][1], size=16, text_align=ft.TextAlign.CENTER)
        self.image = ft.Image(src=self.images[0], expand=6, fit=ft.ImageFit.COVER)
        self.dots = self._build_dots()

    def _build_dots(self):
        return ft.Row(
            controls=[
                ft.Container(
                    width=10,
                    height=10,
                    border_radius=5,
                    bgcolor=ft.Colors.PRIMARY if i == 0 else ft.Colors.GREY_300,
                ) for i in range(self.total_pages)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=5,
        )

    def _update_content(self):
        self.title_text.value = self.content[self.index][0]
        self.subtitle_text.value = self.content[self.index][1]
        self.image.src = self.images[self.index]

        for i, dot in enumerate(self.dots.controls):
            dot.bgcolor = ft.Colors.PRIMARY if i == self.index else ft.Colors.GREY_300

        self.page.update()

    def _next(self, _):
        if self.index < self.total_pages - 1:
            self.index += 1
            self._update_content()
        else:
            self.page.client_storage.set("onboarding_completed", True)
            self.page.go("/signin")

    def _back(self, _):
        if self.index > 0:
            self.index -= 1
            self._update_content()

    def _skip(self, _):
        self.index = self.total_pages - 1
        self._update_content()

    def build(self) -> ft.View:
        return ft.View(
            route="/onboarding",
            controls=[
                ft.Container(
                    content=ft.Column(
                        [
                            self.title_text,
                            self.image,
                            self.subtitle_text,
                            self.dots,
                            ft.Row(
                                [
                                    ft.TextButton("Back", on_click=self._back),
                                    ft.TextButton("Skip", on_click=self._skip),
                                    ft.FilledButton("Next", on_click=self._next),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True
                    ),expand=True
                )
            ],vertical_alignment=ft.MainAxisAlignment.SPACE_EVENLY
        )
