"""
FastAPI application for document management and retrieval using LlamaIndex
Provides endpoints for upload, indexing, searching, and asking questions.
"""

import os
from typing import Optional
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil
from dotenv import load_dotenv

from api.document_manager import DocumentManager
from api.index_manager import IndexManager
from api.search_engine import SearchEngine
from api.qa_engine import QAEngine

# Load environment variables
load_dotenv("../config/application.properties")

# Initialize FastAPI app
app = FastAPI(
    title="Document Management Service",
    description="API for document upload, indexing, searching, and Q&A",
    version="1.0.0"
)

# Initialize managers
doc_manager = DocumentManager()
index_manager = IndexManager()
search_engine = SearchEngine()
qa_engine = QAEngine()


# ============================= REQUEST MODELS =============================

class IndexRequest(BaseModel):
    """Request model for index creation"""
    index_name: str
    data_folder: Optional[str] = None


class SearchRequest(BaseModel):
    """Request model for search queries"""
    query: str
    index_name: Optional[str] = None
    top_k: int = 5


class AskRequest(BaseModel):
    """Request model for Q&A queries"""
    question: str
    index_name: Optional[str] = None


# ============================= ENDPOINTS =============================

@app.post("/upload")
async def upload_documents(
    files: list[UploadFile] = File(...),
    folder: Optional[str] = None
) -> JSONResponse:
    """
    Upload documents to the system.

    Args:
        files: List of files to upload
        folder: Optional destination folder (defaults to DATA_FOLDER from config)

    Returns:
        Success/failure status with uploaded file information
    """
    try:
        upload_folder = folder or os.environ.get('DATA_FOLDER', './data')
        os.makedirs(upload_folder, exist_ok=True)

        uploaded_files = []
        for file in files:
            if not file.filename:
                continue

            file_path = os.path.join(upload_folder, file.filename)

            # Save uploaded file
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            uploaded_files.append({
                "filename": file.filename,
                "path": file_path,
                "size": os.path.getsize(file_path)
            })

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"Uploaded {len(uploaded_files)} file(s)",
                "files": uploaded_files
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/index")
async def create_index(request: IndexRequest) -> JSONResponse:
    """
    Create or update a document index.

    Args:
        request: IndexRequest containing index_name and optional data_folder

    Returns:
        Index creation status and metadata
    """
    try:
        data_folder = request.data_folder or os.environ.get('DATA_FOLDER')

        if not data_folder:
            raise ValueError("DATA_FOLDER not configured")

        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"Data folder not found: {data_folder}")

        # Create index
        index = index_manager.create_index(
            index_name=request.index_name,
            data_folder=data_folder
        )

        # Store index for later use
        index_manager.save_index(request.index_name, index)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "message": f"Index '{request.index_name}' created successfully",
                "index_name": request.index_name,
                "data_folder": data_folder
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/search")
async def search_documents(request: SearchRequest) -> JSONResponse:
    """
    Search documents using the indexed data.

    Args:
        request: SearchRequest containing query, optional index_name and top_k

    Returns:
        Search results with matching documents and relevance scores
    """
    try:
        index_name = request.index_name or "default"

        # Load index
        index = index_manager.load_index(index_name)
        if index is None:
            raise ValueError(f"Index '{index_name}' not found. Create index first.")

        # Perform search
        results = search_engine.search(
            index=index,
            query=request.query,
            top_k=request.top_k
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "query": request.query,
                "index_name": index_name,
                "results_count": len(results),
                "results": results
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/ask")
async def ask_question(request: AskRequest) -> JSONResponse:
    """
    Ask a question about indexed documents using Q&A engine.

    Args:
        request: AskRequest containing question and optional index_name

    Returns:
        Answer generated from the indexed documents
    """
    try:
        index_name = request.index_name or "default"

        # Load index
        index = index_manager.load_index(index_name)
        if index is None:
            raise ValueError(f"Index '{index_name}' not found. Create index first.")

        # Generate answer
        answer = qa_engine.ask(
            index=index,
            question=request.question
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "question": request.question,
                "index_name": index_name,
                "answer": answer
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================= HEALTH CHECK =============================

@app.get("/health")
async def health_check() -> JSONResponse:
    """Check service health"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "Document Management Service"
        }
    )


# ============================= ROOT ENDPOINT =============================

@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint with API information"""
    return JSONResponse(
        status_code=200,
        content={
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
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

