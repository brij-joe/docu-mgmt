"""
Index management module for creating and managing document indexes
"""

import os
import pickle
from typing import Dict, Any, Optional

from llama_index.core.indices import VectorStoreIndex
from llama_index.core.readers import SimpleDirectoryReader


class IndexManager:
    """Manages document indexing and index persistence"""

    def __init__(self, index_storage_path: str = "./indexes"):
        self.index_storage_path = index_storage_path
        self.indexes: Dict[str, Any] = {}
        os.makedirs(index_storage_path, exist_ok=True)

    def create_index(self, index_name: str, data_folder: str) -> VectorStoreIndex:
        """
        Create a VectorStoreIndex from documents in a folder

        Args:
            index_name: Name for the index
            data_folder: Path to folder containing documents

        Returns:
            Created VectorStoreIndex
        """
        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"Data folder not found: {data_folder}")

        try:
            # Load documents from folder
            documents = SimpleDirectoryReader(data_folder).load_data()

            if not documents:
                raise ValueError(f"No documents found in {data_folder}")

            # Create index from documents
            index = VectorStoreIndex.from_documents(documents)

            # Store in memory
            self.indexes[index_name] = index

            print(f"Index '{index_name}' created with {len(documents)} documents")
            return index

        except Exception as e:
            raise Exception(f"Error creating index: {str(e)}")

    def save_index(self, index_name: str, index: VectorStoreIndex) -> None:
        """
        Save index to disk using pickle

        Args:
            index_name: Name of the index
            index: VectorStoreIndex to save
        """
        try:
            index_path = os.path.join(self.index_storage_path, f"{index_name}.pkl")
            with open(index_path, "wb") as f:
                pickle.dump(index, f)
            print(f"Index '{index_name}' saved to {index_path}")
        except Exception as e:
            raise Exception(f"Error saving index: {str(e)}")

    def load_index(self, index_name: str) -> Optional[VectorStoreIndex]:
        """
        Load index from disk or memory

        Args:
            index_name: Name of the index to load

        Returns:
            VectorStoreIndex or None if not found
        """
        # Check memory first
        if index_name in self.indexes:
            return self.indexes[index_name]

        # Try to load from disk
        try:
            index_path = os.path.join(self.index_storage_path, f"{index_name}.pkl")
            if os.path.exists(index_path):
                with open(index_path, "rb") as f:
                    index = pickle.load(f)
                self.indexes[index_name] = index
                print(f"Index '{index_name}' loaded from disk")
                return index
        except Exception as e:
            print(f"Error loading index from disk: {str(e)}")

        return None

    def list_indexes(self) -> Dict[str, Any]:
        """
        List all available indexes

        Returns:
            Dictionary with index information
        """
        indexes = {
            "in_memory": list(self.indexes.keys()),
            "on_disk": []
        }

        if os.path.exists(self.index_storage_path):
            for filename in os.listdir(self.index_storage_path):
                if filename.endswith(".pkl"):
                    index_name = filename[:-4]  # Remove .pkl extension
                    indexes["on_disk"].append(index_name)

        return indexes

    def delete_index(self, index_name: str) -> bool:
        """
        Delete an index from memory and disk

        Args:
            index_name: Name of the index to delete

        Returns:
            True if deleted successfully
        """
        # Remove from memory
        if index_name in self.indexes:
            del self.indexes[index_name]

        # Remove from disk
        try:
            index_path = os.path.join(self.index_storage_path, f"{index_name}.pkl")
            if os.path.exists(index_path):
                os.remove(index_path)
                print(f"Index '{index_name}' deleted")
                return True
        except Exception as e:
            print(f"Error deleting index: {str(e)}")

        return False

