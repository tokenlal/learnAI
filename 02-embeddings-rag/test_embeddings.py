#!/usr/bin/env python3
"""
Test Embedding Generation with Sentence Transformers
This script demonstrates how to generate embeddings using local Sentence Transformer models.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
import time

def test_embedding_generation():
    """Test basic embedding generation functionality."""
    print("🧠 Testing Sentence Transformer Embeddings")
    print("=" * 60)
    
    # Load the embedding model locally
    print("📥 Loading model: all-mpnet-base-v2...")
    start_time = time.time()
    model = SentenceTransformer("all-mpnet-base-v2")
    load_time = time.time() - start_time
    print(f"✅ Model loaded in {load_time:.2f} seconds\n")
    
    def get_embedding(text):
        """Get embedding for a piece of text."""
        return model.encode(text).tolist()
    
    # Test single text embedding
    print("🔍 Testing Single Text Embedding:")
    test_text = "I love programming in Python"
    embedding = get_embedding(test_text)
    
    print(f"Text: {test_text}")
    print(f"Embedding dimension: {len(embedding)}")
    print(f"First 10 values: {[f'{x:.4f}' for x in embedding[:10]]}")
    print(f"Data type: {type(embedding[0])}")
    print()
    
    # Test multiple texts
    print("📚 Testing Multiple Texts:")
    test_texts = [
        "I love programming in Python",
        "Python programming is my passion", 
        "I enjoy cooking Italian food",
        "Machine learning is fascinating",
        "Cooking pasta with fresh herbs"
    ]
    
    print("Generating embeddings for multiple texts...")
    embeddings = []
    for i, text in enumerate(test_texts):
        emb = get_embedding(text)
        embeddings.append(emb)
        print(f"{i+1}. {text[:40]}... → {len(emb)} dimensions")
    
    print()
    
    # Test cosine similarity
    print("📊 Testing Cosine Similarity:")
    
    def cosine_similarity(vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        return dot_product / (norm1 * norm2)
    
    # Compare similarities
    print("Similarity comparisons:")
    for i in range(len(test_texts)):
        for j in range(i + 1, len(test_texts)):
            similarity = cosine_similarity(embeddings[i], embeddings[j])
            print(f"Text {i+1} ↔ Text {j+1}: {similarity:.4f}")
            print(f"  '{test_texts[i][:30]}...' ↔ '{test_texts[j][:30]}...'")
    
    print()

def test_batch_processing():
    """Test batch processing for better performance."""
    print("⚡ Testing Batch Processing:")
    print("=" * 60)
    
    model = SentenceTransformer("all-mpnet-base-v2")
    
    # Test documents
    documents = [
        "Python is excellent for machine learning and data science applications.",
        "I love making Italian pasta with fresh tomatoes and basil leaves.",
        "Deep learning models can process large amounts of unstructured data.",
        "The best pizza requires a crispy crust and high-quality mozzarella.",
        "Natural language processing enables computers to understand human text.",
        "Cooking with fresh ingredients always produces the most flavorful meals.",
        "Artificial intelligence is transforming various industries worldwide.",
        "Mediterranean cuisine emphasizes olive oil, herbs, and fresh vegetables."
    ]
    
    # Single processing
    print("🐌 Single processing:")
    start_time = time.time()
    single_embeddings = []
    for doc in documents:
        embedding = model.encode(doc).tolist()
        single_embeddings.append(embedding)
    single_time = time.time() - start_time
    print(f"Time for {len(documents)} documents: {single_time:.4f} seconds")
    
    # Batch processing
    print("🚀 Batch processing:")
    start_time = time.time()
    batch_embeddings = model.encode(documents).tolist()
    batch_time = time.time() - start_time
    print(f"Time for {len(documents)} documents: {batch_time:.4f} seconds")
    print(f"Speedup: {single_time/batch_time:.2f}x faster")
    
    # Verify they're the same
    print(f"Results identical: {np.allclose(single_embeddings, batch_embeddings)}")
    print()

def test_similarity_search():
    """Test finding most similar documents to a query."""
    print("🔍 Testing Similarity Search:")
    print("=" * 60)
    
    model = SentenceTransformer("all-mpnet-base-v2")
    
    # Document collection
    documents = [
        "Python programming language for data science and machine learning",
        "Italian cooking with fresh pasta and tomato sauce", 
        "Machine learning algorithms for predictive analytics",
        "Homemade pizza with mozzarella cheese and basil",
        "Deep learning neural networks and artificial intelligence",
        "Mediterranean cuisine with olive oil and fresh herbs",
        "Data analysis using Python pandas and numpy libraries",
        "Traditional Italian recipes passed down through generations"
    ]
    
    # Generate embeddings for all documents
    print("📚 Generating embeddings for document collection...")
    doc_embeddings = model.encode(documents)
    
    # Test queries
    queries = [
        "What programming language is good for AI?",
        "How to make delicious Italian food?", 
        "Best practices for data analysis?"
    ]
    
    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    for query in queries:
        print(f"\n🔎 Query: '{query}'")
        query_embedding = model.encode([query])[0]
        
        # Calculate similarities
        similarities = []
        for i, doc_emb in enumerate(doc_embeddings):
            similarity = cosine_similarity(query_embedding, doc_emb)
            similarities.append((similarity, i, documents[i]))
        
        # Sort by similarity (highest first)
        similarities.sort(reverse=True)
        
        print("Top 3 most similar documents:")
        for rank, (sim, idx, doc) in enumerate(similarities[:3], 1):
            print(f"  {rank}. Similarity: {sim:.4f}")
            print(f"     Document: {doc}")
    
    print()

def performance_benchmark():
    """Benchmark embedding performance."""
    print("⏱️ Performance Benchmark:")
    print("=" * 60)
    
    model = SentenceTransformer("all-mpnet-base-v2")
    
    # Test different text lengths
    test_cases = [
        ("Short text", "Hello world"),
        ("Medium text", "This is a medium length sentence with several words to test embedding generation performance."),
        ("Long text", " ".join(["This is a very long text with many repeated sentences."] * 10))
    ]
    
    for name, text in test_cases:
        times = []
        for _ in range(5):  # Run 5 times for average
            start = time.time()
            embedding = model.encode([text])
            times.append(time.time() - start)
        
        avg_time = np.mean(times)
        print(f"{name}: {avg_time:.4f} seconds (avg of 5 runs)")
        print(f"  Text length: {len(text)} characters")
        print(f"  Embedding size: {embedding.shape}")
    
    print()

if __name__ == "__main__":
    print("🚀 Starting Sentence Transformer Embedding Tests")
    print("=" * 70)
    
    try:
        # Run all tests
        test_embedding_generation()
        test_batch_processing()
        test_similarity_search()
        performance_benchmark()
        
        print("✅ All tests completed successfully!")
        print("\n💡 Key Takeaways:")
        print("- Sentence Transformers work completely offline")
        print("- Batch processing is much faster than single processing")
        print("- all-mpnet-base-v2 produces 768-dimensional embeddings")
        print("- Cosine similarity effectively measures text similarity")
        print("- No API keys or internet connection required!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Make sure you have sentence-transformers installed:")
        print("pip install sentence-transformers")