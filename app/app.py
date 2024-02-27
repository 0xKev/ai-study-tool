import streamlit as st
from pdf_utils import PdfProcessor
import tempfile # to store pdfs in temp folder so I can have a file path for now to feed to PdfProcessor
import os

def main():
    st.set_page_config(page_title="Noteify")

    st.title("Chat with file")

    with st.sidebar:
        st.header("File Upload")
        pdf_file = st.file_uploader("Choose your PDFs and click 'Process'", type=["pdf"], accept_multiple_files=False)

        if pdf_file:
            temp_dir = "D:\Documents\Coding\My projects\ai study tool\temp"
            path = os.path.join(temp_dir, pdf_file.name)
            with open(path, "wb") as f:
                f.write(pdf_file.getvalue())


        
        if st.button("Process"):
            if pdf_file is not None:
                
                with st.spinner("Processing..."):
                    raw_text = PdfProcessor(pdf_file)
                    raw_text = raw_text.getPages(4, 5)
                    print(raw_text)
                    st.write(raw_text)
                    '''raw_text = PdfProcessor(pdf_file)
                    raw_text = raw_text.getAll()
                    st.write(raw_text)'''
                  
                

if __name__ == "__main__":
    main()


