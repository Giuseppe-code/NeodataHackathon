import streamlit as st

st.markdown("# Triage Operator 🏥 📄") #titolo pagina
st.divider()

st.write("Hi Marco, you are the Triage Operator. \n I will help you write"
         "the triage. What info we have about the patient?")
chat_input = st.chat_input("Describe the patient's condition:")  # Create a text input field in the Streamlit app

if chat_input:
    st.write(f": {chat_input}")



with open("patient_report.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="ReportPatient",
                    data=PDFbyte,
                    file_name="dataset/triage.pdf",
                    mime='text/plain')
