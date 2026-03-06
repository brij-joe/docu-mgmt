"""
Q&A engine module for answering questions about indexed documents
"""

from typing import Dict, Any
from llama_index.core import VectorStoreIndex


class QAEngine:
    """Handles question answering using indexed documents"""

    def ask(
        self,
        index: VectorStoreIndex,
        question: str
    ) -> str:
        """
        Answer a question using the indexed documents

        Args:
            index: VectorStoreIndex to query
            question: Question to answer

        Returns:
            Generated answer as a string
        """
        try:
            # Create a query engine from the index
            query_engine = index.as_query_engine()

            # Query the engine
            response = query_engine.query(question)

            # Extract answer text
            answer = str(response)

            return answer

        except Exception as e:
            raise Exception(f"Error generating answer: {str(e)}")

    def ask_with_context(
        self,
        index: VectorStoreIndex,
        question: str,
        context_size: int = 5
    ) -> Dict[str, Any]:
        """
        Answer a question and return supporting context

        Args:
            index: VectorStoreIndex to query
            question: Question to answer
            context_size: Number of supporting documents to return

        Returns:
            Dictionary with answer and supporting context
        """
        try:
            # Get the answer
            answer = self.ask(index, question)

            # Get supporting documents
            retriever = index.as_retriever(similarity_top_k=context_size)
            nodes = retriever.retrieve(question)

            # Format context
            context = []
            for node in nodes:
                context.append({
                    "content": node.get_content(),
                    "metadata": node.metadata if hasattr(node, 'metadata') else {}
                })

            return {
                "question": question,
                "answer": answer,
                "context_count": len(context),
                "supporting_documents": context
            }

        except Exception as e:
            raise Exception(f"Error generating answer with context: {str(e)}")

    def conversational_ask(
        self,
        index: VectorStoreIndex,
        question: str,
        chat_history: list = None
    ) -> str:
        """
        Answer a question in a conversational context

        Args:
            index: VectorStoreIndex to query
            question: Current question to answer
            chat_history: Previous conversation messages

        Returns:
            Generated answer as a string
        """
        try:
            # For now, treat it like a regular ask
            # In a production system, you'd use a chat engine
            # and incorporate the chat history

            if chat_history is None:
                chat_history = []

            # Create query with context from chat history
            context_str = self._format_chat_context(chat_history)
            full_question = f"{context_str}\nCurrent question: {question}".strip()

            # Get answer
            query_engine = index.as_query_engine()
            response = query_engine.query(full_question)

            return str(response)

        except Exception as e:
            raise Exception(f"Error in conversational ask: {str(e)}")

    def _format_chat_context(self, chat_history: list) -> str:
        """
        Format chat history for context

        Args:
            chat_history: List of previous messages

        Returns:
            Formatted context string
        """
        if not chat_history:
            return ""

        context = "Previous context:\n"
        for msg in chat_history[-3:]:  # Use last 3 messages
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "")
            context += f"{role}: {content}\n"

        return context

