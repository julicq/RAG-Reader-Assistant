# Text Analysis and Q&A Application

This is a Streamlit-based application that allows users to upload text documents (TXT, PDF, DOC, DOCX) and ask questions based on the content of these documents. The app uses embeddings to find the most relevant paragraphs and provides concise answers.

## Features

- **File Upload:** Supports TXT, PDF, DOC, and DOCX files.
- **Text Parsing:** Extracts and processes text from the uploaded documents.
- **Embeddings:** Generates embeddings for document paragraphs and user queries.
- **Similarity Search:** Finds the most relevant paragraphs based on cosine similarity.
- **Q&A:** Provides answers to user queries using the relevant paragraphs.
- **Progress Bar:** Displays a progress bar during file upload and processing.

## Installation

To install the required dependencies, run:

```bash
pip install streamlit ollama numpy pdfplumber python-docx PyPDF2
```

## Usage
To run the Streamlit application, use the following command:

```bash
streamlit run streamlit_app.py
```

## File Structure
- main_logic.py: Contains the core logic for parsing files, generating embeddings, and finding similar paragraphs.
- streamlit_app.py: The Streamlit UI that allows users to upload files and ask questions, with a progress bar for file processing.


## How It Works
- *Upload a File*: The user uploads a text document (TXT, PDF, DOC, DOCX).
- *Parse the File*: The app extracts text from the document and splits it into paragraphs.
- *Generate Embeddings*: The app generates embeddings for each paragraph using a specified model.
- *Ask a Question*: The user inputs a question.
- *Find Relevant Paragraphs*: The app finds the most relevant paragraphs based on cosine similarity of embeddings.
- *Get an Answer*: The app generates a concise answer using the most relevant paragraphs.