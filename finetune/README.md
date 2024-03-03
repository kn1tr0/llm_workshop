# Fine-tuning
Clone the Fine-tuning Mistral 7B studio from Lightning AI. Then, upload your CSV generated from the markdown file. Remember, the CSV has to have the headers `instruction`, `input`, and `output`.

## Data Preparation
Change the existing data preparation command to use your uploaded csv:

`!python llm-finetune/prepare_dataset.py --dataset csv --csv_path mayo_clinic.csv`

## Fine-tuning
Change the existing dataset source to your custom csv:

`!python llm-finetune/finetune.py --dataset csv`

Once it's successfully training, you should see the loss and iteration time logs.

## Known Bugs
The `pandas` library is missing, so create a code cell and install it via `!pip install pandas` then rerun the data preparation command.