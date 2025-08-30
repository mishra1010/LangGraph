from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
import os
import sqlite3

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool
import requests

load_dotenv()

llm = AzureChatOpenAI(
    deployment_name="gpt-4o-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_version="2024-12-01-preview",  # Replace with the appropriate version
)

# Tools
search_tool = DuckDuckGoSearchRun(region="us-en")

@tool
def calculator(first_num: float, second_num: float, operation: str) -> dict:
    """Performs a calculation on two numbers."""
    try:
        if operation == "add":
            result = first_num + second_num
        elif operation == "subtract":
            result = first_num - second_num
        elif operation == "multiply":
            result = first_num * second_num
        elif operation == "divide":
            if second_num == 0:
                return {"error": "Cannot divide by zero."}
            result = first_num / second_num
        else:
            return {"error": f"Unsupported operation: {operation}"}
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@tool
def get_stock_price(symbol: str) -> dict:
    """Fetches the current stock price for a given symbol."""
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Make tool list
tools = [search_tool, calculator, get_stock_price]

# Make the LLM tool aware
llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# graph nodes
def chat_node(state: ChatState):
    """LLM node that may answer or request a tool call."""
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}
tool_node = ToolNode(tools)


# def chat_node(state:ChatState):

#     #take user query from state
#     messages = state['messages']

#     #send messages to LLM
#     response = llm.invoke(messages)

#     #response store state
#     return {'messages': [response]}


connect = sqlite3.connect(database='chatbot.db', check_same_thread=False)

# use Memory Saver
checkpointer = SqliteSaver(conn=connect)

# Define the state graph

# graph structure #add nodes
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)


# edges
graph.add_edge(START, "chat_node")

# If the LLM response includes a tool call, go to the tool node, else Finish
#graph.add_conditional_edges("chat_node", tools_condition)
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")


# #add edges
# graph.add_edge(START, 'chat_node')
# graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

#test

# response = chatbot.invoke(
#     {'messages': [HumanMessage(content='what is my name?')]},
#     config={'configurable': {'thread_id': 'thread-1'}},
# )

# print(response)

# Helper - Identify how many threads are there in the db already
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        #print(checkpoint.config['configurable']['thread_id'])
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)