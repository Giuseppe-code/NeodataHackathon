import json
# chatbot.py
# Import necessary modules
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import streamlit as st
import sqlite3
from query import creare_connessione_database, verifica_codice_fiscale, recupera_dati_paziente, inserisci_nuovo_paziente
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import NoEscape
from langchain.chains import LLMChain  # Import the LLMChain class

# Define a prompt template for the chatbot
prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "You are a helpful assistant. Based on the patient's condition described, respond only with  ,'white','qreen', 'yellow', or 'red' to categorize the severity of their condition, you have also to consider the past of the patient reading his history before categorizing "),
        ("user", "Patient condition details: {question}")
    ]
)

# Define a prompt template for extracting patient details
detail_prompt = ChatPromptTemplate.from_messages(
    [
        ("system",
         "Extract the following details from the text: Codice_fiscale, Name, Surname, Date of Birth, Gender, Location, Vital Signs, Symptoms. Provide the details in json. dont tell other things other than the json file"),
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


# Function to get patient details from the model response
def get_patient_details(question):
    # Create the LangChain chain

    chain = LLMChain(llm=llm, prompt=detail_prompt)

    # Get the response from the model
    response = chain.run({"question": question})

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

    return name, surname, date_of_birth, gender, location, vital_signs, symptoms, codice_fiscale


# Example usage
name, surname, date_of_birth, gender, location, vital_signs, symptoms, codice_fiscale = get_patient_details(input_text)

print(
    f"Name: {name}, Surname: {surname},Codice fiscale: {codice_fiscale}, Date of Birth: {date_of_birth}, Gender: {gender}, Location: {location}, Vital Signs: {vital_signs}, Symptoms: {symptoms}")