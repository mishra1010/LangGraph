from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import os
import sqlite3

load_dotenv()

llm = AzureChatOpenAI(
    deployment_name="gpt-4o-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_version="2024-12-01-preview",  # Replace with the appropriate version
)

class ChatState(TypedDict):

    messages: Annotated[list[BaseMessage], add_messages]

def chat_node(state:ChatState):

    #take user query from state
    messages = state['messages']

    #send messages to LLM
    response = llm.invoke(messages)

    #response store state
    return {'messages': [response]}


connect = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# use Memory Saver
checkpointer = SqliteSaver(conn=connect)

# Define the state graph

graph = StateGraph(ChatState)

#add nodes
graph.add_node('chat_node', chat_node)


#add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

#test

# response = chatbot.invoke(
#     {'messages': [HumanMessage(content='what is my name?')]},
#     config={'configurable': {'thread_id': 'thread-1'}},
# )

# print(response)

# Identify how many threads are there in the db already
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        #print(checkpoint.config['configurable']['thread_id'])
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)