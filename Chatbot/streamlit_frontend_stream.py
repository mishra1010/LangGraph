import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage

# st.session_state -> dict -> does not delete message history when the app is rerun. so, we will use this with message_history 
# 
# message_history = []

CONFIG = {'configurable': {'thread_id': 'thread-1'}}
#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hello'}


if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input("Type your message here...")

# Define actions

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    # response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_message = response['messages'][-1].content
    # # first add the message to message_history
    # st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    # with st.chat_message('assistant'):
    #     st.text(ai_message)

    with st.chat_message('assistant'):
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config = CONFIG,
                stream_mode='messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    
    