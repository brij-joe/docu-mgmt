"""
Search engine module for searching documents using semantic similarity
"""

from typing import List, Dict, Any
from llama_index.core import VectorStoreIndex


class SearchEngine:
    """Handles semantic search on indexed documents"""

    def search(
        self,
        index: VectorStoreIndex,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search documents using semantic similarity

        Args:
            index: VectorStoreIndex to search on
            query: Search query
            top_k: Number of top results to return

        Returns:
            List of search results with scores and content
        """
        try:
            # Create a retriever from the index
            retriever = index.as_retriever(similarity_top_k=top_k)

            # Retrieve matching nodes
            nodes = retriever.retrieve(query)

            # Format results
            results = []
            for i, node in enumerate(nodes):
                result = {
                    "rank": i + 1,
                    "score": node.score if hasattr(node, 'score') else None,
                    "content": node.get_content(),
                    "metadata": node.metadata if hasattr(node, 'metadata') else {}
                }
                results.append(result)

            return results

        except Exception as e:
            raise Exception(f"Error during search: {str(e)}")

    def multi_field_search(
        self,
        index: VectorStoreIndex,
        queries: List[str],
        top_k: int = 5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Perform multiple searches at once

        Args:
            index: VectorStoreIndex to search on
            queries: List of search queries
            top_k: Number of top results per query

        Returns:
            Dictionary mapping queries to their results
        """
        results = {}
        for query in queries:
            results[query] = self.search(index, query, top_k)

        return results

    def get_similar_documents(
        self,
        index: VectorStoreIndex,
        document_id: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find documents similar to a given document

        Args:
            index: VectorStoreIndex to search on
            document_id: ID of the reference document
            top_k: Number of similar documents to return

        Returns:
            List of similar documents
        """
        try:
            # Get the document content
            retriever = index.as_retriever(similarity_top_k=top_k + 1)

            # This is a simplified implementation
            # In a real scenario, you'd query the document by ID first
            results = []
            return results

        except Exception as e:
            raise Exception(f"Error finding similar documents: {str(e)}")

