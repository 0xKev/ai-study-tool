from data_processing import pdf_utils, text_embedder
from models.qdrant_store import TextVectorDatabase
from data_processing.exist_check import is_file_uploaded, save_hash
from models.fetch_answer import LlmChat

import pickle 

if __name__ == "__main__":
    # sample info 
    user_id = "kevin777"
    file_hash = "d41d8cd98f00b204e9800998ecf8427e"
    query: list[str] = ["What does the crow symbolize?"]

    txt_vector_db = TextVectorDatabase(user_id=user_id, file_hash=file_hash)

    # TEMPORARY! - i dont want to perform this twice, either save page # with each chunk or a seperate dict/csv with chunk # and original text portion
    raw_text: str = pdf_utils.PdfProcessor("pdf_files\The_Happy_Prince by Oscar Wilde.pdf", uploaded_by="kevin").getAll()
    chunks: list[str] = text_embedder.get_text_chunks(raw_text)

    if not is_file_uploaded(user_id=user_id, file_md5_hash=file_hash):
        # process pdf to chunks
        #raw_text: str = pdf_utils.PdfProcessor("D:/Documents/Coding/My projects/ai-study-tool/pdf_files/The_Happy_Prince by Oscar Wilde.pdf", uploaded_by="kevin").getAll()
        #chunks: list = text_embedder.get_text_chunks(raw_text)
        #query: list[str] = ["What does the crow symbolize?"]

        # convert text to embeddings
        embeddings, original_text= text_embedder.get_text_embeddings(chunks) # default is ["Birds can fly."] as a test - text must be a list
        #print(f"embeddings: {embeddings}\ntext: {original_text}")
    
        # store embeddings in qdrant
        print(f"\nAttempting to store embeddings in qdrant.")
       
        txt_vector_db.upload_vectors_qdrant(embeddings)
        save_hash(user_id=user_id, hash=file_hash)
    
    embedded_query = text_embedder.get_text_embeddings("What does the crow symbolize?")[0][0] # original format [ [ query_embeddings ] ]

    print('embeedded query:', embedded_query)
    results = txt_vector_db.search(embedded_query)
    payloads: list = [found.payload for found in results]
    
    chunk_idx: list[int] = [hit["chunk"] for hit in payloads]
    text_chunks = " ".join(chunks[idx] for idx in chunk_idx)

        
    #llm_instance = LlmChat()
    #llm_instance.create_chat_stream(text_chunks=text_chunks, prompt=str(query))
  

    #print("query type:", type(embedded_query.tolist()[0][0]))

    '''print("Run completed.")
    with open("data/embeddings.txt", "w+") as embeddings_txt:
        for embed in embeddings[0]:
            embeddings_txt.write(f"[{str(embed)}]")'''
    