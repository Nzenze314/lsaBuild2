import flet as ft

# Import your custom views
from components.onboarder import OnboardingView
from pages.profile import ProfileView
from pages.home import HomeView
from pages.auth.forgotPass import ForgotPasswordView
from pages.auth.signUp import SignUpView
from pages.auth.signIn import SignInView
from theme.app_theme import get_dark_theme, get_light_theme

# Placeholder components for the special views
def getCatNameById(cat_id):
    return f"Category {cat_id}"
 
def Tasks(page, category_id):
    return ft.Text(f"Tasks for category {category_id}") 

def create_task_dialog(page, category_id, task_list):
    return ft.AlertDialog(title=ft.Text(f"Create task for {category_id}"))

def create_fab2(page, dialog):
    return ft.FloatingActionButton(icon=ft.Icons.ADD, on_click=lambda _: page.dialog.open(dialog))

def delDilog(category_id):
    return ft.AlertDialog(title=ft.Text(f"Delete all tasks in category {category_id}?"))

# Base view class
class BaseView:
    def __init__(self, page: ft.Page): 
        self.page = page

    def build(self) -> ft.View:
        raise NotImplementedError("Each view must implement its own build method.") 

class FavoritesView(BaseView):
    def build(self):
        return ft.View(
            route="/favorites",
            controls=[
                ft.AppBar(title=ft.Text("Favorites"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                ft.Text("Your saved favorites."),
                ft.ElevatedButton("Go Back Home", on_click=lambda _: self.page.go("/")),
            ],
        )

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

# Router with stacked view logic
class Router:
    def __init__(self, page: ft.Page):
        self.page = page

    def is_authenticated(self):
        return self.page.session.get("user") is not None

    def get_view_stack(self, route: str) -> list[ft.View]:
        route_map = {
            "/": OnboardingView,
            "/signin": SignInView,
            "/signup": SignUpView,
            "/home": HomeView,
            "/forgotpassword":ForgotPasswordView,
            "/profile": ProfileView,
            "/favorites": FavoritesView, 
            "/onboarding": OnboardingView,  
        }

        stack = [] 
        # stack.append(OnboardingView(self.page).build())  # base
     
        try:
            if route == "/signin":           
                stack.append(SignInView(self.page).build()) 
                stack.append(route_map[route](self.page).build())

            elif route == "/forgotpassword":
                stack.append(ForgotPasswordView(self.page).build()) 
                stack.append(SignInView(self.page).build())

            elif route == "/onboarding":
                stack.append(OnboardingView(self.page).build()) 
   
            elif route == "/home":
                stack.append(HomeView(self.page).build()) 
                
            elif route == "/profile": 
                stack.append(HomeView(self.page).build())  
                stack.append(route_map[route](self.page).build())

            elif route in route_map:
                   
                stack.append(route_map[route](self.page).build())        
    
            else:
                stack.append(NotFoundView(self.page).build())

        except Exception as e:
            print(f"The usual pop error: {e}")

        return stack

# Main App
class MyApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.router = Router(page)
        self.view_stack = []
        self.ai_server = "https://zylla.onrender.com"
        "Mg8CgSgpU7Ep2Gi"

    def toggle_theme_mode(self, e):
        self.page.theme_mode = (
            ft.ThemeMode.DARK
            if self.page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        self.page.update()

    def main(self):  
        self.page.title = "LSA App"     
        self.page.window.width = 350
        self.page.window.height = 600            
        self.page.window.resizable = False
        self.page.window.always_on_top = True
        self.page.padding = ft.padding.all(0)
        self.page.theme_mode = ft.ThemeMode.SYSTEM
        self.page.theme = get_light_theme()
        self.page.dark_theme = get_dark_theme()

        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

        self.page.floating_action_button = ft.FloatingActionButton(
            icon=ft.Icons.DARK_MODE, 
            on_click=self.toggle_theme_mode  
        ) 

        self.page.fonts = {
            "Grand Hotel": "/fonts/GrandHotel-Regular.ttf",
            "Bungee-Regular": "/fonts/Bungee-Regular.ttf",
        }   
        onboardingCompleted = self.page.client_storage.get("onboarding_completed") 

        if onboardingCompleted:     
            self.page.go("/signin")     
             
        self.page.go(self.page.route)    

    def route_change(self, e):
        print(f"[Route Change] → {e.route}") 
        self.page.views.clear()    
        view_stack = self.router.get_view_stack(e.route)
        self.page.views.extend(view_stack)
        self.view_stack = view_stack[:]  # Copy stack  
        print(f"[Route views] → {self.page.views}")          
        # self.page.client_storage.set("route", self.page.views[1])  # Save current route in session
        self.page.update()             

    def view_pop(self, view):
        try:    
            self.page.views.pop()
            if self.page.views:
                top_view = self.page.views[-1] 
                self.page.go(top_view.route)     
        except Exception as er:             
            print(f"The usual pop error! {er}")             
        self.page.update()
    
# Run
def run(page: ft.Page):
    app = MyApp(page)
    app.main()

ft.app(target=run, view=ft.AppView.FLET_APP, assets_dir="assets")     
