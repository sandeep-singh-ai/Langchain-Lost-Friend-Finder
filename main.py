from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.messages import HumanMessage
from tavily import TavilyClient

load_dotenv()

class AgentResponse(BaseModel):
    name: str = Field(description="the name of the person")
    age: int = Field(description="the age of the person")
    occupation: str = Field(description="the occupation of the person")
    location: str = Field(description="the location of the person")
    linkedin_url: str = Field(description="the linkedin url of the person")
    current_company: str = Field(description="the current company of the person")
    current_position: str = Field(description="the current position of the person")
    current_location: str = Field(description="the current location of the person")
    cell_phone_number: str = Field(description="the cell phone number of the person")
    sources: List[str] = Field(default_factory=list, description="the source of the information")

taily_search = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
    )

@tool
def search_web(query: str) -> str:
    """this toll is used to search person information from the web
    Input: query - the query to search for
    Output: the search results
    """
    return str(taily_search.search(query))

tools = [search_web]
openAI_web_agent = create_agent(model=ChatOpenAI(model="gpt-4o-mini", temperature=0), tools=tools, response_format=AgentResponse)
ollama_web_agent = create_agent(model=ChatOllama(model="qwen2.5:0.5b", temperature=0), tools=tools, response_format=AgentResponse)

def main():
    search_type = input("You like you use the web search or the openAI agent? (serp/agent/local): ")
    if search_type == "serp":
        web_agent()
    elif search_type == "agent":
        openAI_agent()
    elif search_type == "local":
        ollama_agent()
    else:
        print("Invalid search type")


def openAI_agent():
    person_name = input("Enter full information about the person you know about: ")
    summary_template = f"""
    You are helpful agent who helps to find the person and provide atleast two interesting facts about the person.
    Person name is {person_name}
    """

    Information = openAI_web_agent.invoke({"messages": [HumanMessage(content=summary_template)]})
    print(Information)

def ollama_agent():
    person_name = input("Enter the person's full details you know about: ")
    summary_template = f"""
    You are helpful agent who helps to find the person and provide atleast two interesting facts about the person.
    Person name is {person_name}
    """
    
    information = ollama_web_agent.invoke({"messages": [HumanMessage(content=summary_template)]})
    print(information)

def web_agent():
    search = SerpAPIWrapper()
    person_name = input("Enter full information about the person you know about: ")
    results = search.run(f"{person_name} biography profile career background")
    print(results)


if __name__ == "__main__":
    main()
