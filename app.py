import streamlit as st
import time
from src.helper import *

# Set up the Streamlit page configuration
def configure_page(): 
    """Configure the Streamlit page layout"""
    st.set_page_config(page_title="Information Retrieval System", page_icon=":robot:", layout="wide")
    if "chat_history" not in st.session_state: 
        st.session_state.chat_history = []          # Initialize chat history to an empty list
    if "conversation" not in st.session_state: 
        st.session_state.conversation = None        # Initialize conversation to None

# Render the header of the Streamlit app
def render_header(): 
    """Render the header of the Streamlit app"""
    st.header("🤖Information Retrieval System")
    st.markdown("Click the arrow on the top-left to expand the sidebar and upload PDF files.")


# Upload functionality in the sidebar
def handle_file_upload(): 
    """Handle file upload functionality in the sidebar"""
    # Setup session state
    st.session_state.setdefault("show_about", False)
    st.session_state.setdefault("upload_success", False)

    with st.sidebar: # Sidebar for file upload
        st.title("🔗 Attachments")

        # Get the files from user
        uploaded_files = st.file_uploader("Upload PDF files", accept_multiple_files=True)

        # Submit button
        if st.button("Submit"):
            if uploaded_files: # If files are uploaded, process them
                process_uploaded_files(uploaded_files)
                st.session_state.upload_success = False # Reset upload success state
            else: # If no files are uploaded, show a warning message
                st.warning("Please upload at least one PDF file")

        st.markdown("---")
        col1, col2, col3 = st.columns(3)        # Footer row:  GitHub | LinkedIn | About

        with col1:  # GitHub icon
            st.markdown(
                "[![GitHub](https://img.icons8.com/ios-glyphs/40/github.png)](https://github.com/cdacpranav/GenAI_IRS)",
                unsafe_allow_html=True)

        with col2:  # LinkedIn icon
            st.markdown(
                "[![LinkedIn](https://img.icons8.com/ios-glyphs/40/linkedin.png)](https://www.linkedin.com/in/pranavharke)",
                unsafe_allow_html=True)
                
        with col3:  # About toggle button
            if st.button("**ｉ**"):
                st.session_state.show_about = not st.session_state.show_about

        # Show About section content on click
        if st.session_state.show_about:
            st.info("""
                GenAI-IRS is a document question-answering system that lets you upload PDFs and ask questions in natural language. 
                Powered by advanced AI models (LangChain, GROQ, Streamlit), it uses semantic search and conversational memory to provide accurate, source-attributed answers from your documents.
                Upload your PDFs, submit, and start a meaningful conversation with your data!""")
            st.write("Crafted with Curiosity & Fueled by Tea")
            st.markdown("Made with 💡 by [Pranav Harke](https://www.linkedin.com/in/pranavharke)")

# Process the uploaded and valid PDF files
def process_uploaded_files(all_files): 
    """"Process the uploaded files and return a vector store if valid PDFs are found"""
    valid_pdfs = []
    for file in all_files: # Check each uploaded file
        if file.type == "application/pdf": # If the file is a PDF, process it
            container = st.empty()                      # Create a container to show upload status
            container.success(f"✅ Uploaded: {file.name}")   # Show the name of the uploaded file
            valid_pdfs.append(file)                     # Add the valid PDF file to the list    
            time.sleep(0.8)                             
            container.empty()   
        else: # If the file is not a PDF, show an error message
            container = st.empty()
            container.error(f"❌ Rejected: {file.name} ")   # Show an error message for non-PDF files
            time.sleep(1.2)
            container.empty()

    if valid_pdfs: # If there are valid PDF files, process them
        with st.spinner("Processing document(s)..."):           # Show a spinner while processing
            return process_valid_pdfs(valid_pdfs)               # Process the valid PDF files
    return None

# Process the valid PDF files and extract text chunks
def process_valid_pdfs(valid_pdfs): 
    all_chunks = []                             # List to store all text chunks from the PDFs
    all_metadatas = []                          # List to store metadata for each text chunk
    for file in valid_pdfs:                     # Iterate through each valid PDF file
        pdf_text = get_pdf_text(file)           # Extract text from the PDF file
        chunks = get_text_chunks(pdf_text)      # Split the text into chunks
        all_chunks.extend(chunks)               # Add the chunks to the list of all chunks
        all_metadatas.extend([{"source": file.name}] * len(chunks)) # Add metadata for each chunk

    if not all_chunks:  # If no text chunks were extracted, show an error message
        st.error("No readable content found in the uploaded PDF(s)")
        return

    # Create a vector store from the text chunks
    vector_store = get_vector_store(all_chunks, all_metadatas) 
    
    # Update conversation with PDF-based conversational chain
    st.session_state.conversation = get_conversational_chain(vector_store)
    
    st.success("All PDF(s) processed successfully!")
    return vector_store  # Return vector store so main can use it

# Display the chat history in the conversation area
def display_chat_history(): 
    for msg in st.session_state.chat_history:
        with st.chat_message("user", avatar="👤"):
            st.markdown(msg["user"])
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["bot"])

# Handle user input in the chat interface
def handle_chat_input(): 
    user_input = st.chat_input("Ask anything")
    if user_input:
        if not st.session_state.conversation: # If no conversation chain is not available, show a warning
            st.warning("❌ Please upload document(s) to get started.")
            return
            
        # Invoke the conversation chain with the user input
        result = st.session_state.conversation.invoke(user_input)
        response = result.get('answer', str(result))

        # Session state to store the chat history
        st.session_state.chat_history.append({
            "user": user_input,     # Store user input in chat history
            "bot": response         # Store bot response in chat history
        })

        from streamlit.runtime.scriptrunner.script_runner import RerunException, RerunData    # Trigger a rerun to update the chat interface
        raise RerunException(RerunData())                            # This will cause the app to rerun and display the updated chat history

def main(): # Main function to run the Streamlit app
    configure_page()            # Configure the Streamlit page
    render_header()             # Render the header
    handle_file_upload()        # Capture uploaded files processing result
    display_chat_history()      # Display the chat history
    handle_chat_input()         # Handle user input in the chat interface

if __name__ == "__main__": # Entry point for the Streamlit app
    main()