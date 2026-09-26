import ollama
import streamlit as st
st.title("Welcome to ChatBot App!!")
with st.sidebar:
    uploaded_file=st.file_uploader("upload a text file..")
    if uploaded_file:
        st.write("FIle uploaded successfully")
        context=uploaded_file.read().decode("utf-8")
        st.text(context)
if "msgs" not in st.session_state:
    st.session_state.msgs = []
for msg in st.session_state.msgs:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
question = st.chat_input("You:")
if question:
    st.session_state.msgs.append({
        "role": "user",
        "content": question
    })
    with st.chat_message("user"):
        st.write(question)
    with st.spinner("Thinking..."):
        response = ollama.chat(
            model="llama3.2:3b",
            messages=st.session_state.msgs
        )
    answer = response["message"]["content"]
    st.session_state.msgs.append({
        "role": "assistant",
        "content": answer
    })
    with st.chat_message("assistant"):
        st.write(answer)