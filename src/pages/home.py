import flet as ft
from components.base_view import BaseView
from components.authFunctions import getConvos, supabase, logout
import datetime
import requests
import json

from components.drawer import SideBar
from components.alert import AlertBox # Import httpx

class HomeView(BaseView):
    def __init__(self, page):
        super().__init__(page)
        self.page.padding = 0
        self.page.scroll = ft.ScrollMode.ADAPTIVE
        self.page.bgcolor = ft.Colors.SURFACE_TINT
        self.font = "Bungee-Regular"
        self.font2 = "Grand Hotel"
        self.defultFont = "Roboto"
        self.current_conversation_id = self.get_or_create_conversation 
        self.user_id = self.page.session.get("userId")
        self.user_email = self.page.session.get("email")
        self.alert_box = AlertBox(page)

        self.drawer = SideBar(self.page, self.handle_conversation_change)

    def handle_logout(self, e):
        logout(self, e)

    def user_avatar(self):
        # Placeholder for user avatar, will fetch from profile later
        return ft.Container(
                    content=ft.Image(src="images/fox.png", fit=ft.ImageFit.COVER,expand=True ),
                    border_radius=20,width=40,height=40
                )

    def messageBubble(self, text,is_user=False, img_src=None,is_header=True):
        """Creates a message bubble with optional image and avatar."""
        try:
            currentTime = datetime.datetime.now().strftime("%H:%M")
            avatar =self.user_avatar()
            ai_respond = ft.Markdown(
                value=text,
                extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                on_tap_link=lambda e: print(f"Link tapped: {e.data}")
            )
            defultMessage = ft.Text(text, size=16, font_family=self.font if is_header else "", 
                color=ft.Colors.with_opacity(0.7,ft.Colors.PRIMARY_CONTAINER) if is_header else ft.Colors.BLACK ,text_align=ft.TextAlign.CENTER if is_header else ft.TextAlign.START,
                    style=ft.TextStyle(shadow=ft.BoxShadow(spread_radius=1,
                        blur_radius=6,
                        color=ft.Colors.WHITE,
                        offset=ft.Offset(0, 0),
                        blur_style=ft.ShadowBlurStyle.OUTER,
                        ))
                    )
            if not is_user:
                img = ft.Image(src = "images/botHello.png",height=120,fit=ft.ImageFit.COVER) if is_header else ft.Text(height=0)

                return ft.Container(
                    content=ft.Column(
                        [   
                            img,
                            defultMessage if is_header else ai_respond
                        ],alignment=ft.MainAxisAlignment.CENTER,horizontal_alignment=ft.CrossAxisAlignment.CENTER if is_header else ft.CrossAxisAlignment.START
                    ),alignment=ft.alignment.center if is_header else ft.alignment.top_left
                )
            else:
                return ft.Container(
                content=ft.Row(
                    [
                        ft.Container(
                            ft.Column(
                                [
                                    ft.Text(text, size=15, color=ft.Colors.GREY_800,expand=7,text_align=ft.TextAlign.RIGHT,),
                                    ft.Text(currentTime, size=7, color=ft.Colors.GREY_500,expand=1) # TODO: Replace with actual timestamp
                                ],horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),alignment=ft.alignment.bottom_right,bgcolor=ft.Colors.ON_SECONDARY_CONTAINER,
                            border_radius=ft.border_radius.only(top_left=20,top_right=10,bottom_left=20,bottom_right=0),
                            padding=ft.padding.all(5),width=len(text) * 8 + 20, # This width calculation might need adjustment
                        )
                    ],vertical_alignment=ft.CrossAxisAlignment.END,alignment=ft.MainAxisAlignment.END,wrap=True
                ),
                padding=ft.padding.all(5),
                alignment=ft.alignment.bottom_right if is_user else ft.alignment.bottom_left,
            
            )
        except Exception as er:
            print(f'{er}')

    def handle_conversation_change(self, convo_id):
        try:
            self.current_conversation_id = convo_id
            self.page.session.set("current_conversation_id", convo_id)
            
            # Clear current messages and load existing messages of selected conversation if any...
            self.chat_messages.controls.clear()
            self.load_conversation_messages()
            self.page.close(self.drawer)

            self.page.update()
        except Exception as er:
            print(f'{er}')




    def fetch_user_data(self): # Removed async
        try:
            user_session_str = self.page.session.get("user")
            if user_session_str:
                user_data = json.loads(user_session_str)
                self.user_id = user_data.get("id")
                self.user_email = user_data.get("email")
                print(f"User ID: {self.user_id}, Email: {self.user_email}")
                # You can fetch profile data here if needed
                # try:
                #     response = supabase.from_('profiles').select('*').eq('id', self.user_id).single().execute()
                #     if response.data:
                #         self.user_profile = response.data
                #         print("User profile:", self.user_profile)
                # except Exception as e:
                #     print(f"Error fetching profile: {e}")
            else:
                print("No user session found, redirecting to signin.")
                self.page.go("/signin")
            self.page.update()
        except Exception as er:
            print(f'{er}')

    def save_message(self, conversation_id, sender, content): # Removed async
        try:
            data = {
                "convo_id": str(conversation_id),
                "sender": str(sender),
                "content": content,
                
            }
            response = supabase.table('messages').insert(data).execute() # Save message to database..
            if response.data:
                # print("Message saved:", response.data)
                return response.data[0]
            else:
                print("Error saving message:", response.error)
                return None
        except Exception as e:
            print(f"Exception saving message: {e}")
            return None
        
    def load_conversation_messages(self):
        self.get_or_create_conversation
        try:
            if not self.current_conversation_id:
                return

            response = supabase.table("messages") \
                .select("*") \
                .eq("convo_id", self.current_conversation_id) \
                .order("time") \
                .execute()

            messages = response.data if response.data else []

            self.chat_messages.controls.clear()
            
            for msg in messages:
                
                user = False if msg.get("sender") == "bot" else True
                self.chat_messages.controls.append(
                    self.messageBubble(
                        msg.get("content", ""),
                        is_user=user,is_header=False
                    )
                )

            self.page.update()

        except Exception as er:
            print(f'{er}')
            


    def get_or_create_conversation(self): # Removed async

        if self.page.session.get("current_conversation_id"):
            return self.page.session.get("current_conversation_id")
        
        # For simplicity, let's create a new conversation for each session for now
        # In a real app, you might query existing conversations for the user
        try:
            data = {
                "sender": str(self.user_id)
            }
            response = supabase.table('conversations').insert(data).execute()  # Create a new conversation with user..........
            if response.data:
                self.current_conversation_id = response.data[0]['id']
                self.page.session.set("current_conversation_id",response.data[0]['id'])   # save new convo in session..............
                print("New conversation created:", self.current_conversation_id)
                return self.current_conversation_id
            else:
                print("Error creating conversation:", response.error)
                return None
        except Exception as e:
            print(f"Exception creating conversation: {e}")
            return None

    def chat_with_ai_server(self, message):
        print(f"Sending message to AI server: {message}")
        try: 
            # Replace with your actual AI server endpoint
            response = requests.post("https://zylla.onrender.com/askZylla/text", json={"question": message})
            response.raise_for_status()  # Raise an exception for HTTP errors
            # print(response.json())
            return response.json().get("response", "Sorry, I couldn't process that.")
        
        except requests.RequestException as e:
            print(f"HTTP request failed: {e}")
            return "Sorry, I couldn't connect to the internet."
        
        except requests.HTTPError as e:
            print(f"HTTP status error: {response.status_code} - {response.text}")
            return f"AI server error: {response.status_code}"
        
        except Exception as e:
            print(f"An unexpected error occurred during AI chat: {e}")
            return "An unexpected error occurred."


    def build(self):
        # App bar with avatar
        App_bar = ft.AppBar(
            leading=ft.IconButton(
                icon=ft.Icons.MENU,icon_color=ft.Colors.PRIMARY,
                on_click=lambda _: self.toggle_drawer()
            ),
            title=ft.Text("LSA Chatbot",font_family=self.font,
                          weight=ft.FontWeight.W_100, size=20,color=ft.Colors.with_opacity(0.5,ft.Colors.PRIMARY),
                          style=ft.TextStyle(shadow=ft.BoxShadow(spread_radius=1,
                                            blur_radius=2,color="white",
                                            offset=ft.Offset(0, 0.4),
                                            blur_style=ft.ShadowBlurStyle.OUTER,
                                            ))
                          ),
            center_title=False,
            bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.ON_TERTIARY_CONTAINER),
            actions=[
                ft.Container(
                    margin=ft.margin.only(right=10),
                    content=self.user_avatar(),
                    on_click= lambda _: self.page.go('/profile')
                )
            ]
        )

        # Chat messages area
        self.chat_messages = ft.ListView(
            expand=True,
            # height=self.page.window.height - 185,  # Adjust height based on app bar
            auto_scroll=True,
            spacing=5,
            padding=ft.padding.all(5),
            controls=[
                self.messageBubble('Hi there, what can i help you with today',is_header=True,is_user=False)
            ]
        )

        # Message input area
        self.message_text_field = ft.TextField(
            expand=True,
            hint_text="Type your message...",
            border_radius=ft.border_radius.all(16)
        )
        message_input = ft.Container(
            padding=ft.padding.all(10),
            content=ft.Row(
                controls=[
                    self.message_text_field,
                    ft.IconButton(
                        icon=ft.Icons.SEND,
                        icon_color="primary",
                        on_click=self.send_message
                    )
                ],
                spacing=10,expand=2
            )
        )

        # Main content filling the screen
        main_content = ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    content=self.chat_messages,
                    expand=8
                ),
                message_input
            ]
        )

        

        return ft.View(
            route="/home",
            appbar=App_bar,
            drawer=self.drawer,
            controls=[ft.Container(
                content=main_content,
                expand=True,
                padding=0,
                margin=0
            )],
            spacing=0,vertical_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

    def toggle_drawer(self):
        self.drawer.open = not self.drawer.open
        self.page.update()

    def send_message(self, e):
        e.control.disable = True
        message_text = self.message_text_field.value.strip()
        self.message_text_field.value = "" # Clear input immediately
        self.page.update()

        if not message_text:
            e.control.disable = False
            return

        # Display user message
        self.chat_messages.controls.append(
            self.messageBubble(message_text, is_user=True,is_header=False)
        )
        self.page.update()
        self.chat_messages.controls.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.ProgressRing()
                    ],alignment=ft.MainAxisAlignment.START
                )
            )
        )
        self.page.update()

        # Get or create conversation
        if not self.current_conversation_id:
            self.fetch_user_data() # Ensure user_id is set
            if not self.user_id:
                print("User not authenticated, cannot create conversation.")
                e.control.disable = False
                return
            self.current_conversation_id = self.get_or_create_conversation
            if not self.current_conversation_id:
                print("Failed to get or create conversation.")
                e.control.disable = False
                return

        # Save user message to Supabase
        self.save_message(self.current_conversation_id, self.user_id, message_text)
        
        # Get AI response
        ai_response = self.chat_with_ai_server(message_text)

        
        self.chat_messages.controls.pop()
        # Display AI response
        self.chat_messages.controls.append(
            self.messageBubble(ai_response, is_user=False,is_header=False)
        )
        e.control.disable = False
        self.page.update()

        # Save AI response to Supabase
        self.save_message(self.current_conversation_id, "bot", ai_response) # Assuming AI messages are also linked to user_id for conversation context
