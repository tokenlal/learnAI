from sentence_transformers import SentenceTransformer

# Load the embedding model locally
model = SentenceTransformer("all-mpnet-base-v2")

def get_embedding(text: str):
    # Encode the text and convert the numpy array to list
    return model.encode(text).tolist()
