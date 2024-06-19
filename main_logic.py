import ollama
import os
import json
import numpy as np
from numpy.linalg import norm
import docx
import pdfplumber
from io import StringIO
from docx import Document
from PyPDF2 import PdfReader

def parse_file(filename):
    if filename.endswith('.txt'):
        return parse_txt_file(filename)
    elif filename.endswith('.pdf'):
        return parse_pdf_file(filename)
    elif filename.endswith('.doc') or filename.endswith('.docx'):
        return parse_doc_file(filename)
    else:
        raise ValueError("Unsupported file format")

def parse_txt_file(filename):
    with open(filename, encoding="utf-8-sig") as f:
        paragraphs = []
        buffer = []
        for line in f.readlines():
            line = line.strip()
            if line:
                buffer.append(line)
            elif buffer:
                paragraphs.append(" ".join(buffer))
                buffer = []
        if buffer:
            paragraphs.append(" ".join(buffer))
        return paragraphs

def parse_pdf_file(filename):
    with pdfplumber.open(filename) as pdf:
        paragraphs = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                paragraphs.extend(text.split('\n\n'))
        return paragraphs

def parse_doc_file(filename):
    doc = Document(filename)
    paragraphs = [p.text for p in doc.paragraphs if p.text]
    return paragraphs

def save_embeddings(filename, embeddings):
    if not os.path.exists("embeddings"):
        os.makedirs("embeddings")
    with open(f"embeddings/{filename}.json", "w") as f:
        json.dump(embeddings, f)

def load_embeddings(filename):
    filepath = f"embeddings/{filename}.json"
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r") as f:
        return json.load(f)

def get_embeddings(filename, modelname, chunks):
    embeddings = load_embeddings(filename)
    if embeddings:
        return embeddings
    embeddings = [
        ollama.embeddings(model=modelname, prompt=chunk)["embedding"]
        for chunk in chunks
    ]
    save_embeddings(filename, embeddings)
    return embeddings

def find_most_similar(needle, haystack):
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

def get_response(paragraphs, embeddings, prompt, model="llama3"):
    SYSTEM_PROMPT = """You are a helpful reading assistant who answers questions 
        based on snippets of text provided in context. Answer only using the context provided, 
        being as concise as possible. If you're unsure, just say that you don't know.
        Context:
    """
    prompt_embedding = ollama.embeddings(model="nomic-embed-text", prompt=prompt)["embedding"]
    most_similar_chunks = find_most_similar(prompt_embedding, embeddings)[:5]

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT + "\n".join(paragraphs[item[1]] for item in most_similar_chunks),
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response["message"]["content"]
