import flet as ft

def AlertBox(content):
    """
    Class to create dynamic, reuseable alert box
    """
    if isinstance(content, str) and content.lower() == "loading":
        return ft.AlertDialog(
                    modal=True,
                    title = ft.Text("One moment", weight=ft.FontWeight.BOLD),
                    content=ft.Row(
                        controls=[
                            ft.ProgressRing(),
                            ft.Text("Please wait...", size=14),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    shape=ft.RoundedRectangleBorder(radius=10),
                 )
    else:
        return ft.AlertDialog(
                    title = ft.Text("Alert", weight=ft.FontWeight.BOLD),
                    content=ft.Text(content),
                    shape=ft.RoundedRectangleBorder(radius=10),
                    
                 )
