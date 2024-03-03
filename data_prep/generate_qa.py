import csv
import json
import ollama
from openai import OpenAI
import os
from tqdm import tqdm
from utilities import parse_markdown_sections


from dotenv import load_dotenv
load_dotenv()


if __name__ == '__main__':
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    prompt = 'Respond in JSON with a key for "question" and "answer" where the value for "question" is a question where the below paragraph is the answer,\
            the value for "answer" is the answer adapted from the below paragraph.\n\n'
    
    file_path = 'data/mayo_clinic.md'
    qa_file_path = file_path.split('.')[0] + '.csv'
    # Open the file for writing ('w' mode to overwrite if exists, 'a' mode to append)
    with open(qa_file_path, 'w', newline='') as csvfile:
        # Define the column titles
        fieldnames = ['instruction', 'input', 'output']
        
        # Create a writer object specifying the fieldnames
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write the header row
        writer.writeheader()
        sections = parse_markdown_sections(file_path)

        for title, content in tqdm(sections.items()):
            formatted_content = f"Section: {title}\nContent:\n{content}\n"
            prompt_with_content = prompt + formatted_content

            response = client.chat.completions.create(model='gpt-3.5-turbo', response_format={"type": "json_object"}, messages=[
            {
                'role': 'user',
                'content': prompt_with_content,
            },
            ])
            response_dict = json.loads(response.choices[0].message.content)
            print(response_dict)

            # Zip the fieldnames to the row's data to create a dictionary
            row = (response_dict['question'], '', response_dict['answer'])
            row_dict = dict(zip(fieldnames, row))
            writer.writerow(row_dict)