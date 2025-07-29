import flet as ft
from components.onboarder import OnboardingView



ROUTES = ["/", "/store", "/favorites", "/home"]

def BottomNavigationBar(page: ft.Page):
    def change_route(e):
        selected_index = e.control.selected_index
        new_route = ROUTES[selected_index]
        page.go(new_route)

    return ft.NavigationBar(
        selected_index=ROUTES.index(page.route) if page.route in ROUTES else 0,
        on_change=change_route,
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.STORE, label="Store"),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Favorites",
            ),
            ft.NavigationBarDestination(icon=ft.Icons.INFO, label="Onboarding"),
        ]
    )

# Base View class
class BaseView:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self) -> ft.View:
        raise NotImplementedError("Each view must implement its own build method.")

# Home View
class HomeView(BaseView):
    def build(self):
        return ft.View(
            route="/home",
            controls=[
                ft.AppBar(title=ft.Text("Home"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                ft.Text("Welcome to the Home Page!"),
                ft.ElevatedButton("Go to Store", on_click=lambda _: self.page.go("/store")),
            ],
            bottom_appbar=BottomNavigationBar(self.page)
        )

# Store View
class StoreView(BaseView):
    def build(self):
        return ft.View(
            route="/store",
            controls=[
                ft.AppBar(title=ft.Text("Store"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                ft.Text("This is the Store."),
                ft.ElevatedButton("Go Back Home", on_click=lambda _: self.page.go("/")),
            ],
            bottom_appbar=BottomNavigationBar(self.page)
        )

# Favorites View
class FavoritesView(BaseView):
    def build(self):
        return ft.View(
            route="/favorites",
            controls=[
                ft.AppBar(title=ft.Text("Favorites"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                ft.Text("Your saved favorites."),
                ft.ElevatedButton("Go Back Home", on_click=lambda _: self.page.go("/")),
            ],
             bottom_appbar=BottomNavigationBar(self.page)
        )

# NotFound View
class NotFoundView(BaseView):
    def build(self):
        return ft.View(
            route="/404",
            controls=[
                ft.AppBar(title=ft.Text("Not Found"), bgcolor=ft.Colors.ERROR),
                ft.Text("Oops! Page not found."),
                ft.ElevatedButton("Go Home", on_click=lambda _: self.page.go("/")),
            ]
        )

# Router
class Router:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_view(self, route: str) -> ft.View:
        route_map = {
            "/home": HomeView,
            # "/store": StoreView,
            # "/favorites": FavoritesView,
            "/": OnboardingView
        }
        view_class = route_map.get(route, NotFoundView)
        return view_class(self.page).build()

# Main App
class MyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.router = Router(page)

    def main(self):
        self.page.title = "Mobile Flet App"
        self.page.window.width = 350
        self.page.window.height = 600
        self.page.window.resizable = False
        self.page.window.always_on_top = True
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop
        self.page.go(self.page.route)

    def route_change(self, route):
        
        self.page.views.clear()
        view = self.router.get_view(self.page.route)
        self.page.views.append(view)
        self.page.update()

    def view_pop(self, view):
        self.page.views.pop()
        if self.page.views:
            self.page.go(self.page.views[-1].route)

# Run
def run(page: ft.Page):
    app = MyApp(page)
    app.main()

ft.app(target=run, view=ft.AppView.FLET_APP,assets_dir="assets")
