import os
import glob
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


class MistralWithDocuments:
    def __init__(self, api_key, data_folder, model="mistral-large-latest"):
        self.client = MistralClient(api_key=api_key)
        self.model = model
        self.messages = []
        self._load_files(data_folder)

    def _load_files(self, folder):
        for file_path in glob.glob(folder + "*.md"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    md_content = file.read()
                    self.messages.append(ChatMessage(role="system", content=md_content))
            except IOError as e:
                print(f"Error reading file {file_path}: {e}")

    def chat(self, prompt):
        try:
            chat_response = self.client.chat(
                model=self.model,
                messages=self.messages + [ChatMessage(role="user", content=prompt)],
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
    chat_instance = MistralWithDocuments(api_key, 'data/')

    # Sample chat
    response = chat_instance.chat("What's the main idea of the loaded documents?")
    print(response)
