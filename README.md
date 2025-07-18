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

    5. 