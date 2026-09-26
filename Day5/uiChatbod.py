import streamlit as st
import ollama
from pypdf import PdfReader
from docx import Document
st.title("🤖 My AI ChatBot")
st.subheader("Welcome! Ask me anything.")
st.badge("✨ Nice to chat with you")
if "messages" not in st.session_state:
    st.session_state.messages = []
if "file_text" not in st.session_state:
    st.session_state.file_text = ""
if "file_name" not in st.session_state:
    st.session_state.file_name = ""
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
prompt = st.chat_input(
    "💬 Type your question or upload a file...",
    accept_file=True,
    file_type=["txt", "pdf", "docx"]
)
if prompt:
    question = prompt.text
    files = prompt.files
    if files:
        for file in files:
            st.write("📎 Uploaded:", file.name)
            file_name = file.name.lower()
            if file_name.endswith(".pdf"):
                pdf = PdfReader(file)
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                st.session_state.file_text = text
                st.session_state.file_name = file.name
            elif file_name.endswith(".txt"):
                text = file.read().decode("utf-8")
                st.session_state.file_text = text
                st.session_state.file_name = file.name
            elif file_name.endswith(".docx"):
                document = Document(file)
                text = ""
                for paragraph in document.paragraphs:
                    text += paragraph.text + "\n"
                st.session_state.file_text = text
                st.session_state.file_name = file.name
            if st.session_state.file_text:
                st.success(
                    f" {file.name} read successfully!"
                )
                st.info(
                    f"📄 Characters extracted: "
                    f"{len(st.session_state.file_text)}"
                )
            else:
                st.error(
                    "Could not extract text from this file."
                )
    if question:
        st.session_state.messages.append({
            "role": "user",
            "content": question
        })
        with st.chat_message("user"):
            st.write(question)
        if st.session_state.file_text:
            file_content = st.session_state.file_text
            ai_prompt = f""" 
You are an AI assisstant.
The user has uploaded a file name:
{st.session_state.file_name}
Here is the content of the file:
{file_content}
The user's question is:
{question}
Answer the user's question based on the uploaded file 
If the answer is not available in the file ,clearlg say so
"""
            messages = [
                {
                    "role": "user",
                    "content": ai_prompt
                }
            ]
        else:
            messages = st.session_state.messages
        with st.chat_message("assistant"):
            with st.spinner("Reading file and thinking..."):
                try:
                    response = ollama.chat(
                        model="llama3.2:3b",
                        messages=messages
                    )
                    answer = response["message"]["content"]
                except Exception as e:
                    answer = f"Error: {e}"
            st.write(answer)
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })