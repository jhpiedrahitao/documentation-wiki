import streamlit as st
import requests

API_URL = "http://localhost:5589/sagemaker"  
DOWNLOAD_URL = "http://localhost:5589/download/"

# Streamlit UI elements
st.title("AWS Sagemaker Documentation Wiki (PoC)")

question = st.text_input("Enter your question:")
submit_button = st.button("Submit")

def get_answer_and_sources(question):
    # Function to send a POST request to the API
    data = {"question": question}
    response = requests.post(API_URL, data=data)
    return response.json()

if submit_button:
    with st.spinner("Getting Answer..."):
        if question:
            result = get_answer_and_sources(question)
            answer = result.get("answer")
            sources = result.get("sources")

            st.subheader("Answer:")
            st.markdown(answer.replace("\n", "  \n"))

            if sources:
                st.subheader("Source Documents:")
                st.write("These documents could be relevant for you:")
                for source in sources:
                    source=source.replace("Documents/sagemaker_documentation/", "")
                    st.markdown(f"[{source}]({DOWNLOAD_URL}{source})")
                    #st.markdown(f"[{source.replace('Documents/sagemaker_documentation/','')}]({source})")

        else:
            st.warning("Please enter a question.")