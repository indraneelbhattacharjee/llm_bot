import streamlit as st
import shelve
from bot import bot_response

# Set up a title for the Streamlit app
st.title("Personal Assistant")

USER = "👤"
BOT = "🤖"

# Load chat history from shelve
def load_chat_history():
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve
def save_chat_history(messages):
    with shelve.open("chat_history") as db:
        db["messages"] = messages

# Initialize or load chat history from session state
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

# Sidebar with an option to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        # Clear chat history from session state
        st.session_state.messages = []
        # Clear chat history from shelve database
        save_chat_history([])

# Display chat messages
for message in st.session_state.messages:
    avatar = USER if message["role"] == "user" else BOT
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Main chat interface for user input
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER):
        st.markdown(prompt)
        
    with st.chat_message("assistant", avatar=BOT):
        # Generate bot's response using the bot_response function
        response = bot_response(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Save chat history after every interaction
save_chat_history(st.session_state.messages)
