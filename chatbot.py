import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Automatically reads GROQ_API_KEY from your .env file
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM = open("oggy_persona.txt", encoding="utf-8").read()

st.title("🐱 OggyBot (Powered by Groq)")

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.chat_message(m["role"]).write(m["content"])

if prompt := st.chat_input("Oggy se baat karo..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Pass the system prompt first, followed by conversation history
    messages_payload = [{"role": "system", "content": SYSTEM}] + [
        {"role": m["role"], "content": m["content"]}
        for m in st.session_state.messages
    ]

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",  # Fast, high-quality model on Groq's free tier
            messages=messages_payload,
            max_tokens=300,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"*Arre yaar!* Kuch gadbad ho gayi: `{e}`"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.chat_message("assistant").write(reply)
