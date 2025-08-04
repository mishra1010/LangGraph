from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
import os

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

# Define the state graph

# use Memory Saver
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)

#add nodes
graph.add_node('chat_node', chat_node)


#add edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)


# Streaming in chatbot using langgraph

# for message_chunk, metadata in chatbot.stream(
#     {'messages': [HumanMessage(content='What is the recipe to make pasta?')]},
#     config= {'configurable': {'thread_id': 'thread-1'}},
#     stream_mode='messages'
# ):

#     if message_chunk.content:
#         print(message_chunk.content, end=" ", flush=True)

#print(type(stream))