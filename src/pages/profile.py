# pages/profile.py
from components.base_view import BaseView
from components.reviewCard import LeaveReviewCard
from components.alert import AlertBox
from components.authFunctions import logout
import flet as ft

class ProfileView(BaseView):
    def __init__(self,page):
        super().__init__(page)
        uuid = self.page.session.get("userId")
        self.profileData = self.page.session.get("userProfile")
        self.font = "Bungee-Regular"
        
    def build(self): 
        appbar = ft.AppBar(
            title=ft.Text("Profile", font_family=self.font,
                          weight=ft.FontWeight.W_100, size=20,color=ft.Colors.with_opacity(0.5,ft.Colors.PRIMARY),
                          style=ft.TextStyle(shadow=ft.BoxShadow(spread_radius=1,
                            blur_radius=2,color="white",
                            offset=ft.Offset(0, 0.4),
                            blur_style=ft.ShadowBlurStyle.OUTER,
                        ))),

        )
        username = self.profileData.get('username', '') if self.profileData else ''
        useremail = self.profileData.get('email', '') if self.profileData else ''

        return ft.View(
            route="/profile",
            appbar=appbar,
            controls=[
                ft.Column(
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                                content=ft.Image(src="images/fox.png", fit=ft.ImageFit.COVER,expand=True ),
                                border_radius=63,width=130,height=130
                            ),
                        ft.Text(str(username), size=22, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        ft.ElevatedButton(
                            text="Edit Profile", icon=ft.Icons.EDIT, bgcolor=ft.Colors.WHITE,
                            on_click=lambda _: self.page.open(AlertBox('Feature not yet implement!!'))
                        ),
                        ft.Container(height=5),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.EMAIL),
                            title=ft.Text('Email'),
                            subtitle=ft.Text(str(useremail)),
                            bgcolor=ft.Colors.GREY_100,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOCATION_ON),
                            title=ft.Text("Location"),
                            subtitle=ft.Text("Buea, Cameroon"),
                            bgcolor=ft.Colors.GREY_100,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.SCHOOL),
                            title=ft.Text("University"),
                            subtitle=ft.Text("Landmark"),
                            bgcolor=ft.Colors.GREY_100,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOCK),
                            title=ft.Text("Change Password"),
                            on_click=lambda _: self.page.open(AlertBox('Feature not yet implement!!')),
                            bgcolor=ft.Colors.GREY_100,
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.STAR),
                            title=ft.Text('Rate this app'),
                            on_click=lambda _: self.page.open(LeaveReviewCard(self.page)),
                            bgcolor=ft.Colors.GREY_100
                        ),
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.INFO),
                            title=ft.Text("About App"),
                            on_click=lambda _: self.page.go("/about"),
                            bgcolor=ft.Colors.GREY_100,
                        ), 
                        ft.ListTile(
                            leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.RED),
                            title=ft.Text("Sign-out", color=ft.Colors.RED),
                            on_click=self.logout
                        ),
                    ],
                )
            ],
           
            scroll=ft.ScrollMode.AUTO,
        )

    def logout(self, e):
        logout(self,e)
        self.page.update()
