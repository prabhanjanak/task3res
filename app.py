import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Directly set the API key here (not recommended for production)
api_key = "AIzaSyDVufVbnVxP2haei0E7rGv38bvUuNi4ox4"

# Configure the API key
genai.configure(api_key=api_key)

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

# Initialize the Streamlit app
st.set_page_config(page_title="Q&A with Your Documents", layout="centered")

# Add the logo at the top of the page
st.image("assets/logo.png", width=100)

# Add the title
st.header("Task 3 - Retrieval Augmented Generation (RAG) Application in Streamlit")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Process the uploaded PDF
if uploaded_file:
    # Display progress for processing the PDF
    st.write("### Processing your file...")
    progress = st.progress(0)
    
    reader = PdfReader(uploaded_file)
    text_content = ""
    num_pages = len(reader.pages)
    
    for i, page in enumerate(reader.pages):
        text_content += page.extract_text() + "\n"
        progress.progress((i + 1) / num_pages)
    
    st.success("PDF processed successfully!")
    
    # Store extracted content in session state for later use
    st.session_state['pdf_content'] = text_content

    # Enable user input for asking questions after processing is done
    query = st.text_input("Ask a question about the document:")
    ask_button = st.button("Ask")

    if ask_button and query:
        st.session_state['chat_history'].append(("You", query))
        prompt = f"Based on the following document content:\n{st.session_state['pdf_content']}\n\nAnswer the following question:\n{query}"
        
        try:
            response = get_gemini_response(prompt)
            st.write("### Response:")
            response_text = ""
            for chunk in response:
                response_text += chunk.text
                st.write(chunk.text)
            st.session_state['chat_history'].append(("Bot", response_text))
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display chat history
st.subheader("Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Powered by Streamlit & Google Gemini | © 2024</p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Developed by Prabhanjan Bhat - AI Engineer Intern at Resolute AI</p>", unsafe_allow_html=True)
