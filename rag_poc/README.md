# FastAPI RAG Project with Gemini AI

This project is a FastAPI-based RAG (Retrieval-Augmented Generation) application that uses Milvus vector database for document storage and Google's Gemini 2.0 Flash model for intelligent question answering.

---

## 🚀 Prerequisites

Before you begin, ensure you have the following installed:

- **Rancher Desktop** or **Docker Desktop** (for running Milvus containers)
- **Python 3.8+** for the FastAPI application
- **Gemini API Key** from Google AI Studio

---

## 📋 Project Architecture

- **Milvus**: Vector database for storing document embeddings
- **FastAPI**: Web API for document upload and querying
- **Sentence Transformers**: Local embedding model (all-mpnet-base-v2)
- **Gemini 2.0 Flash**: LLM for generating responses

---

## 🛠️ Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd rag_poc
```

### 2. Configure Environment Variables
Create a `.env` file with your Gemini API key:
```bash
GEMINI_API_KEY=your-gemini-api-key-here
MILVUS_HOST=localhost
MILVUS_PORT=19530
```

### 3. Start Milvus Backend (Vector Database)

#### Option A: Using Rancher Desktop (Recommended for macOS)
```bash
# Make the script executable
chmod +x run-with-rancher.sh

# Start all Milvus services
./run-with-rancher.sh up

# Check status
./run-with-rancher.sh ps

# View logs
./run-with-rancher.sh logs

# Stop services
./run-with-rancher.sh down
```

#### Option B: Using Docker Desktop
```bash
# Start services
docker compose up -d

# Check status
docker compose ps

# Stop services
docker compose down
```

### 4. Start FastAPI Application (Frontend)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

---

## 🌐 Accessing the Application

Once both backend and frontend are running:

- **API Documentation**: http://localhost:8000/docs (Interactive Swagger UI)
- **FastAPI App**: http://localhost:8000 (Main web interface for document upload and queries)
- **Attu (Milvus GUI)**: http://localhost:3000 (Visual management of Milvus collections)
- **MinIO Console**: http://localhost:9001 (Storage backend - login: minioadmin/minioadmin)
- **Milvus Server**: localhost:19530 (Vector database port)

### 📊 Attu - Milvus Visual Management Tool

**Attu** is a powerful GUI administration tool for Milvus that allows you to:

#### Features:
- 🔍 **Browse Collections**: View all your vector collections and their schemas
- 📈 **Monitor Statistics**: Check collection size, entity count, and index status
- 🔎 **Search Interface**: Test similarity searches directly in the UI
- 🗂️ **Data Management**: Insert, update, or delete vectors and entities
- ⚙️ **Configuration**: Manage indexes, partitions, and collection settings
- 📊 **Performance Metrics**: Monitor query performance and resource usage

#### How to Use Attu:
1. Navigate to http://localhost:3000
2. Connect to Milvus server (default: `milvus-standalone:19530`)
3. Browse your collections (look for `rag_collection` - the default collection name)
4. View collection details:
   - **Schema**: See the fields (id, embedding, chunk)
   - **Index**: Check the index type (IVF_FLAT) and metric (COSINE)
   - **Entities**: View total document count
5. Use the Query interface to test vector searches
6. Monitor collection statistics and health

#### Attu Connection Details:
- **Host**: `milvus-standalone` (Docker network) or `localhost` (from host machine)
- **Port**: `19530`
- **Connection automatically configured** via docker-compose environment variables

---

## 🧪 Testing the RAG System

### 1. Upload a Document
Upload a text document to the vector database:

```bash
curl -X POST "http://localhost:8000/upload/" \
     -F "file=@app/sample.txt"
```

**Expected Response:**
```json
{"message":"Inserted 7 chunks."}
```

### 2. Upload Vegetables Document
```bash
curl -X POST "http://localhost:8000/upload/" \
     -F "file=@app/vegetables.txt"
```

### 3. Query the Document
Ask questions about your uploaded documents:

```bash
curl -X POST "http://localhost:8000/query/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "query=What are the health benefits of apples?&k=3"
```

**Parameters:**
- `query`: Your question
- `k`: Number of similar chunks to retrieve (default: 5)

**Response includes:**
- Query text
- Top matching chunks from the database
- AI-generated answer from Gemini based on retrieved context

### 4. Query with Different Parameters
```bash
# Get more context (top 5 chunks)
curl -X POST "http://localhost:8000/query/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "query=What vegetables are good for health?&k=5"

# Quick answer with fewer chunks
curl -X POST "http://localhost:8000/query/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "query=Tell me about tomatoes&k=2"
```

### 5. Using the Web Interface
1. Navigate to http://localhost:8000 (Main UI)
2. Or use http://localhost:8000/docs (Interactive Swagger API docs)
3. Upload documents via the web form or API
4. Ask questions and get AI-powered answers

---

## 🔧 Development Workflow

1. **Start Backend Services**:
   ```bash
   ./run-with-rancher.sh up
   ```

2. **Start FastAPI Development Server**:
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Upload Sample Document**:
   ```bash
   curl -X POST "http://localhost:8000/upload/" -F "file=@app/sample.txt"
   ```

4. **Test Querying**:
   ```bash
   curl -X POST "http://localhost:8000/query/" \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "query=Tell me about apple varieties&k=5"
   ```

---

## 📂 Project Structure

```
rag_poc/
├── app/
│   ├── main.py              # FastAPI application
│   ├── milvus_client.py     # Milvus database operations
│   ├── embedding_utils.py   # Text embedding utilities
│   ├── chunk_utils.py       # Document chunking
│   ├── config.py           # Configuration settings
│   └── sample.txt          # Sample document for testing
├── docker-compose.yml       # Milvus services configuration
├── requirements.txt         # Python dependencies
├── run-with-rancher.sh     # Helper script for Rancher Desktop
├── .env                    # Environment variables
└── README.md               # This file
```

---

## 🔧 Advanced Commands & Management

### Docker Container Management

#### Check Container Status
```bash
docker compose ps
```

#### View Container Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f standalone  # Milvus
docker compose logs -f minio       # Storage
docker compose logs -f etcd        # Metadata
docker compose logs -f attu        # GUI
```

#### Restart Services
```bash
# Restart all services
docker compose restart

# Restart specific service
docker compose restart standalone
```

#### Stop and Remove Everything
```bash
# Stop containers (keeps data)
docker compose down

# Stop and remove all data (DESTRUCTIVE!)
docker compose down -v
```

### Milvus Collection Management

#### Drop and Recreate Collection (Python)
Use this if you need to change the schema or reset data:

```bash
cd /path/to/rag_poc
source venv/bin/activate

python3 << 'EOF'
from pymilvus import connections, utility
from app.config import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME

connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)

if utility.has_collection(COLLECTION_NAME):
    print(f"Dropping collection '{COLLECTION_NAME}'...")
    utility.drop_collection(COLLECTION_NAME)
    print("✅ Collection dropped successfully!")
else:
    print(f"Collection '{COLLECTION_NAME}' does not exist.")

connections.disconnect("default")
EOF
```

#### List All Collections
```bash
python3 << 'EOF'
from pymilvus import connections, utility
from app.config import MILVUS_HOST, MILVUS_PORT

connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
collections = utility.list_collections()
print(f"Collections: {collections}")
connections.disconnect("default")
EOF
```

#### Check Collection Statistics
```bash
python3 << 'EOF'
from pymilvus import connections, Collection
from app.config import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME

connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
collection = Collection(COLLECTION_NAME)
print(f"Collection: {COLLECTION_NAME}")
print(f"Total entities: {collection.num_entities}")
print(f"Schema: {collection.schema}")
connections.disconnect("default")
EOF
```

### Server Management

#### Kill FastAPI Server
```bash
# Find the process
lsof -i :8000

# Kill by process ID
kill -9 <PID>

# Or kill all uvicorn processes
pkill -f "uvicorn app.main:app"
```

#### Restart FastAPI Server
```bash
cd /path/to/rag_poc
source venv/bin/activate

# Start in foreground (see logs)
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Or start in background
nohup uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 > server.log 2>&1 &

# View logs
tail -f server.log
```

#### Check Server Logs
```bash
# View last 50 lines
tail -50 server.log

# Follow logs in real-time
tail -f server.log

# Search for errors
grep -i error server.log
```

### Network & Port Debugging

#### Check What's Using a Port
```bash
lsof -i :8000   # FastAPI
lsof -i :19530  # Milvus
lsof -i :3000   # Attu
lsof -i :9000   # MinIO API
lsof -i :9001   # MinIO Console
```

#### Test API Connectivity
```bash
# Test FastAPI
curl http://localhost:8000/

# Test Milvus (returns HTML if running)
curl http://localhost:19530/

# Test Attu
curl http://localhost:3000/
```

---

## 🐛 Troubleshooting

### Backend Issues

#### Container Startup Fails
```bash
# Check Docker/Rancher Desktop is running
docker ps

# Check available ports
lsof -i :19530
lsof -i :9000
lsof -i :9001
lsof -i :3000

# View detailed logs
docker compose logs -f standalone
```

#### Milvus Connection Errors
```bash
# Verify Milvus is healthy
docker compose ps

# Check Milvus logs
docker compose logs standalone | tail -50

# Test connection manually
python3 -c "from pymilvus import connections; connections.connect('default', host='localhost', port='19530'); print('✅ Connected!')"
```

#### Metric Type Mismatch Error
If you see `metric type not match: invalid parameter[expected=L2][actual=COSINE]`:

```bash
# This means the collection was created with a different metric
# Solution: Drop and recreate the collection
python3 << 'EOF'
from pymilvus import connections, utility
from app.config import MILVUS_HOST, MILVUS_PORT, COLLECTION_NAME

connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
utility.drop_collection(COLLECTION_NAME)
print("Collection dropped. Restart the server to recreate.")
connections.disconnect("default")
EOF

# Then restart FastAPI server
pkill -f "uvicorn app.main:app"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend Issues

#### Import Errors
```bash
# Verify virtual environment is activated
which python  # Should show venv path

# If not activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

#### Port Already in Use
```bash
# Find and kill the process
lsof -i :8000
kill -9 <PID>

# Or kill all uvicorn
pkill -f uvicorn
```

#### Gemini API Errors
```bash
# Check API key is set
cat .env | grep GEMINI_API_KEY

# Test API key
curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H "Content-Type: application/json" \
  -H "X-goog-api-key: YOUR_API_KEY" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'
```

### Database Issues

#### Collection Not Found
The collection is created automatically on first upload. If missing:

```bash
# Option 1: Upload a document to trigger creation
curl -X POST "http://localhost:8000/upload/" -F "file=@app/sample.txt"

# Option 2: Restart the server (creates collection on startup)
pkill -f uvicorn
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

#### Dimension Mismatch
If you changed the embedding model:

```bash
# Drop the old collection
python3 << 'EOF'
from pymilvus import connections, utility
connections.connect("default", host="localhost", port="19530")
utility.drop_collection("rag_collection")
connections.disconnect("default")
EOF

# Restart server to recreate with new dimensions
```

### Complete System Reset

```bash
# 1. Stop all containers
docker compose down

# 2. Remove all data (DESTRUCTIVE - deletes all uploaded documents)
docker compose down -v
rm -rf volumes/

# 3. Kill FastAPI server
pkill -f uvicorn

# 4. Start fresh
docker compose up -d
sleep 30  # Wait for containers to be healthy

# 5. Start FastAPI
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# 6. Upload test document
curl -X POST "http://localhost:8000/upload/" -F "file=@app/sample.txt"
```

### Common Commands Summary
```bash
# Restart everything
docker compose down && docker compose up -d
pkill -f uvicorn && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 &

# Check everything is running
docker compose ps
lsof -i :8000

# View logs
docker compose logs -f
tail -f server.log

# Test the system
curl -X POST "http://localhost:8000/upload/" -F "file=@app/sample.txt"
curl -X POST "http://localhost:8000/query/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "query=test query&k=3"
```

---

## 📊 Key Technical Details

### Similarity Metric: COSINE
This system uses **COSINE similarity** (not L2 Euclidean distance) for semantic search because:
- ✅ Better for normalized embeddings (sentence-transformers produces normalized vectors)
- ✅ Focuses on direction/meaning rather than magnitude
- ✅ More intuitive for semantic similarity
- ✅ Industry standard for text embeddings

### Embedding Model: all-mpnet-base-v2
- **Dimensions**: 768
- **Type**: Sentence Transformers
- **Performance**: Excellent balance of speed and accuracy
- **Local**: No API calls required, runs on your machine

### Index Type: IVF_FLAT
- **Algorithm**: Inverted File Index with flat (exact) search within clusters
- **Clusters (nlist)**: 128
- **Search Parameter (nprobe)**: 10 clusters searched per query
- **Trade-off**: Balanced between speed and accuracy

---

## 🚀 Next Steps

### Features to Add
- 📄 Support more document types (PDF, DOCX, Markdown)
- 🔐 Implement user authentication and authorization
- 💬 Add conversation history and context memory
- 🎨 Enhanced UI with real-time streaming responses
- 📊 Analytics dashboard for query patterns
- 🔄 Document versioning and updates

### Deployment Options
- 🐳 Docker containerization for full stack
- ☁️ Deploy to cloud (AWS, GCP, Azure)
- 🚀 Use managed Milvus (Zilliz Cloud)
- 🔄 Add load balancing and horizontal scaling

### Integration Ideas
- 🤖 Support multiple LLM providers (OpenAI, Anthropic, Cohere)
- 🔗 Connect to external knowledge bases
- 📧 Email/Slack integration for queries
- 🎯 Fine-tune embeddings for domain-specific content

---

## 📚 Additional Resources

- **Milvus Documentation**: https://milvus.io/docs
- **Attu GitHub**: https://github.com/zilliztech/attu
- **Sentence Transformers**: https://www.sbert.net/
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Gemini API**: https://ai.google.dev/

---

## 💡 Tips & Best Practices

1. **Regular Backups**: Use `docker compose down` (without `-v`) to preserve data
2. **Monitor Performance**: Check Attu regularly for collection health
3. **Batch Uploads**: Upload multiple documents at once for better performance
4. **Optimize Chunks**: Experiment with chunk sizes (current: ~500 chars)
5. **API Rate Limits**: Be mindful of Gemini API quotas
6. **Collection Naming**: Use descriptive names for multiple collections
7. **Version Control**: Keep track of embedding model versions

---

## 🤝 Contributing

Found an issue or want to contribute? Feel free to open issues or pull requests!

---

## 📝 License

This project is for educational purposes. Check individual component licenses:
- Milvus: Apache 2.0
- FastAPI: MIT
- Sentence Transformers: Apache 2.0
