# Development Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Edit `config/application.properties`:
```properties
OPENAI_API_KEY=your_key_here
DATA_FOLDER=C:/temp/data
```

### 3. Run the Application

```bash
cd src
python main.py
```

The API will be available at `http://localhost:8000`

## Project Architecture

### Directory Structure

```
src/
├── main.py                  # FastAPI application
└── api/
    ├── document_manager.py  # Document handling & validation
    ├── index_manager.py     # Index creation & persistence
    ├── search_engine.py     # Semantic search implementation
    └── qa_engine.py         # Question answering engine
```

### Component Overview

#### 1. **DocumentManager** (`api/document_manager.py`)
- Handles document uploads and validation
- Supports multiple file formats (.pdf, .txt, .docx, .md, .html, .json)
- Provides folder information and document statistics

#### 2. **IndexManager** (`api/index_manager.py`)
- Creates VectorStoreIndex from documents
- Manages index persistence (in-memory and disk)
- Supports index lifecycle (create, load, save, delete)
- Pickle-based serialization for index storage

#### 3. **SearchEngine** (`api/search_engine.py`)
- Performs semantic similarity search
- Retrieves top-k relevant documents
- Supports batch queries
- Returns ranked results with scores and metadata

#### 4. **QAEngine** (`api/qa_engine.py`)
- Generates answers using LlamaIndex query engine
- Supports context-aware Q&A
- Provides supporting documents with answers
- Handles multi-turn conversations

### API Endpoints

```
GET  /                    # Service info
GET  /health             # Health check
POST /upload             # Upload documents
POST /index              # Create index
POST /search             # Search documents
POST /ask                # Ask questions
```

## Development Workflow

### Adding a New Endpoint

1. Create a request model in `main.py`:
```python
class MyRequest(BaseModel):
    param1: str
    param2: int = 5
```

2. Add endpoint handler:
```python
@app.post("/my-endpoint")
async def my_endpoint(request: MyRequest) -> JSONResponse:
    try:
        # Your logic here
        result = do_something(request.param1)
        return JSONResponse(status_code=200, content={"result": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Modifying Search Logic

Edit `api/search_engine.py`:
```python
def search(self, index, query, top_k=5):
    # Customize retriever settings
    retriever = index.as_retriever(similarity_top_k=top_k)
    # Modify result formatting
    nodes = retriever.retrieve(query)
    # Process results
    return formatted_results
```

### Customizing Q&A Engine

Edit `api/qa_engine.py`:
```python
def ask(self, index, question):
    # Use different query engines
    query_engine = index.as_query_engine(
        response_mode="tree_summarize",  # or other modes
        streaming=True  # Enable streaming
    )
    response = query_engine.query(question)
    return str(response)
```

## Testing

### Run Test Suite

```bash
python test_api.py
```

### Manual Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Upload documents
curl -X POST "http://localhost:8000/upload" \
  -F "files=@document.pdf"

# Create index
curl -X POST "http://localhost:8000/index" \
  -H "Content-Type: application/json" \
  -d '{"index_name":"test","data_folder":"C:/temp/data"}'

# Search
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"machine learning","index_name":"test"}'

# Ask
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question":"What is ML?","index_name":"test"}'
```

### Interactive Testing

Use the Swagger UI at `http://localhost:8000/docs` to test endpoints interactively.

## Docker Deployment

### Build Docker Image

```bash
docker build -t tblr-api:latest .
```

### Run with Docker Compose

```bash
docker-compose up -d
```

### Run Docker Container

```bash
docker run -p 8000:8000 \
  -e DATA_FOLDER=/app/data \
  -v ./data:/app/data \
  -v ./indexes:/app/indexes \
  tblr-api:latest
```

## Performance Optimization

### 1. Index Caching
- Indexes are cached in memory after first load
- Use IndexManager.load_index() for faster subsequent access

### 2. Batch Requests
- Use batch search for multiple queries
- Reduce API calls by combining operations

### 3. Top-K Optimization
- Adjust `top_k` parameter based on use case
- Balance between accuracy and speed

### 4. Document Preprocessing
- Consider implementing document chunking
- Remove duplicates and clean data before indexing

## Troubleshooting

### Common Issues

**Issue**: Import errors
```
ModuleNotFoundError: No module named 'llama_index'
```
**Solution**: Install dependencies with `pip install -r requirements.txt`

**Issue**: API returns empty results
```
"results_count": 0
```
**Solution**: 
1. Verify documents are uploaded
2. Check index is created
3. Ensure data folder path is correct

**Issue**: "Index not found"
**Solution**: Create index first using POST /index

**Issue**: Authentication errors
**Solution**: Verify API keys in `config/application.properties`

### Debug Mode

Run with uvicorn debug:
```bash
uvicorn src.main:app --reload --log-level debug
```

View logs in console for detailed error information.

## Code Style

### Python Standards
- Use type hints for all functions
- Follow PEP 8 naming conventions
- Use docstrings for all classes and functions
- Keep functions focused and modular

### Example Function

```python
def search(
    self,
    index: VectorStoreIndex,
    query: str,
    top_k: int = 5
) -> List[Dict[str, Any]]:
    """
    Search documents using semantic similarity.
    
    Args:
        index: VectorStoreIndex to search on
        query: Search query string
        top_k: Number of top results to return
        
    Returns:
        List of search results with scores and content
    """
    # Implementation here
    pass
```

## Dependencies

### Core
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **llama-index**: Document indexing and search
- **pydantic**: Data validation

### Utilities
- **python-dotenv**: Environment variable management
- **python-multipart**: File upload handling

### Optional
- **openai**: For embeddings and LLM
- **anthropic**: Alternative LLM provider
- **google-generativeai**: Google Gemini support

## Deployment Checklist

- [ ] Install dependencies
- [ ] Configure environment variables
- [ ] Create data folder
- [ ] Test all endpoints
- [ ] Review error handling
- [ ] Set up logging
- [ ] Configure Docker (if using containers)
- [ ] Set resource limits
- [ ] Plan backup strategy for indexes
- [ ] Document API usage

## Future Enhancements

1. **Authentication**: Add JWT-based auth
2. **Rate Limiting**: Implement request throttling
3. **Caching**: Add Redis for query caching
4. **Monitoring**: Add Prometheus metrics
5. **Logging**: Implement structured logging
6. **Database**: Add PostgreSQL for metadata
7. **Webhooks**: Event notifications
8. **Async**: Full async/await support
9. **Streaming**: Real-time response streaming
10. **Multi-tenancy**: Support multiple users/indexes

## Support

For issues or questions, contact: brij_joe@yahoo.com

