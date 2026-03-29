import streamlit as st
import requests

st.set_page_config(page_title="RAG Chat Assistant")

st.title(" Research Paper Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Ask something...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.markdown(user_input)


    with st.spinner("Thinking..."):
        response = requests.post(
            "http://localhost:5001/query",
            json={"query": user_input}
        )

        if response.status_code == 200:
            answer = response.json().get("answer", "No answer found")
        else:
            answer = "Error from API"


    st.session_state.messages.append({"role": "assistant", "content": answer})
    
    with st.chat_message("assistant"):
        st.markdown(answer)