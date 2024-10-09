import streamlit as st
import uuid

base_request_url = "https://cf61-207-188-8-20.ngrok-free.app"

def generate_task_id():
    return str(uuid.uuid4())

key_dict = dict(st.secrets["GOOGLE_CLOUD_CREDENTIALS"])
key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]["value"]
zenrowsApiKey = st.secrets["ZENROWS_API_KEY"]["value"]
OWLER_PC_cookie = st.secrets["OWLER_PC_COOKIE"]["value"]