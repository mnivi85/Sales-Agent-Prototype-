
import streamlit as st
import json
from groq import Groq

# Groq Client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Filepath for chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Function to load chat history
def load_chat_history():
    try:
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return [{"role": "assistant", "content": "Hello"}]  # Default message
    except json.JSONDecodeError:
        return [{"role": "assistant", "content": "Hello"}]  # Reset on error

# Function to save chat history
def save_chat_history(chat_history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(chat_history, file)

# Load chat history into session state
if "message" not in st.session_state:
    st.session_state["message"] = load_chat_history()

print('Session State: ', st.session_state)

# Set a default model
if "default_model" not in st.session_state:
    st.session_state["default_model"] = "llama3-8b-8192"

# Set a message collection
if "message" not in st.session_state:
    st.session_state["message"] = [
        {"role": "assistant", "content": "Hello"}
    ]

# Sidebar
st.sidebar.title('Chat')
st.sidebar.slider("Temperature", 0, 2)

# Page Header
st.title('Chat')
st.write('Chatbot powered by Groq')
st.divider()

# Display the Messages
for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input():
    # Add user message to the messages collection
     st.session_state.message.append({"role": "user", "content": prompt})
    
    # Display the user message
     with st.chat_message('user'):
        st.write(prompt)
    
    # Assistant message container
     with st.chat_message("assistant"):
        response_text = st.empty()
        
        # Make the API call to Groq
        completion = client.chat.completions.create(
            model=st.session_state.default_model,
            stream=True,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.message
            ]
        )
        
        # Display each chunk of text
        full_response = ""
        for chunk in completion:
            full_response += chunk.choices[0].delta.content or ""
            response_text.write(full_response)
        
        # Add the assistant message to the messages collection
        st.session_state.message.append({"role": "assistant", "content": full_response})
    
    # Save the chat history
     save_chat_history(st.session_state.message)
