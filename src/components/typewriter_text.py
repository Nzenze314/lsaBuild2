import flet as ft
import asyncio


class TypewriterText(ft.Container):
    def __init__(self, text: str, speed: float = 0.03):
        super().__init__()
        self.full_text = text
        self.speed = speed
        self.label = ft.Text(value="", selectable=True)  # Allows copying text

    def build(self):
        return self.label

    def did_mount(self):
        # Run the typing effect asynchronously
        self.page.run_task(self._type_text)

    async def _type_text(self):
        current_text = ""
        for char in self.full_text:
            current_text += char
            self.label.value = current_text
            self.update()
            await asyncio.sleep(self.speed)
