from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from app.config import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME, DIMENSION

def connect_milvus():
    connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)

def create_collection():
    connect_milvus()
    
    # If the collection exists, check the dimension of the "embedding" field.
    if utility.has_collection(COLLECTION_NAME):
        collection = Collection(COLLECTION_NAME)
        # Lookup the embedding field by iterating over the fields list.
        embedding_field = next((field for field in collection.schema.fields if field.name == "embedding"), None)
        current_dim = None
        if embedding_field:
            # Try to get the dimension either as an attribute or from params.
            current_dim = getattr(embedding_field, "dim", None) or (embedding_field.params.get("dim") if hasattr(embedding_field, "params") else None)
        if current_dim != DIMENSION:
            print(f"Collection exists but dimension ({current_dim}) does not match expected {DIMENSION}. Dropping collection...")
            utility.drop_collection(COLLECTION_NAME)
        else:
            print("Collection already exists with the correct dimension.")
    
    # Create collection if it doesn't exist now
    if not utility.has_collection(COLLECTION_NAME):
        print("Creating new collection...")
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
            FieldSchema(name="chunk", dtype=DataType.VARCHAR, max_length=2048)
        ]
        schema = CollectionSchema(fields, description="Document chunks for RAG")
        collection = Collection(name=COLLECTION_NAME, schema=schema)
        
        print("Creating index on embedding field...")
        collection.create_index(
            field_name="embedding",
            index_params={
                "metric_type": "L2",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
        )
        print("Index created.")
    else:
        print("Using existing collection.")
        collection = Collection(COLLECTION_NAME)
        # If the index is missing, create it.
        if not collection.has_index():
            print("Index not found, creating index...")
            collection.create_index(
                field_name="embedding",
                index_params={
                    "metric_type": "L2",
                    "index_type": "IVF_FLAT",
                    "params": {"nlist": 128}
                }
            )
            print("Index created.")
    
    # Load the collection if it contains data.
    if collection.num_entities > 0:
        print("Loading collection...")
        collection.load()
        print("Collection loaded.")
    else:
        print("Collection is empty; skipping load().")
    
    return collection

def insert_embeddings(embeddings, chunks):
    collection = Collection(COLLECTION_NAME)
    # Since 'id' is auto-generated, only provide values for 'embedding' and 'chunk'
    collection.insert([embeddings, chunks])
    collection.flush()

def search_embeddings(query_embedding, k=5):
    collection = Collection(COLLECTION_NAME)
    if collection.num_entities > 0:
        collection.load()
    results = collection.search(
        data=[query_embedding],
        anns_field="embedding",
        param={"metric_type": "L2", "params": {"nprobe": 10}},
        limit=k,
        output_fields=["chunk"]
    )
    return [hit.entity.get("chunk") for hit in results[0]]
