from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from langchain_community.utilities import SerpAPIWrapper

load_dotenv()

def main():
    search_type = input("You like you use the web search or the openAI agent? (web/agent/local): ")
    if search_type == "web":
        web_agent()
    elif search_type == "agent":
        openAI_agent()
    elif search_type == "local":
        ollama_agent()
    else:
        print("Invalid search type")


def openAI_agent():
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    person_name = input("Enter the person's name: ")
    summary_template = f"""
    You are helpful agent who helps to find the person and provide atleast two interesting facts about the person.
    Person name is {person_name}
    """

    summary_prompt = PromptTemplate(
        input_variables=["person_name"],
        template=summary_template
    )

    submit = summary_prompt | model
    person_information = submit.invoke({"person_name": person_name})
    print(person_information.content)

def ollama_agent():
    model = ChatOllama(model="gemma2:2b", temperature=0)
    person_name = input("Enter the person's name: ")
    summary_template = f"""
    You are helpful agent who helps to find the person and provide atleast two interesting facts about the person.
    Person name is {person_name}
    """
    summary_prompt = PromptTemplate(
        input_variables=["person_name"],
        template=summary_template
    )
    submit = summary_prompt | model
    person_information = submit.invoke({"person_name": person_name})
    print(person_information.content)

def web_agent():
    search = SerpAPIWrapper()
    person_name = input("Enter the person's name: ")
    results = search.run(f"{person_name} biography profile career background")
    print(results)


if __name__ == "__main__":
    main()
