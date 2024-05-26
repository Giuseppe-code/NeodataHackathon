import streamlit as st
st.set_page_config(page_title="Ijea Assistant", page_icon="")


messages = []
textIntroduction = "Hi Giovanni, you are the General Doctor. The info about the patient are at the top"

with open("patient_report.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()

st.markdown("# General Doctor 🩺️")
st.divider()

st.download_button(label="ReportPatient",
                   data=PDFbyte,
                   file_name="dataset/triage.pdf",
                   mime='text/plain')

varText = st.chat_input("assign the patient at the doctor ...")
# Initialize chat history
with st.container(height=280):
    if messages == []:
        messages = []
        messages.append(
            {"role": "assistant", "content": textIntroduction})

    # Display chat messages from history on app rerun
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # React to user input
    if prompt := varText:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        messages.append({"role": "user", "content": prompt})

        response = f"Echo: {prompt}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        messages.append({"role": "assistant", "content": response})
