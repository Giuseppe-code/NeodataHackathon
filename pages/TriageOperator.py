from chatbot import *
import streamlit as st

st.markdown("# Triage Operator  📄") #titolo pagina
st.divider()

textIntroduction = "Hi Angela, you are the Triage Operator. I will help you write the triage. What info we have about the patient?"
varText = st.chat_input("Write here..")


with st.container(height=340):
    if "messages_3" not in st.session_state:
        st.session_state.messages_3 = []
        st.session_state.messages_3.append(
            {"role": "🤖", "content": textIntroduction})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages_3:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


    # React to user input
    if prompt := varText:
        # Display user message in chat message container
        st.chat_message("🥼").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages_3.append({"role": "🥼", "content": prompt})

        response = getTriageReport(prompt)
        severity = GetReportPatient(prompt)
        st.write(severity)
        print(response)
        # Display assistant response in chat message container
        with st.chat_message("🤖"):
            st.markdown(response)
            st.session_state.messages_1.append(
                {"role": "🤖", "content": response})

        # Add assistant response to chat history
        st.session_state.messages_3.append({"role": "🤖", "content": response})

