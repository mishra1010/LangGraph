# LangGraph

## Day 1
Setting up new virtual environment, make sure anaconda is installed in machine.

Open Anaconda command prompt or VS terminal if Python is added to env variables

Run the following commands in a folder

C:\LangGraph\LangGraph>python -m venv venv

 C:\LangGraph\LangGraph>LG\Scripts\activate

 pip install langgraph

 C:\LangGraph\LangGraph>pip install langchain

 C:\LangGraph\LangGraph>pip install langchain_openai

 C:\LangGraph\LangGraph>pip install dotenv

 Test the install by checking import

 from langgraph.graph import StateGraph

 Sequential workflows

## Day 2

Parallel workflows

1. Batsman workflow

2. UPSC essay workflow

## Day 3 - Conditional workflows in LangGraph

We have seen

1. Sequential workflows

2. Parallel workflows

3. Conditional workflow - we will see today. 

    - we will see a non-llm workflow - Quadratic Equation
    
    - then we will see one with LLM  - Customer support
    find sentiment from user feedback then for negative response we will run diagnosis to check issue-type, tone of user, urgency shown by user in the form of json and then
    we will use this for our response to user and end workflow
    
    1. we will focus on getting the sentiment from the review. Either positive or negative. we needto get a structured output from LLM, so first define a schema

    2. check a prompt to get the sentiment

    3. Define state ReviewState

    4. Now lets create a graph (pass reviewstate here), add nodes , create functions and add edges

## Day 4 - Iterative or Looping workflows in LangGraph

Automated workflow -> Generate post -> Post in LinkedIn, Insta etc.

How to understand if the post generated is having any quality issues? Iterative workflow

Topic -> LLM generate -> LLM evaluate -> good then -> end and HITL -> API
                                      -> if not good -> optimize LLM -> approve or improve loop

Lets build the workflow in LangGraph with 3 llms - generator llm, evaluator llm, optimizer llm


file - post_generation

## Day 5 - Build a Chatbot using LangGraph

file - 9_basic_chatbot

State - messages - Annotated list and add_messages(acts as reducer)

Why we use add_messages reducer here - state generally replaces old state and adds new state which would remove the old message in this case as we get new messages added.

So, we will use add_messages

Annotated list will extend BaseMessages so that we will have user message, system message or Ai message or to message

last time we had used operator.add as the reducer

This workflow does not store prev messages in memory. When invoke function is called, previous message get erased.. So, we need to use persistence

In persistence , state is not erased at the End. This message is stored in memory or db. DB is used in the industry. So, we will import memorysaver module

### This workflow does not store prev messages in memory. When invoke function is called, previous message get erased.. So, we need to use persistence
### In persistence , state is not erased at the End. This message is stored in memory or db. For implementing this import MemorySaver from LG and then 
### use checkpointer while declaring graph and pass checkpointer(memory saver) in compiler. Then wwhile invoking use thread_id to identify each of the chat sessions, each chat is a thread
### Before invoking , create a config variable and pass a configurable dictionary with thread_id. This will help in storing the messages in memory or db. We need to pass this config variable in invoke function.

State -> RAM

Next chat triggers workflow and then LG fetches state from RAM

Then passes the full state with message

which helps in persistence


