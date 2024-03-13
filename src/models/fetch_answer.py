from openai import OpenAI
from dotenv import load_dotenv
from os import getenv

class LlmChat:
    def __init__(self, model: str = "OPEN-API-KEY"):
        load_dotenv()
        OPEN_AI_API_KEY = getenv(model)
        
        self.client = OpenAI(api_key=OPEN_AI_API_KEY)

    def test(self):  # Indentation corrected
        print(self.client.models.list())

    def create_chat_stream(self, text_chunks: str, prompt: str):
        stream = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {"role": "system", "content": "Refer to the following text:" + text_chunks + "and answer the query."},
                {"role": "user", "content": "Query:" + prompt}
            ],
            stream=True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="")

if __name__ == "__main__":
    llm_instance = LlmChat() 
    llm_instance.create_chat_stream()    