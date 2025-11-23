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
- **FastAPI App**: http://localhost:8000
- **Attu (Milvus GUI)**: http://localhost:3000 (Visualize collections and data)
- **MinIO Console**: http://localhost:9001 (admin/minioadmin)
- **Milvus**: localhost:19530

---

## 🧪 Testing the RAG System

### Upload a Document
```bash
curl -X POST "http://localhost:8000/upload/" \
     -F "file=@app/sample.txt"
```

### Query the Document
```bash
curl -X POST "http://localhost:8000/query/" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "query=What are the health benefits of apples?&k=3"
```

### Using the Web Interface
1. Go to http://localhost:8000/docs
2. Try the `/upload/` endpoint to upload documents
3. Use the `/query/` endpoint to ask questions

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

## 🐛 Troubleshooting

### Backend Issues
- **Container startup fails**: Ensure Rancher Desktop/Docker is running
- **Network connectivity**: Disable VPN if having registry access issues
- **Port conflicts**: Check if ports 19530, 9000, 9001 are available

### Frontend Issues
- **Import errors**: Ensure virtual environment is activated and dependencies installed
- **API connection**: Verify Milvus containers are healthy before starting FastAPI
- **Gemini API errors**: Check your API key in `.env` file

### Common Commands
```bash
# Restart everything
./run-with-rancher.sh down
./run-with-rancher.sh up
source venv/bin/activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Check container health
./run-with-rancher.sh ps

# View application logs
./run-with-rancher.sh logs
```

---

## 🚀 Next Steps

- Add more document types support (PDF, DOCX)
- Implement user authentication
- Add conversation history
- Deploy to production environment
- Integrate with other LLM providers
