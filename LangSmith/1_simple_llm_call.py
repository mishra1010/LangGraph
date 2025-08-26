from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

load_dotenv()

# Simple one-line prompt
prompt = PromptTemplate.from_template("{question}")

#model = ChatOpenAI()
llm = AzureChatOpenAI(
    deployment_name="gpt-4o-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_version="2024-12-01-preview",  # Replace with the appropriate version
)
parser = StrOutputParser()

# Chain: prompt → model → parser
chain = prompt | llm | parser

# Run it
result = chain.invoke({"question": "What is the capital of Peru?"})
print(result)
