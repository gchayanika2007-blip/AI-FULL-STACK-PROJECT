import ollama
import streamlit as st
st.markdown("# ***Story Generator!!*** ")
st.subheader("*share your story😊*" \
"")
with st.sidebar:
    st.header(":blue[Chat settings]")
    if st.button("Clear chat "):
        st.session_state.msgs = []
        st.success("Chat cleared 🗑️")
    personalities = {
        "Kid👶": " Answer the question like you are explaing to a 5 yeas old kid.Give the answer in 2 line only",
        "Friend 👩‍🦱" :"Answer the question in a friendly way and casual manner. Give the answer in 2 lines only",
        "Father 🧓" : " Answer the question as a father is talling to the daugther.Give in 2 lines only"
    }
    personality= st.selectbox("Select a personality",personalities.keys())
    uploaded_file=st.file_uploader(" 📁 upload a text file..")
    try:
        if uploaded_file:
            st.success("File uploaded successfully")
        if st.button("Display"):
            context=uploaded_file.read().decode("utf-8")
            st.text(context)
    except:
        st.error("File type not supported")
if "msgs" not in st.session_state:
    st.session_state.msgs = []
for msg in st.session_state.msgs:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
question = st.chat_input("💬 Type messages")
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
            messages= [
                {"role": "system",
                 "content": personalities[personality]}]
               + st.session_state.msgs
        )
    answer = response["message"]["content"]
    st.session_state.msgs.append({
        "role": "assistant",
        "content": answer
    })
    with st.chat_message("assistant"):
        st.write(answer)