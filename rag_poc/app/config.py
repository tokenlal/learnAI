import os
from dotenv import load_dotenv

load_dotenv()

# Update DIMENSION to 768 for the chosen embedding model ("all-mpnet-base-v2")
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_collection")
DIMENSION = int(os.getenv("DIMENSION", "768"))

# No need for OPENAI_API_KEY anymore
