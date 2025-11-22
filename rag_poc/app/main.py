from fastapi import FastAPI, UploadFile, File, Form
from app.milvus_client import create_collection, insert_embeddings, search_embeddings
from app.embedding_utils import get_embedding
from app.chunk_utils import chunk_text
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"

app = FastAPI()

@app.on_event("startup")
def startup_event():
    create_collection()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    text = content.decode("utf-8")
    chunks = chunk_text(text)
    embeddings = [get_embedding(chunk) for chunk in chunks]
    insert_embeddings(embeddings, chunks)
    return {"message": f"Inserted {len(chunks)} chunks."}

def build_prompt(query: str, context_chunks: list[str]) -> str:
    """
    Build a strict prompt to prevent hallucination from the LLM.
    """
    prompt = (
        "You are an AI assistant that answers questions strictly based on the provided Context Documents.\n"
        "If the answer cannot be found in the documents, you must respond with exactly: \"I don't know\".\n"
        "Do not use outside knowledge. Do not make up or guess answers.\n\n"
        f"QUESTION: {query}\n"
        "=========\n"
    )

    for i, chunk in enumerate(context_chunks):
        prompt += f"Context Document {i+1}:\n{chunk.strip()}\n\n"

    prompt += "=========\nAnswer:"
    return prompt

@app.post("/query/")
async def query_text(query: str = Form(...), k: int = Form(default=5)):
    query_embedding = get_embedding(query)
    top_chunks = search_embeddings(query_embedding, k)

    prompt = build_prompt(query, top_chunks)

    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent",
        headers={
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        },
        json={
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ]
        }
    )

    if response.status_code != 200:
        return {"error": f"Failed to get response from Gemini API: {response.text}"}

    answer = response.json()["candidates"][0]["content"]["parts"][0]["text"].strip()

    # 🚨 Post-filter: check if answer seems hallucinated
    context_text = " ".join(chunk.lower() for chunk in top_chunks)
    hallucination_cues = ["here is", "generally", "commonly", "typically", "usually"]

    if ("i don't know" not in answer.lower() and
        query.lower() not in context_text and
        any(cue in answer.lower() for cue in hallucination_cues)):
        answer = "I don't know"

    return {
        "query": query,
        "top_chunks": top_chunks,
        "answer": answer
    }
