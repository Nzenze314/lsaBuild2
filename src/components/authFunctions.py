import flet as ft
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import smtplib
from email.message import EmailMessage
import secrets
import string
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
SUPABASE_URL = "https://jxwljzluygmbogwajkgp.supabase.co" 
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp4d2xqemx1eWdtYm9nd2Fqa2dwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM5NjA1OTUsImV4cCI6MjA2OTUzNjU5NX0.1M7baVwaKrsElXfVN2KQaB4y4qlbnLu4KuPvGwgBTaU"
SERVICE_ROLE_KEY= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imp4d2xqemx1eWdtYm9nd2Fqa2dwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Mzk2MDU5NSwiZXhwIjoyMDY5NTM2NTk1fQ._Ks7WuWZiRNhkP3MaAcjbpkM950fVSaEA0Z9GkQzYWs"

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise ValueError("Supabase URL and Anon Key must be set in .env file")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


supabase2 = create_client(
    SUPABASE_URL,
    SERVICE_ROLE_KEY,
    options=ClientOptions(
        auto_refresh_token=False,
        persist_session=False,
    )
)
# Access auth admin api
supabaseA = supabase2.auth.admin

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
    
def createNewChat(page,data) -> str|None:
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

def send_password_email(to_email, new_password):
    # Sender credentials
    EMAIL_ADDRESS = "ebongloveis@gmail.com"
    EMAIL_PASSWORD = "ouxa nxrj gnwg whmb"  # Use app password if using Gmail

    # Email content
    msg = EmailMessage()
    msg['Subject'] = "Your New Password"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(f"""
            Hello from LSA Support Team,

            Your password has been reset successfully. Here is your new password:

            🔐 Password: {new_password}

            Please log in and change your password as soon as possible.

            Thank you,
            Your Support Team
            """)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print(" Email sent successfully.")
        return True
    except Exception as e:
        print(f" Failed to send email: {e}")
        return False


def generate_secure_password(length=8):
    """Generate a secure random password with letters, digits, and symbols."""
    characters = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(characters) for _ in range(length))
        # Ensure password has at least one letter, digit, and symbol
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password)):
            return password

def reset_password(email):
    new_password = generate_secure_password()

    try:
        response = supabase.table('profiles').select('id').eq('email', email).execute()
        user_data = response.data

        if user_data and len(user_data) > 0:
            user_id = user_data[0]["id"]
            supabaseA.update_user_by_id(user_id, {
                "password": new_password
            })
            send_password_email(email, new_password)
            return True
        else:
            print("User not found.")
            return False
    except Exception as e:
        print(f'There was an error: {e}')
        return False

    
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
    supabase.auth.sign_out()
    print('logging the user out')
    self.page.session.clear()
    self.page.go("/signin")
