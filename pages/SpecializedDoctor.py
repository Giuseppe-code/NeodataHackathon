import streamlit as st

st.markdown("# Specialized Doctor ⚕️") #titolo pagina
st.divider()
st.write("Hi Marco, you are the Specialized Doctor. \n I will send"
         " you the information. We have this info about the patient:")

chat_input = st.chat_input("assign the patient at the doctor ...")  # Create a text input field in the Streamlit app


if chat_input:
    st.write(f": {chat_input}")

with open("patient_report.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.download_button(label="ReportPatient",
                    data=PDFbyte,
                    file_name="dataset/triage.pdf",
                    mime='text/plain')
