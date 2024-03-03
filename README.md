# Installation
This workshop utilizes multiple tools that can have conflicting requirements. Recommend using pyenv to manage separate python versions, then virtualenv for separate environments for each component (e.g. `data_prep`, `rag`).

# Introduction
In this workshop, we show the two main workflows when working with LLMs: RAG (retrieval-augmented generation) and fine-tuning. We show how to take a PDF and generate a dataset for fine-tuning and evaluation.

# Data Preparation
We utilize marker to turn PDFs into markdown, which can then be easily parsed into a format suitable for LLM consumption. Please reference the [marker docs](https://github.com/VikParuchuri/marker) for installation and setup. After it's successfully installed, convert the example PDF into markdown using `marker`.

Now that you have a suitable document, we'll turn it into a Q&A dataset using a local llm. First, install [Ollama](https://github.com/ollama/ollama). 

# Fine-tuning

# RAG

# Evals

