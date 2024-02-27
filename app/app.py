import streamlit as st
from pdf_utils import PdfProcessor
import tempfile # to store pdfs in temp folder so I can have a file path for now to feed to PdfProcessor
import os

def main():
    st.set_page_config(page_title="Noteify")

    #st.title("Chat with PDF file.")
    st.header("Upload your PDF and start chatting with it.")
    st.text_input("Ask a question: ")

    menu = ["Notes", "Chat Bot", "Flashcards", "Quiz", "Transcript", "Settings"]
    choice = st.sidebar.selectbox("Menu", menu)

    with st.sidebar:
        st.header("Document Upload")
        pdf_file = st.file_uploader("Choose your PDFs and click 'Process'", type=["pdf"], accept_multiple_files=True)

        if st.button("Process"):
            if pdf_file:
                with st.spinner("Processing..."):
                    # create temp folder to store pdfs
                    temp_folder = tempfile.TemporaryDirectory()
                    file_path = os.path.join(temp_folder.name, pdf_file.name)
                    with open(file_path, "wb") as f:
                        f.write(pdf_file.getvalue())

                    pdf = PdfProcessor(file_path)
                    st.success("Processing complete.")


if __name__ == "__main__":
    main()


