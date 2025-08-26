from langchain_openai import AzureChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os

os.environ['LANGCHAIN_PROJECT'] = 'SeqLLMApp'
load_dotenv()

prompt1 = PromptTemplate(
    template='Generate a detailed report on {topic}',
    input_variables=['topic']
)

prompt2 = PromptTemplate(
    template='Generate a 5 pointer summary from the following text \n {text}',
    input_variables=['text']
)

model = AzureChatOpenAI(
    deployment_name="gpt-4o-mini",
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("azure_endpoint"),
    api_version="2024-12-01-preview",  # Replace with the appropriate version
)

parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

config = {
    'tags': ['llm_app', 'report_generation' 'summarization'],
    'metadata':{'model': 'gpt-4o-mini', 'parser': 'stroutputparser'}
}

result = chain.invoke({'topic': 'Unemployment in India'}, config=config)

print(result)
