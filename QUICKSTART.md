# Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Keys (1 minute)
Edit `config/application.properties` and add your OpenAI API key:
```properties
OPENAI_API_KEY=sk-proj-your_key_here
DATA_FOLDER=C:/temp/data
```

### Step 3: Create Data Folder
```bash
mkdir data
```

### Step 4: Start the Server (1 minute)
```bash
cd src
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 5: Test the API (1 minute)
Open browser to: `http://localhost:8000/docs`

## Common Workflows

### Workflow 1: Upload → Index → Search

```bash
# 1. Upload documents
curl -X POST "http://localhost:8000/upload" \
  -F "files=@myfile.pdf"

# 2. Create index
curl -X POST "http://localhost:8000/index" \
  -H "Content-Type: application/json" \
  -d '{"index_name":"my_docs","data_folder":"C:/temp/data"}'

# 3. Search
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"your search term","index_name":"my_docs"}'
```

### Workflow 2: Upload → Index → Ask Questions

```bash
# 1-2. Same as above...

# 3. Ask a question
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the document say about...?","index_name":"my_docs"}'
```

## Using Python Requests Library

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Upload
files = [("files", open("document.pdf", "rb"))]
r = requests.post(f"{BASE_URL}/upload", files=files)
print(r.json())

# 2. Index
r = requests.post(f"{BASE_URL}/index", json={
    "index_name": "my_docs",
    "data_folder": "C:/temp/data"
})
print(r.json())

# 3. Search
r = requests.post(f"{BASE_URL}/search", json={
    "query": "machine learning",
    "index_name": "my_docs",
    "top_k": 5
})
print(r.json())

# 4. Ask
r = requests.post(f"{BASE_URL}/ask", json={
    "question": "What is ML?",
    "index_name": "my_docs"
})
print(r.json())
```

## Docker Quick Start

```bash
# Build and run with docker-compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f tblr-api

# Stop
docker-compose down
```

## File Organization

```
tblr-gen/
├── src/
│   ├── main.py                 ← FastAPI app (start here)
│   └── api/
│       ├── document_manager.py
│       ├── index_manager.py
│       ├── search_engine.py
│       └── qa_engine.py
├── config/
│   └── application.properties  ← Add API keys here
├── requirements.txt            ← Dependencies
├── API_GUIDE.md               ← Full API documentation
├── DEVELOPMENT.md             ← Developer guide
├── Dockerfile                 ← Docker image
├── docker-compose.yml         ← Docker orchestration
└── test_api.py               ← Test script
```

## Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Service info |
| GET | `/health` | Health check |
| POST | `/upload` | Upload documents |
| POST | `/index` | Create index |
| POST | `/search` | Search documents |
| POST | `/ask` | Ask questions |

## Troubleshooting

**Q: "Connection refused" when running test**
- A: Make sure the server is running with `python main.py`

**Q: "Index not found" error**
- A: Create an index first using POST /index

**Q: "No documents found"**
- A: Upload documents first using POST /upload, or ensure DATA_FOLDER contains files

**Q: API key errors**
- A: Check `config/application.properties` has correct OPENAI_API_KEY

## Next Steps

1. Read `API_GUIDE.md` for detailed endpoint documentation
2. Check `DEVELOPMENT.md` for advanced configuration
3. Run `python test_api.py` to test all endpoints
4. Explore the Swagger UI at `http://localhost:8000/docs`

## Need Help?

- **API Documentation**: `API_GUIDE.md`
- **Development Guide**: `DEVELOPMENT.md`
- **Contact**: brij_joe@yahoo.com

---

**You're ready to go!** 🚀

Start with the **5-Minute Setup** above, then try one of the **Common Workflows**.

