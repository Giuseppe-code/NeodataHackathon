
import streamlit as st

st.title("Introduction️")

st.write("# Welcome to Igea! 🏥")

st.markdown("""
The Igea chatbot is designed to streamline and enhance the workflow for all employees, from general practitioners to specialists, and even those without medical experience.

### Benefits of Our Healthcare Assistant Chatbot:

1. **Efficient Documentation**:  
     The chatbot simplifies the process of writing and digitizing documents, making it easier and faster for medical staff to maintain accurate and up-to-date records.

2. **Streamlined Work Organization**:  
     Seamlessly pass files between departments, ensuring smooth communication and coordination. This will help in organizing tasks more effectively and reducing delays.  

3. **Personnel Management**:  
     Quickly organize and manage personnel assignments, ensuring the right staff is in the right place at the right time.

4. **Help Patient Classification**:  
     Efficiently help the triage operator classify patients with the color-coded system (white, green, yellow, red) to prioritize care based on the severity of their condition.

5. **Patient History Tracking**:  
     The chatbot, in the future (not implemented) , could check if a patient has previously visited the hospital, potentially with similar symptoms, to provide better continuity of care and more accurate diagnoses.

Our chatbot is here to support your daily operations, enhance productivity, and ensure that patient care is delivered swiftly and effectively. Welcome to a new era of healthcare management!
""")

st.markdown("""    
### Try the chatbot  
In this demo you can fulfill 3 different roles:
1. **Trage Specialist**  
   Every specialist, regardless of experience, will be able to fill out the Trage document. They will have a device for the client, assigning them the most appropriate color code, just use only a sentence for describe the situation
2. **Specialized Doctor**  
    A specialized doctor will be assigned the patient and the related documentation. It will provide possible solutions/medications. 
    The doctor can either send the patient home or refer them to the general doctor obviously with the aid of the chatbot.
3. **General Practitioner**  
    A general practitioner will receive the documentation if necessary, can conduct further examinations, and if needed, send the patient home""")

st.write("""### You can select your role in the Sidebar, now!👈 """)

