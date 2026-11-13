
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client()

SYSTEM = open("oggy_persona.txt").read()

st.title("🐱 OggyBot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Oggy se baat karo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Convert messages into Gemini format
    history = [
        {
            "role": "user" if m["role"] == "user" else "model",
            "parts": [{"text": m["content"]}]
        }
        for m in st.session_state.messages
    ]

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=history,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM,
            max_output_tokens=300,
        ),
    )

    reply = response.text

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)

