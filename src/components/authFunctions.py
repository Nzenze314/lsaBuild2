import flet as ft
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Supabase URL and Anon Key must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def on_login_success(self, user_data):
    self.page.session.set("user", user_data)  # Save user session
    
    self.page.go("/home")  # Redirect to signin

def getConvos(userId):
    # Get conversations for the user
    try:
        response = supabase.table("conversations").select("*").eq("sender",userId).order("time", desc=True).execute()
        if response.data:
            
            return response.data
        else:
            return []
    except Exception as er:
        print(er)
        return []
    
def createNewChat(page,data):
    response = supabase.table('conversations').insert(data).execute()  # Create a new conversation with user..........
    if response.data:
        
        page.session.set("current_conversation_id",response.data[0]['id'])   # save new convo in session..............
        print("New conversation created:", page.current_conversation_id)
        return page.current_conversation_id
    else:
        print("Error creating conversation:", response.error)
        return None
    
def deleteChat(chatId):
    try:
        res = supabase.table('conversations').delete().eq("id",chatId).execute()
        if res.data:
            return True
        raise Exception()
    except Exception as er:

        print(f'{er}')
        return
    
def getMessagesOfConvo(convoId):
    # Get messages for the conversation
    try:
        response = supabase.table("messages").select("*").eq("convo_id",convoId).execute()
        if response.data:
            return response.data
        else:
            return []
    except Exception as er:
        print(er)
        return []

def sign_up(email, password,name):
    try:
        res = supabase.auth.sign_up({"email":email, "password":password})
        # Create user profile in the database
        createUser = supabase.table('profiles').insert({"id": res.user.id,"username":name, "email": email}).execute()
        if not createUser.data:
            raise Exception("Failed to create user profile in database")
        return res.user, None
    except Exception as e:
        return None, str(e)

def sign_in(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email":email, "password":password})
        
        return res.user, None
    except Exception as e:
        return None, str(e)
    
def get_profile_data(userId):
    try:
        res = supabase.table("profiles").select("*").eq("id",userId).execute()
        if res.data:
            return res.data[0]
        else:
            return []
    except Exception as er:
        print(f'{er}')
        return [], str(er)

def reset_password(email):
    try:
        supabase.auth.reset_password_for_email(email)
        return True, None
    except Exception as e:
        return False, str(e)
    
def submitReview(data):
    try:
        res = supabase.table("feedbacks").insert(data).execute()
        if res.data:
            return res
        else:
            return None
    except Exception as er:
        print(f'{er}')
        return None

def logout(self, e):
    print('logging the user out')
    self.page.session.clear()
    self.page.go("/signin")
