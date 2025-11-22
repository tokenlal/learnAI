# Running RAG POC with Rancher Desktop

## ✅ **Rancher Desktop Setup Confirmed**

Your system is properly configured with:
- ✅ Rancher Desktop installed and running
- ✅ Docker CLI available via Rancher Desktop (version 28.3.3-rd)
- ✅ Docker Compose available (version v2.40.3)

## 🚀 **Quick Start**

Use the provided script to manage the project:

```bash
# Start services
./run-with-rancher.sh up

# Stop services  
./run-with-rancher.sh down

# View logs
./run-with-rancher.sh logs

# Check status
./run-with-rancher.sh ps
```

## 🔧 **Manual Docker Commands**

If you prefer to run Docker commands manually:

```bash
# Set PATH for Rancher Desktop
export PATH="/Applications/Rancher Desktop.app/Contents/Resources/resources/darwin/bin:$PATH"

# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f
```

## 🐛 **Troubleshooting**

### Network Connectivity Issues

If you encounter "Error response from daemon: Get https://registry-1.docker.io/v2/: EOF":

1. **Check Rancher Desktop Settings:**
   - Open Rancher Desktop
   - Go to Preferences → Container Engine
   - Ensure "dockerd (moby)" is selected
   - Try switching network settings if available

2. **Reset Rancher Desktop:**
   - Quit Rancher Desktop completely
   - Restart it
   - Wait for it to fully initialize

3. **Alternative: Use Local Images**
   - Pre-pull images when connectivity is working
   - Use offline mode for development

### If Registry Issues Persist

You can try these alternatives:

1. **Use different image registries:**
   ```bash
   # Pull from alternative registries
   docker pull ghcr.io/milvusdb/milvus:v2.5.7
   ```

2. **Manual installation:**
   - Install Milvus using local binaries
   - Use SQLite as vector database alternative
   - Run services natively on macOS

## 🔄 **Development Workflow**

1. **Start Infrastructure:**
   ```bash
   ./run-with-rancher.sh up
   ```

2. **Verify Services:**
   ```bash
   ./run-with-rancher.sh ps
   ```

3. **Run the FastAPI Application:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Run the app
   uvicorn app.main:app --reload
   ```

4. **Test the Application:**
   - Upload documents: `POST http://localhost:8000/upload/`
   - Query documents: `POST http://localhost:8000/query/`

## 🌐 **Service URLs**

When running with Rancher Desktop:
- **FastAPI App:** http://localhost:8000
- **Milvus:** http://localhost:19530  
- **MinIO Console:** http://localhost:9001
- **MinIO API:** http://localhost:9000

## 📝 **Notes**

- The docker-compose.yml has been updated to remove obsolete version specification
- Rancher Desktop uses containerd by default, which might have different networking behavior
- All functionality should work the same as with Docker Desktop
- Container data is stored in Rancher Desktop's virtual machine

## 🆘 **Need Help?**

If issues persist:
1. Check Rancher Desktop logs in the app
2. Try switching container runtimes in Rancher Desktop settings
3. Consider using Docker Desktop as alternative
4. Use the native Python setup with SQLite for development