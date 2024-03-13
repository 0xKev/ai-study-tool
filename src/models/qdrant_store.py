"""
Qdrant Structure:
    - One collection with payload based partioning (https://qdrant.tech/documentation/guides/multiple-partitions/)
    - metadata (user_id, file_name, file_type[pdf, txt, doc, etc], file hash (to check if exist)

To Do:
    - create collection called 'text collection (only need one collection for all users for now)  
    - user requests for pdf 
    - search collection by user_id (group_id) and pdf_name to check if exist
    - if not then text embeddor to qdrant
    -
"""
import sys    
print("In module products sys.path[0], __package__ ==", sys.path[0], __package__)

from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct, Distance, VectorParams
from dotenv import load_dotenv
import os

class TextVectorDatabase:
    def __init__(self, user_id: str, file_hash: str):
        load_dotenv()
        self.__QDRANT_API_KEY = os.getenv("QDRANT-API-KEY")

        self.collection_name = "text collection"
        self.user_id = user_id
        self.file_hash = file_hash
        self.client = QdrantClient(
            location="localhost",
            port=6333,
            https=True,
            api_key=self.__QDRANT_API_KEY
        )
        self._unique_id = self.user_id + self.file_hash[:7]



    def _collection_not_exists(self) -> bool:
        all_collections = self.client.get_collections().collections

        not_exists = not any(collection.name == self.collection_name for collection in all_collections) # return True if any true

        return not_exists


    def upload_vectors_qdrant(self, embeddings: list) -> None:
    # Create collection if doesn't exist
        if self._collection_not_exists():
            print(self.collection_name, "does not exist! Creating now...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=4096, distance=Distance.COSINE),
                hnsw_config=models.HnswConfigDiff( # used to index vectors for each user indepdently instead of global
                    payload_m=16, 
                    m=0 # disables building global index for whole collection
                )
            ) # change recreate to create - only using recreate for testing rn
            print(f"Collection created with the parameters (collection_name={self.collection_name}, vector_size=4096, distance=Distance.COSINE)")
        
        # need unique id for PointStruct, can just randomize auto generate but maybe 
        # upload_records meant for multiple vectors in one load, but cant add payload so not viable
        # create own batches of pointstruct with payloads to send
        # payload metadata contain user_id and file_hash for searches instead of filename and filetype bc not important
        # example: payload=f"{'user_id': '{user_id}', 'file_hash': '{file_hash}'}"
            num_of_data: int = len(embeddings)
        
        #unique_id = [{f"'id': '{get_unique_id(user_id, file_hash)}_{num}'"} for num in range(num_of_data)]
        #print("unique id:", unique_id)
        #not sure how to use my own unique ids instead of auto generated
        #chunk_num: list = [chunk for chunk in range(num_of_data)]
            metadata: list[dict] = [
                {
                    "user_id": self.user_id, 
                    "file_hash": self.file_hash, 
                    "chunk": num,
                    "unique_id": self._unique_id 
                } for num in range(num_of_data) 
            ]

        
            self.client.upload_collection(
                collection_name=self.collection_name,
                vectors=embeddings,
                payload=metadata,
            )

            self.create_payload_index()

            print("Success")

    def create_payload_index(self):
        #https://qdrant.tech/documentation/concepts/indexing/#payload-index 
        # the more different values a payload value has, the more efficiently the index will be used.
        self.client.create_payload_index(
            collection_name=self.collection_name,
            field_name="unique_id",
            field_schema=models.PayloadSchemaType.KEYWORD
        )

    def search(self, query_vector: list):
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="unique_id",
                        match=models.MatchValue(
                            value=self._unique_id
                        )
                    ),
                ]
            ),
            query_vector=query_vector,
            limit=5
        )
        return search_result

if __name__ == "__main__":
    test = TextVectorDatabase("kevin777", "d41d8cd98f00b204e9800998ecf8427e")
