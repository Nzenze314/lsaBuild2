import flet as ft

# Base View class
class BaseView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self) -> ft.View:
        raise NotImplementedError("Each view must implement its own build method.")