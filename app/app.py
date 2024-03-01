import streamlit as st
from pdf_utils import PdfProcessor, get_text_chunks
import tempfile # to store pdfs in temp folder so I can have a file path for now to feed to PdfProcessor
import os
import time

def progress_bar():
    progress_text = "Your PDF is being processed. Please wait..."
    my_bar = st.progress(0, progress_text)
    for percent_complete in range(100):
        time.sleep(0.001)
        my_bar.progress(percent_complete + 1, progress_text)
    time.sleep(1)
    my_bar.empty()
        
def main():
    st.set_page_config(page_title="Noteify")

    #st.title("Chat with PDF file.")
    st.header("Upload your PDF and start chatting with it.")
    st.text_input("Ask a question: ")

    menu = ["Notes", "Chat Bot", "Flashcards", "Quiz", "Transcript", "Settings"]
    choice = st.sidebar.selectbox("Menu", menu)

    with st.sidebar:
        st.header("Document Upload")
        uploaded_pdf_file = st.file_uploader("Choose your PDFs and click 'Process'", type=["pdf"], accept_multiple_files=False) # false for now, if true will need to loop upload_pdf_file

        if st.button("Process", key="process_pdf"):
            if uploaded_pdf_file:
                with st.spinner("Processing..."):
                    # i want to store the pdf in a temp folder so i can get the file path and feed it to PdfProcessor
                    temp_dir = tempfile.TemporaryDirectory()
                    temp_file_path = os.path.join(temp_dir.name, uploaded_pdf_file.name)

                    with open(temp_file_path, "wb") as f:
                        f.write(uploaded_pdf_file.getbuffer())

                    
                    raw_text = PdfProcessor(temp_file_path).getAll()
                    

                    text_chunks = get_text_chunks(raw_text)
                    st.write(text_chunks)
                    '''for i in range(len(text_chunks)):
                        st.write(f"Chunk {i + 1}: {text_chunks[i]}")'''
                    
                    st.success("Processing complete.")
    
    if st.button("Start progress bar", key="start_progress_bar"):
        progress_bar()

    


if __name__ == "__main__":
    main()


