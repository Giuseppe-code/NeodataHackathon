from chatbot import * 
import streamlit as st

st.markdown("# Specialized Doctor ⚕️")
st.divider()

textIntroduction = f"Hi Marco, you are the Specialized Doctor. \n I will send you the information. We have this info about the patient: "
varText = st.chat_input("write here...")


with st.container(height=340):
    if "messages_1" not in st.session_state:
        st.session_state.messages_1 = []
        st.session_state.messages_1.append(
            {"role": "🤖", "content": textIntroduction})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages_1:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



    # React to user input
    if prompt := varText:
        # Display user message in chat message container
        st.chat_message("🥼").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages_1.append({"role": "🥼", "content": prompt})

        response = getSpecializedReport(prompt)
        # Display assistant response in chat message container
        with st.chat_message("🤖"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages_2.append({"role" : " ", "content" : response})
        st.session_state.messages_1.append({"role": "🤖", "content": response})

