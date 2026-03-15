import fitz  # PyMuPDF for better PDF extraction (pip install pymupdf)
import pyttsx3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

# Voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    try:
        engine.stop()
        engine.say(str(text))
        engine.runAndWait()
    except Exception as e:
        print("Voice error:", e)

print("Loading AI model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

def read_pdf(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found. Download a policy PDF and place it here.")
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    doc.close()
    print(f"Extracted {len(text)} chars from PDF.")
    return text

def split_text(text, size=200, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), size - overlap):
        chunks.append(" ".join(words[i:i+size]))
    return chunks

print("Reading PDF...")
pdf_text = read_pdf("C:/Users/pooja/OneDrive/Desktop/policy.pdf")

if not pdf_text.strip():
    raise ValueError("PDF text extraction failed. Try another PDF or check file.")

chunks = split_text(pdf_text)
print(f"Created {len(chunks)} chunks.")

print("Creating embeddings...")
embeddings = model.encode(chunks)
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings).astype('float32'))

print("Chatbot ready! Handles 100+ questions efficiently.")

while True:
    question = input("\nAsk a question: ")
    if question.lower() == "exit":
        break

    q_embedding = model.encode([question])
    D, I = index.search(np.array(q_embedding).astype('float32'), k=1)
    score = D[0][0]
    result = chunks[I[0][0]]

    if score > 0.8:  # Tuned threshold: lower = stricter match
        answer = "Please ask relevant questions."
    else:
        answer = result

    print("Bot:", answer)
    speak(answer)