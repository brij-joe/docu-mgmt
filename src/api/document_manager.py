"""
Document management module for handling document uploads and organization
"""

import os
from typing import List, Dict, Any

from llama_index.core.readers import SimpleDirectoryReader


class DocumentManager:
    """Manages document upload and retrieval"""

    def __init__(self):
        self.supported_formats = [
            '.pdf', '.txt', '.docx', '.md', '.html', '.json'
        ]

    def validate_file(self, filename: str) -> bool:
        """
        Validate if file format is supported

        Args:
            filename: Name of the file to validate

        Returns:
            True if file format is supported
        """
        _, ext = os.path.splitext(filename)
        return ext.lower() in self.supported_formats

    def load_documents(self, folder_path: str) -> List[Any]:
        """
        Load documents from a folder using SimpleDirectoryReader

        Args:
            folder_path: Path to the folder containing documents

        Returns:
            List of loaded documents
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        try:
            reader = SimpleDirectoryReader(folder_path)
            documents = reader.load_data()
            return documents
        except Exception as e:
            raise Exception(f"Error loading documents: {str(e)}")

    def get_folder_info(self, folder_path: str) -> Dict[str, Any]:
        """
        Get information about documents in a folder

        Args:
            folder_path: Path to the folder

        Returns:
            Dictionary with folder information
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder not found: {folder_path}")

        files = []
        total_size = 0

        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                total_size += size
                files.append({
                    "name": filename,
                    "size": size,
                    "supported": self.validate_file(filename)
                })

        return {
            "folder": folder_path,
            "file_count": len(files),
            "total_size": total_size,
            "files": files
        }

