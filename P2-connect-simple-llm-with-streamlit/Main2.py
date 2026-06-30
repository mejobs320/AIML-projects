
# project connect to google ai atudio llm  ((gemini-2.5-flash) and summaries answers 
# It also create web ui using streamlit and answer queries

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

# Load the API key from the .env file
load_dotenv()

# 1. Page Configuration
st.set_page_config(
    page_title="Gemini Q&A Web App",
    page_icon="🤖",
    layout="centered"
)

# 2. Initialize the LLM (Cached so it doesn't reload on every button click)
@st.cache_resource
def init_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )

try:
    llm = init_llm()
except Exception as e:
    st.error(f"Failed to connect to Gemini: {e}")

# 3. Web UI Layout
st.title("🤖 Q&A Web Assistant")
st.write("Type your question below to get an instant answer from Google AI Studio.")
st.divider()

# User Input Field
user_query = st.text_input("Your Question:", placeholder="e.g., Explain quantum computing in one sentence...")

# Submit Button
if st.button("Ask Gemini", type="primary"):
    if user_query.strip() == "":
        st.warning("Please enter a question before submitting.")
    else:
        # Visual spinner while waiting for the API response
        with st.spinner("Gemini is thinking..."):
            try:
                # Format messages
                messages = [
                    SystemMessage(content="You are a clear, direct, and concise AI assistant."),
                    HumanMessage(content=user_query)
                ]
                
                # Fetch response
                response = llm.invoke(messages)
                
                # Display result in a nice UI box
                st.subheader("Response:")
                st.info(response.content)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                st.caption("Tip: Please verify that your GOOGLE_API_KEY inside the .env file is valid.")