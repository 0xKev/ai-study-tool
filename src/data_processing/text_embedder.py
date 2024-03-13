# splits the raw text into chunks of 1000 characters with 200 characters overlap
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS # only kept to test out sentenceTransformers but will remove bc qdrant 
from sentence_transformers import SentenceTransformer
import torch
import torch.nn.functional as F
from torch import Tensor
import numpy as np
from transformers import AutoModel, AutoTokenizer


def get_text_chunks(raw_text: str) -> list:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len
    )

    chunks = text_splitter.split_text(raw_text)
    
    return chunks

"""def embedd_to_vector(text: str) -> list: # most likely remove bc not using SentenceTransformer and will use automodel
    '''
    embedds the text into a list of strings
    '''
    model = SentenceTransformer("C:\LLM\embedder\SFR-Embedding-Mistral", device="cuda", cache_folder="src/models")
    embeddings = model.encode(text)
    vector_store = FAISS(text, embeddings)

    return vector_store"""

def last_token_pool(last_hidden_states: Tensor,
                 attention_mask: Tensor) -> Tensor:
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]


def get_text_embeddings(text: list = ["Birds can fly."]) -> tuple[list, list]:
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = AutoModel.from_pretrained("C:\LLM\embedder\SFR-Embedding-Mistral", device_map="cuda", torch_dtype=torch.float16)
    tokenizer = AutoTokenizer.from_pretrained("C:\LLM\embedder\SFR-Embedding-Mistral", device_map="cuda", torch_dtype=torch.float16)

    with torch.no_grad(): # model is pre-trained so gradients not needed
        max_length = 4096 # hard limit max is 4096
        input_texts = text
        batch_dict = tokenizer(input_texts, max_length=max_length, padding=True, truncation=True, return_tensors="pt").to(device)
        outputs = model(**batch_dict)
        embeddings = last_token_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
        embeddings = F.normalize(embeddings, p=2, dim=1)
        embeddings = embeddings.detach().cpu().numpy() 

        #print(f"vector size: {model.config.hidden_size}")
        #print(f"embeddings: {embeddings}")
    
    return embeddings, text

if __name__ == "__main__":
    print("Running get_text_embeddings()\n")
    embeddings, text = get_text_embeddings() # default is ["Birds can fly."] as a test - text must be a list
    print(f"\nembeddings: {embeddings}\ntext: {text}")
    #print(f"\nAttempting to store embeddings in qdrant.")
    #save_text_qdrant(user_id="test_user_id", file_name="the happy prince", file_type="pdf")
