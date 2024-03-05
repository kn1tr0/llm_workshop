import glob
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import numpy as np
import os
import faiss



class RAG:
    def __init__(self, api_key, data_folder, model="mistral-large-latest"):
        self.client = MistralClient(api_key=api_key)
        self.model = model
        self.messages = []
        self.index = None
        self.chunks = []
        self._load_files(data_folder)
        

    def _load_files(self, folder):
        chunk_size = 2048

        for file_path in glob.glob(folder + "*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    md_content = file.read()
                    self.chunks += [md_content[i:i + chunk_size] for i in range(0, len(md_content), chunk_size)]
            except IOError as e:
                print(f"Error reading file {file_path}: {e}")

        text_embeddings = np.array([self._get_text_embedding(chunk) for chunk in self.chunks])
        if self.index is None:
            d = text_embeddings.shape[1]
            self.index = faiss.IndexFlatL2(d)
        self.index.add(text_embeddings)
    
    def _get_text_embedding(self, input):
        embeddings_batch_response = self.client.embeddings(
            model="mistral-embed",
            input=input
        )
        return embeddings_batch_response.data[0].embedding

    def chat(self, prompt):
        prompt_embeddings = np.array([self._get_text_embedding(prompt)])
        D, I = self.index.search(prompt_embeddings, k=2) # distance, index
        retrieved_chunk = [self.chunks[i] for i in I.tolist()[0]]

        augmented_prompt = f"""
        Context information is below.
        ---------------------
        {retrieved_chunk}
        ---------------------
        Given the context information and not prior knowledge, answer the query.
        Query: {prompt}
        Answer:
        """
        try:
            chat_response = self.client.chat(
                model=self.model,
                messages=self.messages + [ChatMessage(role="user", content=augmented_prompt)],
            )
            return chat_response.choices[0].message.content
        except Exception as e:
            print(f"Error during chat completion: {e}")
            return None


# Example usage
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    api_key=os.environ.get("MISTRAL_API_KEY")
    chat_instance = RAG(api_key, 'data/')

    # Sample chat
    response = chat_instance.chat("What is chronic pain?")
    print(response)