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
os.environ['OPENAI_API_KEY'] = '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'
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

st.set_page_config(
    page_title="Igea",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

loader = WebBaseLoader(
    [
        "https://www.nurse24.it/specializzazioni/emergenza-urgenza/che-cos-e-il-triage-infermieristico.html",
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
    "triage_classifier",
    "for classifiing the patient you must follow this informations and instructions criterias!",
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
# triage report
triagereport_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "you are a great triage operator, summarize in markdown the medichal condition of the patient in the following schema Personal informations , brief summary of the motivation that caused him to go the hospital, synthoms and a brief possible threatment. dont add more than askd "),
        ("user", "Patient condition details: {question}")
    ]
)

# specialized report
specializedreport_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         " you are an automatic notifier, based on the additional info provided by the specialist, list in markdown all of the hospital wards to notify and the exam to take "),
        ("user", "Specialist response: {question}")
    ]
)
        
# response del medico generale
generalreport_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "Based on the imput provided if the doctor declares the dimission write in markdown:the patient is dimitted"),
        ("user", "General doctor response: {question}")
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
st.title("Per caricare il bot passa prima da triage, specialized, general, dopo prova l' app da triage👈")  # Set the title of the Streamlit app
input_text = st.text_input(" ")
# Initialize the Ollama model with temperature set to 0
#llm = Ollama(model="llama3", temperature=0)
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o",temperature=0)
llm.bind_tools(tools)
#aggiunta di un output parser
from langchain_core.output_parsers import StrOutputParser
output_parser = StrOutputParser()



# Create chains that combine the prompt and the gpt4oa model
categorize_chain = prompt | llm | output_parser
detail_chain = detail_prompt | llm | output_parser
codicefiscale_chain = codicefiscale_prompth | llm | output_parser
triagereport_chain = triagereport_prompt | llm | output_parser


# creazione dell'agent
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


  







# Invoke the chain with the input text and display the output
def GetReportPatient(input_text):
    if input_text:
    # Categorize the severity
        response = categorize_chain.invoke({"question": input_text})
    #response = llm.invoke(input_text)
    #severity = response.split()[1]
        #st.write(f"il sistema IGEA classifica il paziente con il codice: {response}")
        return response


# Function to get patient details from the model response
def get_patient_details(question):
    if input_text:
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
#name, surname, date_of_birth, gender, location, vital_signs, symptoms = get_patient_details(input_text)
# preleva il codeice fiscale

def get_patient_CodiceFiscale(question):
    if input_text:
        prompt = codicefiscale_prompth
        codicefiscale_chain = codicefiscale_prompth | llm | output_parser


        response = codicefiscale_chain.invoke({"question": input_text})
        codice_fiscale = response
        return codice_fiscale
codice_fiscale = get_patient_CodiceFiscale(input_text)
#st.write(codice_fiscale)

#print(
#    f"Name: {name}, Surname: {surname},Codice fiscale: {codice_fiscale}, Date of Birth: {date_of_birth}, Gender: {gender}, Location: {location}, Vital Signs: {vital_signs}, Symptoms: {symptoms}")




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


def insert_patient_and_card(codice_fiscale, name, surname, birthday, residence, gender, city_of_birth, symptoms,severity, day_of_registration):
    # Controllo se il paziente esiste
    cursor.execute('SELECT * FROM Patient WHERE codice_fiscale = ?', (codice_fiscale,))
    patient = cursor.fetchone()

    if patient is None:
        # Inserisco il paziente
        cursor.execute('''
        INSERT INTO Patient (codice_fiscale, name, surname, birthday,residence, gender,city_of_birth)
        VALUES (?, ?, ?, ?,?, ?, ?)
        ''', (codice_fiscale, name, surname, birthday,residence, gender, city_of_birth))
        conn.commit()
        print(f'Inserted Patient with codice_fiscale: {codice_fiscale}')
    else:
        #non lo inserisco
        print(f'Patient with codice_fiscale: {codice_fiscale} already exists.')

    # Inserisco la Patient_card (insert che va fatto sempre)
    cursor.execute('''
    INSERT INTO Patient_card (codice_fiscale, day_of_registration, symptoms, severity )
    VALUES (?, ?, ?, ?)
    ''', (codice_fiscale, day_of_registration, symptoms,severity))
    conn.commit()
    print(f'Inserted Patient_card for codice_fiscale: {codice_fiscale}')





def getTriageReport(input_text):
    if input_text:
        prompt = triagereport_prompt
        triagereport_chain = prompt | llm | output_parser


        response = triagereport_chain.invoke({"question": input_text})
        #name, surname, date_of_birth, gender, location, vital_signs, symptoms = get_patient_details(input_text)

        #insert_patient_and_card(codice_fiscale,severity)

        return response



def getSpecializedReport(input_text):
    if input_text:
        specializedreport_chain = specializedreport_prompt | llm | output_parser


        response = specializedreport_chain.invoke({"question": input_text})
        return response



def getGeneralReport(input_text):
    if input_text:
        generalreport_chain = generalreport_prompt | llm | output_parser


        response = generalreport_chain.invoke({"question": input_text})
        return response
