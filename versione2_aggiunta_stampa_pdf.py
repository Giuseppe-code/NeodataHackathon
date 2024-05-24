# chatbot.py
# Import necessary modules
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
import streamlit as st
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

# Set up the Streamlit framework
st.title('Langchain Chatbot With LLAMA2 model')  # Set the title of the Streamlit app
input_text = st.text_input("Describe the patient's condition:")  # Create a text input field in the Streamlit app

# Initialize the Ollama model
llm = Ollama(model="llama3")

# Create chains that combine the prompt and the Ollama model
categorize_chain = prompt | llm
detail_chain = detail_prompt | llm

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

# Invoke the chain with the input text and display the output
if input_text:
    # Categorize the severity
    response = categorize_chain.invoke({"question": input_text})
    severity = response.split()[0]
    st.write(f"The patient's condition is categorized as: {severity}")
    
    # Extract patient details
    detail_response = detail_chain.invoke({"question": input_text})
    details = {
        "Name": "John",
        "Surname": "Doe",
        "Date of Birth": "01/01/1970",
        "Gender": "Male",
        "Location": "Unknown",
        "Vital Signs": "Stable",
        "Symptoms": "None",
    }
    
    # Generate LaTeX report
    generate_latex_report(details, severity)
    st.write("Patient report generated.")
