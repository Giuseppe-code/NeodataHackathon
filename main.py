#

import requests
import os
import json
# chatbot.py
# Import necessary modules
from langchain_core.prompts import ChatPromptTemplate
#da togliere questa riga
from langchain_community.llms import Ollama
import streamlit as st
import sqlite3
from query import *
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import NoEscape
from langchain.chains import LLMChain  # Import the LLMChain class

# CHIAVI API
os.environ['OPENAI_API_KEY'] = 'sk-proj-eGrGL5sBrvtXjyMm7oApT3BlbkFJsN0aau3Ivx3puXkLqSXp'
os.environ['tavily_api_key'] = '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'
os.environ['TAVILY_API_KEY'] = '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'
#  Importazioni necessarie per la RAG
from langchain_community.retrievers import WikipediaRetriever
#retriever = WikipediaRetriever()
#docs = retriever.invoke("codice fiscale")
#print(docs)
# Aggiunta delle conoscenze di triage:
from langchain.tools.retriever import create_retriever_tool
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.tools.tavily_search import TavilySearchResults


loader = WebBaseLoader(
    [
        "https://web.dmi.unict.it/corsi/l-31/insegnamenti?seuid=CD1ABF9F-5308-450E-813E-60B84F9EDAA5",
        "https://web.dmi.unict.it/corsi/l-31/insegnamenti?seuid=6E03B0E2-5E93-43C5-BBFB-E4D6446DB180",
        "https://web.dmi.unict.it/corsi/l-31/insegnamenti?seuid=81E1DC57-5DC2-46ED-84AF-3C8BB46F3F49",
        "https://web.dmi.unict.it/corsi/l-31/contatti",
    ]
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
#documents = RecursiveCharacterTextSplitter(
#    chunk_size=1000, chunk_overlap=400
#).split_documents(docs)
# creazione degli embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

persist_directory = "./chroma/"
embedding = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(splits,embedding,persist_directory=persist_directory)


#vectorstore = Chroma.from_documents(documents=splits,
                                    #embedding=OpenAIEmbeddings,
                                    #persist_directory=persist_directory)



#vector = Chroma.from_documents(documents, OpenAIEmbeddings())
retriever = vectorstore.as_retriever(search_type="mmr", search_kwargs={"k": 6})
# Create tools
retriever_tool = create_retriever_tool(
    retriever,
    "Uni_helper",
    "Help students and Search for information about University of Catania courses. For any questions about uni courses and their careers, you must use this tool for helping students!",
)
# Search tool

tavily_api_key = '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'
search = TavilySearchResults(max_results=3,tavily_api_key=tavily_api_key)
tools = [search, retriever_tool]









# Define a prompt template for the chatbot
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a helpful assistant. Based on the patient's condition described, respond only with  ,'white','qreen', 'yellow', or 'red' to categorize the severity of their condition, you have also to consider the past of the patient reading his history before categorizing "),
        ("user", "Patient condition details: {question}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)




# Define a prompt template for extracting patient details
detail_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "using the json format from ommitting the json in the response, Extract the following details from the text: Codice_fiscale, Name, Surname, Date of Birth, Gender, Location, Vital Signs, Symptoms. Provide the details in json. dont tell other things other than the json file"),
        ("user", "Patient condition details: {question}")
    ]
)
#pronpth del codice fiscale
codicefiscale_prompth = ChatPromptTemplate.from_messages(
    [
        ("system",
         "in base alla descrizione del paziente rispondi solo con una parola estrapolando il codice fiscale dalla descrizione fornita"),
        ("user", "Patient codice fiscale: {question}")
    ]
)



# Define database variables
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Set up the Streamlit framework
st.title('Langchain Chatbot With LLAMA2 model')  # Set the title of the Streamlit app
input_text = st.text_input("Describe the patient's condition:")  # Create a text input field in the Streamlit app

# Initialize the Ollama model with temperature set to 0
#llm = Ollama(model="llama3", temperature=0)
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o",temperature=0)
llm.bind_tools(tools)
#aggiunta di un output parser
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()



# Create chains that combine the prompt and the Ollama model
categorize_chain = prompt | llm | output_parser
detail_chain = detail_prompt | llm | output_parser
codicefiscale_chain = codicefiscale_prompth | llm | output_parser



# creazione dell'agent
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


  







# Invoke the chain with the input text and display the output
if input_text:
    # Categorize the severity
    response = categorize_chain.invoke({"question": input_text})
    #response = llm.invoke(input_text)
    #severity = response.split()[1]
    st.write(f"il sistema IGEA classifica il paziente con il codice: {response}")


# Function to get patient details from the model response
def get_patient_details(question):
    # Create the LangChain chain

    #chain = LLMChain(llm=llm, prompt=detail_prompt)
    detail_chain = detail_prompt | llm | output_parser

    # Get the response from the model
    #response = chain.run({"question": question})
    response = detail_chain.invoke({"question": input_text})
    
# Rimozione degli ultimi 3 caratteri
    #response = response[:5]

    print()
    print(response)
   # response.lstrip(5)
    print(type(response))
    print()

    # Convert the response to a dictionary
    response_dict = json.loads(response)

    # Extract the parameters
    name = response_dict.get("Name", "non specificato")
    codice_fiscale = response_dict.get("Codice fiscale","Non specificato")
    surname = response_dict.get("Surname", "non specificato")
    date_of_birth = response_dict.get("Date of Birth", "non specificato")
    gender = response_dict.get("Gender", "non specificato")
    location = response_dict.get("Location", "non specificato")
    vital_signs = response_dict.get("Vital Signs", "non specificato")
    symptoms = response_dict.get("Symptoms", "non specificato")




    return name, surname, date_of_birth, gender, location, vital_signs, symptoms


# Example usage
name, surname, date_of_birth, gender, location, vital_signs, symptoms = get_patient_details(input_text)
# preleva il codeice fiscale

def get_patient_CodiceFiscale(question):
    prompt = codicefiscale_prompth
    codicefiscale_chain = codicefiscale_prompth | llm | output_parser


    response = codicefiscale_chain.invoke({"question": input_text})
    codice_fiscale = response
    return codice_fiscale
codice_fiscale = get_patient_CodiceFiscale(input_text)
st.write(codice_fiscale)

print(
    f"Name: {name}, Surname: {surname},Codice fiscale: {codice_fiscale}, Date of Birth: {date_of_birth}, Gender: {gender}, Location: {location}, Vital Signs: {vital_signs}, Symptoms: {symptoms}")




# Function to generate LaTeX report
def generate_latex_report(details, severity):
    doc = Document()
    with doc.create(Section('Patient Report')):
        doc.append(f"Name: {details.get('Name', 'N/A')}\n")
        doc.append(f"Surname: {details.get('Surname', 'N/A')}\n")
        doc.append(f"Date of Birth: {details.get('Date of Birth', 'N/A')}\n")
        doc.append(f"Gender: {details.get('Gender', 'N/A')}\n")
        doc.append(f"Location: {details.get('Location', 'N/A')}\n")
        doc.append(f"Vital Signs: {details.get('Vital Signs', 'N/A')}\n")
        doc.append(f"Symptoms: {details.get('Symptoms', 'N/A')}\n")
        doc.append(f"Severity: {severity}\n")
    
    # Save the document
    doc.generate_pdf('patient_report', clean_tex=False)

