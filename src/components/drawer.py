import datetime
import json
from dateutil import parser
import flet as ft
import pytz

from components.authFunctions import createNewChat, deleteChat, getConvos, logout

class SideBar(ft.NavigationDrawer):

    def readable_time(self,iso_str):
            dt = parser.parse(iso_str).astimezone(pytz.timezone("Africa/Douala"))
            return dt.strftime("%m/%d/%Y, %I:%M %p")  # Adjust format as needed
    
    def select_conversation(self, convo_id):
        self.page.session.set("current_conversation_id", convo_id)
        if self.on_convo_selected:
            self.on_convo_selected(convo_id)

    def startNewChat(self,e):
        try:
            data = {
                "sender": str(self.user_id)
            }
            print("Starting a new chat")
            conviId = createNewChat(self.page,data)
            self.select_conversation(conviId)
            self.update_convos(e)
            self.page.close(self)
            self.page.update()
        except Exception as er:
            return
        

    def deleteConvo(self,e):
        print("Deleting conversation...")
        self.page.close(self)
        id = e.control.data
        if deleteChat(id):
            self.update_convos(e)
            self.page.update()      
        else:
            print("Deleting conversation...")
            self.page.close(self)

          

    def __init__(self, page: ft.Page, on_convo_selected=None):
        super().__init__()
        self.page = page
        self.font = "Bungee-Regular"
        self.on_convo_selected = on_convo_selected

        user_session_str = self.page.session.get("user")
        if user_session_str:
            user_data = json.loads(user_session_str)
            self.user_id = user_data.get("id")
            self.user_email = user_data.get("email")
        convos = getConvos( self.user_id)
        

        # print(convos)
        if len(convos) > 0:
            self.page.session.set("current_conversation_id",convos[0]["id"])
        else:
            createNewChat(page,{"sender":self.user_id})
             

        self.convos_list = ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                          [
                            ft.Text(f"You - {self.readable_time(conv['time'])}", color=ft.Colors.WHITE),
                            ft.IconButton(
                                  icon=ft.Icons.DELETE,icon_color=ft.Colors.WHITE, data=conv["id"],
                                  on_click= lambda e: self.deleteConvo(e),
                            )
                          ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    bgcolor=ft.Colors.PURPLE_300,
                    border_radius=8,
                    data=conv["id"],
                    padding=6,
                    margin=ft.margin.symmetric(horizontal=16, vertical=0),
                    on_click=lambda e: self.select_conversation(e.control.data),
                )
                for conv in convos
            ],horizontal_alignment=ft.CrossAxisAlignment.STRETCH, height=self.page.height * 0.4,
            scroll=ft.ScrollMode.AUTO
        )            

        self.bgcolor = ft.Colors.PURPLE_600
        self.controls = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text("Zylla ", spans=[
                            ft.TextSpan(
                                "v 0.9",style=ft.TextStyle(size=12,color=ft.Colors.ON_PRIMARY)
                            )
                        ], size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, font_family=self.font),
                        ft.IconButton(
                            ft.Icons.CLOSE,icon_color='white',
                            tooltip="Close",
                            on_click=lambda e: self.page.close(self),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                padding=ft.padding.all(16),
            ),

            ft.Container(
                content=ft.ElevatedButton(
                    "New Chat",
                    icon=ft.Icons.ADD,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.PURPLE_ACCENT,
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=10),
                        padding=ft.padding.symmetric(vertical=10),
                    ),
                    on_click= self.startNewChat,
                ),
                padding=ft.padding.symmetric(horizontal=16),
            ),

            ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Recent", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,icon_color=ft.Colors.WHITE,
                            on_click= self.update_convos
                        )
                    ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN,expand=True
                ),
                padding=ft.padding.only(left=16, top=20, bottom=8),
            ),
            
            self.convos_list,  # Controls COntaining the list of conversations.........

            ft.Container(expand=True),

            ft.Divider(color=ft.Colors.WHITE54),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE),
                title=ft.Text("Manage Profile", color=ft.Colors.WHITE),
                on_click=lambda e: self.page.go("/profile"),
            ),
            ft.ListTile(
                leading=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.WHITE),
                title=ft.Text("Sign-out", color=ft.Colors.WHITE),
                on_click=self.logout,
            ),
            ft.Container(height=12)
        ]

    def logout(self, e):
        logout(self,e)
        self.page.update()

    def update_convos(self,e):
        try:
            print('Updating convos')
            self.convos_list.controls.clear()
            convos = getConvos(self.user_id)
            
            if len(convos) > 0:
                self.convos_list.controls.extend([
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(f"You - {self.readable_time(conv['time'])}", color=ft.Colors.WHITE),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,icon_color=ft.Colors.WHITE, data=conv["id"],
                                    on_click= lambda e: self.deleteConvo(e),
                                )
                            ],alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        bgcolor=ft.Colors.PURPLE_300,
                        border_radius=8,
                        data=conv["id"],
                        padding=6,
                        margin=ft.margin.symmetric(horizontal=16, vertical=0),
                        on_click=lambda e: self.select_conversation(e.control.data),
                    )
                    for conv in convos
                ])
            
            self.page.update()
        except Exception as er:
                print(f'{er}')
                return