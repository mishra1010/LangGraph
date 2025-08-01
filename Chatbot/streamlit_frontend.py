import streamlit as st

with st.chat_message('user'):
    st.text('Hello, how are you?')

with st.chat_message('assistant'):
    st.text('I am good, how can i help you?')

with st.chat_message('user'):
    st.text('My name is Deepak')

user_input = st.chat_input("Type your message here...")

# Define actions

if user_input:
    with st.chat_message('user'):
        st.text(user_input)
    
    