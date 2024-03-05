import csv
import json
import ollama
from openai import OpenAI
import os
from tqdm import tqdm
from rag.mistral_with_documents import MistralWithDocuments

from pprint import pprint

from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    mistral_api_key=os.environ.get("MISTRAL_API_KEY")
    candidate = MistralWithDocuments(mistral_api_key, 'rag/data/')

    # Define the CSV file name
    filename = 'data_prep/data/mayo_clinic.csv'  # Replace 'your_file_name.csv' with the actual file name

    # Open the CSV file for reading
    with open(filename, 'r', newline='') as csvfile:
        # Create a CSV reader object
        reader = csv.reader(csvfile)
        
        # Skip the header row if your CSV has one
        next(reader, None)  # Comment out this line if there's no header
        
        # Iterate over each row in the CSV
        for row in reader:
            query = row[0]
            expected_answer = row[-1]
            candidate_answer = candidate.chat(query)

            eval_prompt = 'Respond in JSON with a key for "matches_content" where the value is True if the predicted answer matches the content of the expected answer (False otherwise) \
            and a key for "matches_style" where the value is True if the predicted answer matches the style of the expected answer.\n\nPredicted:{0}\n\nExpected:{1}'.format(candidate_answer, expected_answer)

            response = client.chat.completions.create(model='gpt-3.5-turbo', response_format={"type": "json_object"}, messages=[
            {
                'role': 'user',
                'content': eval_prompt,
            },
            ])
            response_dict = json.loads(response.choices[0].message.content)
            pprint(response_dict)
