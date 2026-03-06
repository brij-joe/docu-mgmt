# FastAPI Document Management Service

A FastAPI-based application for document management with semantic search and Q&A capabilities using LlamaIndex.

## Features

- **Upload Endpoint**: Upload documents to the system
- **Index Endpoint**: Create searchable document indexes
- **Search Endpoint**: Perform semantic search on indexed documents
- **Ask Endpoint**: Ask questions about indexed documents with AI-powered responses
- **Health Check**: Monitor service health

## Project Structure

```
tblr-gen/
├── src/
│   ├── main.py                 # FastAPI application and endpoints
│   ├── app_launcher.py         # Original launcher script
│   └── api/
│       ├── __init__.py
│       ├── document_manager.py # Document handling
│       ├── index_manager.py    # Index management
│       ├── search_engine.py    # Semantic search
│       └── qa_engine.py        # Q&A engine
├── config/
│   └── application.properties  # Configuration file
├── requirements.txt            # Python dependencies
└── indexes/                    # Stored indexes (created at runtime)
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure environment configuration is set in `config/application.properties`:
   - `DATA_FOLDER`: Path to document storage
   - `OPENAI_API_KEY`: OpenAI API key (for embeddings and Q&A)

## Running the Application

### Start the server:
```bash
cd src
python main.py
```

Or use uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Access API Documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### 1. Upload Documents
**Endpoint**: `POST /upload`

Upload one or more documents to the system.

**Parameters**:
- `files` (required): List of files to upload
- `folder` (optional): Destination folder (defaults to `DATA_FOLDER`)

**Example Request**:
```bash
curl -X POST "http://localhost:8000/upload" \
  -H "accept: application/json" \
  -F "files=@document1.pdf" \
  -F "files=@document2.txt"
```

**Response**:
```json
{
  "status": "success",
  "message": "Uploaded 2 file(s)",
  "files": [
    {
      "filename": "document1.pdf",
      "path": "C:/temp/data/document1.pdf",
      "size": 1024000
    },
    {
      "filename": "document2.txt",
      "path": "C:/temp/data/document2.txt",
      "size": 5120
    }
  ]
}
```

### 2. Create Index
**Endpoint**: `POST /index`

Create a searchable index from documents in a folder.

**Request Body**:
```json
{
  "index_name": "my_documents",
  "data_folder": "C:/temp/data"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/index" \
  -H "Content-Type: application/json" \
  -d '{
    "index_name": "my_documents",
    "data_folder": "C:/temp/data"
  }'
```

**Response**:
```json
{
  "status": "success",
  "message": "Index 'my_documents' created successfully",
  "index_name": "my_documents",
  "data_folder": "C:/temp/data"
}
```

### 3. Search Documents
**Endpoint**: `POST /search`

Perform semantic search on indexed documents.

**Request Body**:
```json
{
  "query": "search query",
  "index_name": "my_documents",
  "top_k": 5
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning applications",
    "index_name": "my_documents",
    "top_k": 5
  }'
```

**Response**:
```json
{
  "status": "success",
  "query": "machine learning applications",
  "index_name": "my_documents",
  "results_count": 2,
  "results": [
    {
      "rank": 1,
      "score": 0.95,
      "content": "Machine learning is used in various applications...",
      "metadata": {}
    },
    {
      "rank": 2,
      "score": 0.87,
      "content": "Deep learning applications in computer vision...",
      "metadata": {}
    }
  ]
}
```

### 4. Ask Questions
**Endpoint**: `POST /ask`

Ask questions about indexed documents and get AI-powered answers.

**Request Body**:
```json
{
  "question": "your question here",
  "index_name": "my_documents"
}
```

**Example Request**:
```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the key benefits of machine learning?",
    "index_name": "my_documents"
  }'
```

**Response**:
```json
{
  "status": "success",
  "question": "What are the key benefits of machine learning?",
  "index_name": "my_documents",
  "answer": "Based on the indexed documents, the key benefits of machine learning include... [AI-generated answer based on document content]"
}
```

### 5. Health Check
**Endpoint**: `GET /health`

Check service health and status.

**Example Request**:
```bash
curl http://localhost:8000/health
```

**Response**:
```json
{
  "status": "healthy",
  "service": "Document Management Service"
}
```

### 6. Root Endpoint
**Endpoint**: `GET /`

Get API information and available endpoints.

**Response**:
```json
{
  "service": "Document Management Service",
  "version": "1.0.0",
  "endpoints": {
    "upload": "POST /upload - Upload documents",
    "index": "POST /index - Create document index",
    "search": "POST /search - Search documents",
    "ask": "POST /ask - Ask questions about documents",
    "health": "GET /health - Health check"
  }
}
```

## Supported Document Formats

- `.pdf` - PDF files
- `.txt` - Text files
- `.docx` - Microsoft Word documents
- `.md` - Markdown files
- `.html` - HTML files
- `.json` - JSON files

## Configuration

Edit `config/application.properties`:

```properties
# API Keys
OPENAI_API_KEY=your_openai_api_key
HF_TOKEN=your_huggingface_token

# Data Configuration
DATA_FOLDER=C:/temp/data
```

## Usage Workflow

1. **Upload documents**:
   ```bash
   POST /upload
   ```

2. **Create index**:
   ```bash
   POST /index
   ```

3. **Search documents**:
   ```bash
   POST /search
   ```

4. **Ask questions**:
   ```bash
   POST /ask
   ```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request
- `500`: Server error

Error responses include detailed messages:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Development

To modify the API:

1. **Add new endpoints**: Edit `src/main.py`
2. **Modify search logic**: Edit `src/api/search_engine.py`
3. **Customize Q&A**: Edit `src/api/qa_engine.py`
4. **Update document handling**: Edit `src/api/document_manager.py`

## Performance Considerations

- Indexing large document sets may take time
- Search and Q&A operations use embeddings which require API calls
- Consider caching frequently searched queries
- Use appropriate `top_k` values for search to balance quality and speed

## Troubleshooting

**Issue**: "Index not found"
- Solution: Create the index first using the `/index` endpoint

**Issue**: "DATA_FOLDER not configured"
- Solution: Set `DATA_FOLDER` in `config/application.properties`

**Issue**: "No documents found in folder"
- Solution: Upload documents using `/upload` endpoint or ensure documents are in the specified folder

**Issue**: API key errors
- Solution: Verify `OPENAI_API_KEY` is set correctly in configuration

## Future Enhancements

- Multi-language support
- Advanced filtering options
- Document preprocessing pipeline
- Custom embedding models
- Real-time document indexing
- User authentication and authorization
- Rate limiting
- Caching layer for frequent queries

## License

Proof of Concept (PoC)

## Contact

For more details, contact: brij_joe@yahoo.com

