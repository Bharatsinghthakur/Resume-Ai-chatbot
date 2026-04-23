import streamlit as st
import requests
import json

st.title("AI Interviewer Bot")

# session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None


# upload resume
uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file


# chat input
user_input = st.chat_input("Ask something about your resume...")

if user_input and st.session_state.uploaded_file:

    file = st.session_state.uploaded_file

    # 🔥 IMPORTANT: reset file pointer
    file.seek(0)

    files = {
        "file": (file.name, file, file.type)
    }

    data = {
        "user_input": user_input,
        "chat_history": json.dumps(st.session_state.chat_history)
    }

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        files=files,
        data=data
    )

    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    if response.status_code == 200:
        try:
            bot_reply = response.json().get("reply", "No reply")
        except:
            st.error("Invalid JSON response")
            bot_reply = "Error parsing response"
    else:
        st.error(response.text)
        bot_reply = "Backend error"

    # update chat history
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )
    st.session_state.chat_history.append(
        {"role": "assistant", "content": bot_reply}
    )


# display chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])