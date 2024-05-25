# chatbot.py
# Import necessary modules
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import streamlit as st
import sqlite3
from query import creare_connessione_database, verifica_codice_fiscale, recupera_dati_paziente, inserisci_nuovo_paziente
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import NoEscape

# Define a prompt template for the chatbot
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Based on the patient's condition described, respond with either 'verde', 'giallo', or 'rosso' to categorize the severity of their condition."),
        ("user", "Patient condition details: {question}")
    ]
)

# Define a prompt template for extracting patient details
detail_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Extract the following details from the text: Name, Surname, Date of Birth, Gender, Location, Vital Signs, Symptoms. Provide the details in a structured format."),
        ("user", "Patient condition details: {question}")
    ]
)

# Define database variables
conn = sqlite3.connect('database.db')
cursor = conn.cursor()


# Set up the Streamlit framework
st.title('Langchain Chatbot With LLAMA2 model')  # Set the title of the Streamlit app
input_text = st.text_input("Describe the patient's condition:")  # Create a text input field in the Streamlit app

# Initialize the Ollama model with temperature set to 0
llm = Ollama(model="llama3", temperature=0)

# Create chains that combine the prompt and the Ollama model
categorize_chain = prompt | llm
detail_chain = detail_prompt | llm



# Invoke the chain with the input text and display the output
if input_text:
    # Categorize the severity
    response = categorize_chain.invoke({"question": input_text})
    severity = response.split()[0]
    st.write(f"The patient's condition is categorized as: {severity}")
    

    
