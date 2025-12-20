"""
Qdrant vector store for semantic memory.

Provides semantic search and retrieval for conversations, code snippets, and documentation.
"""

from __future__ import annotations

from typing import Any, Sequence
from uuid import UUID

from qdrant_client import AsyncQdrantClient, models
from qdrant_client.models import Distance, PointStruct, VectorParams

from hivemind.config import get_settings


class VectorStore:
    """
    Qdrant-based vector store for semantic memory.

    Manages multiple collections for different content types and provides
    semantic search with metadata filtering.
    """

    def __init__(self, client: AsyncQdrantClient | None = None):
        """
        Initialize vector store.

        Args:
            client: Optional Qdrant client. If None, creates from config.
        """
        if client is None:
            settings = get_settings()
            client = AsyncQdrantClient(
                host=settings.qdrant.host,
                port=settings.qdrant.port,
                grpc_port=settings.qdrant.grpc_port,
                api_key=settings.qdrant.api_key.get_secret_value() if settings.qdrant.api_key else None,
                https=settings.qdrant.https,
            )
        self._client = client
        self._settings = get_settings()

    async def close(self) -> None:
        """Close the client connection."""
        await self._client.close()

    # =========================================================================
    # Collection Management
    # =========================================================================

    async def create_collection(
        self,
        name: str,
        vector_size: int | None = None,
        distance: Distance = Distance.COSINE,
    ) -> None:
        """
        Create a new collection.

        Args:
            name: Collection name
            vector_size: Vector dimension size. Defaults to config default.
            distance: Distance metric (COSINE, EUCLID, DOT)
        """
        if vector_size is None:
            vector_size = self._settings.qdrant.default_vector_size

        await self._client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=distance,
            ),
        )

    async def collection_exists(self, name: str) -> bool:
        """
        Check if a collection exists.

        Args:
            name: Collection name

        Returns:
            True if collection exists
        """
        collections = await self._client.get_collections()
        return any(col.name == name for col in collections.collections)

    async def delete_collection(self, name: str) -> None:
        """
        Delete a collection.

        Args:
            name: Collection name
        """
        await self._client.delete_collection(collection_name=name)

    async def ensure_collection(
        self,
        name: str,
        vector_size: int | None = None,
        distance: Distance = Distance.COSINE,
    ) -> None:
        """
        Ensure a collection exists, creating it if necessary.

        Args:
            name: Collection name
            vector_size: Vector dimension size
            distance: Distance metric
        """
        if not await self.collection_exists(name):
            await self.create_collection(name, vector_size, distance)

    async def initialize_default_collections(self) -> None:
        """
        Initialize default collections for HIVEMIND.

        Creates:
        - conversations: Semantic conversation search
        - code_snippets: Code example retrieval
        - documentation: Documentation search
        """
        await self.ensure_collection(
            self._settings.qdrant.conversations_collection,
        )
        await self.ensure_collection(
            self._settings.qdrant.code_snippets_collection,
        )
        await self.ensure_collection(
            self._settings.qdrant.documentation_collection,
        )

    # =========================================================================
    # Vector Operations
    # =========================================================================

    async def upsert(
        self,
        collection_name: str,
        id: str | UUID,
        vector: list[float],
        payload: dict[str, Any] | None = None,
    ) -> None:
        """
        Upsert a single vector with metadata.

        Args:
            collection_name: Collection name
            id: Point ID (converted to string)
            vector: Embedding vector
            payload: Optional metadata
        """
        point = PointStruct(
            id=str(id),
            vector=vector,
            payload=payload or {},
        )
        await self._client.upsert(
            collection_name=collection_name,
            points=[point],
        )

    async def upsert_batch(
        self,
        collection_name: str,
        points: list[tuple[str | UUID, list[float], dict[str, Any]]],
    ) -> None:
        """
        Upsert multiple vectors in batch.

        Args:
            collection_name: Collection name
            points: List of (id, vector, payload) tuples
        """
        point_structs = [
            PointStruct(
                id=str(point_id),
                vector=vector,
                payload=payload,
            )
            for point_id, vector, payload in points
        ]
        await self._client.upsert(
            collection_name=collection_name,
            points=point_structs,
        )

    async def get(
        self,
        collection_name: str,
        id: str | UUID,
    ) -> models.Record | None:
        """
        Get a point by ID.

        Args:
            collection_name: Collection name
            id: Point ID

        Returns:
            Point record or None if not found
        """
        results = await self._client.retrieve(
            collection_name=collection_name,
            ids=[str(id)],
        )
        return results[0] if results else None

    async def delete(
        self,
        collection_name: str,
        id: str | UUID,
    ) -> None:
        """
        Delete a point by ID.

        Args:
            collection_name: Collection name
            id: Point ID
        """
        await self._client.delete(
            collection_name=collection_name,
            points_selector=models.PointIdsList(
                points=[str(id)],
            ),
        )

    async def delete_batch(
        self,
        collection_name: str,
        ids: list[str | UUID],
    ) -> None:
        """
        Delete multiple points by ID.

        Args:
            collection_name: Collection name
            ids: List of point IDs
        """
        await self._client.delete(
            collection_name=collection_name,
            points_selector=models.PointIdsList(
                points=[str(id) for id in ids],
            ),
        )

    # =========================================================================
    # Search Operations
    # =========================================================================

    async def search(
        self,
        collection_name: str,
        query_vector: list[float],
        limit: int = 10,
        score_threshold: float | None = None,
        filter: models.Filter | None = None,
    ) -> list[models.ScoredPoint]:
        """
        Semantic search in a collection.

        Args:
            collection_name: Collection name
            query_vector: Query embedding vector
            limit: Maximum number of results
            score_threshold: Minimum similarity score
            filter: Optional metadata filter

        Returns:
            List of scored points
        """
        return await self._client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=filter,
        )

    async def search_with_payload_filter(
        self,
        collection_name: str,
        query_vector: list[float],
        filter_conditions: dict[str, Any],
        limit: int = 10,
        score_threshold: float | None = None,
    ) -> list[models.ScoredPoint]:
        """
        Semantic search with payload metadata filtering.

        Args:
            collection_name: Collection name
            query_vector: Query embedding vector
            filter_conditions: Dictionary of field->value filters
            limit: Maximum number of results
            score_threshold: Minimum similarity score

        Returns:
            List of scored points matching filters
        """
        # Build filter from conditions
        must_conditions = [
            models.FieldCondition(
                key=key,
                match=models.MatchValue(value=value),
            )
            for key, value in filter_conditions.items()
        ]

        filter = models.Filter(
            must=must_conditions,
        ) if must_conditions else None

        return await self.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            filter=filter,
        )

    # =========================================================================
    # Specialized Collection Methods
    # =========================================================================

    async def store_conversation(
        self,
        conversation_id: UUID,
        vector: list[float],
        session_id: UUID,
        message_count: int,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Store a conversation vector.

        Args:
            conversation_id: Conversation ID
            vector: Conversation embedding
            session_id: Parent session ID
            message_count: Number of messages
            metadata: Additional metadata
        """
        payload = {
            "conversation_id": str(conversation_id),
            "session_id": str(session_id),
            "message_count": message_count,
            **(metadata or {}),
        }
        await self.upsert(
            self._settings.qdrant.conversations_collection,
            conversation_id,
            vector,
            payload,
        )

    async def search_conversations(
        self,
        query_vector: list[float],
        session_id: UUID | None = None,
        limit: int = 10,
        score_threshold: float | None = None,
    ) -> list[models.ScoredPoint]:
        """
        Search for similar conversations.

        Args:
            query_vector: Query embedding
            session_id: Optional session ID filter
            limit: Maximum results
            score_threshold: Minimum similarity

        Returns:
            Similar conversations
        """
        filter_conditions = {}
        if session_id:
            filter_conditions["session_id"] = str(session_id)

        return await self.search_with_payload_filter(
            self._settings.qdrant.conversations_collection,
            query_vector,
            filter_conditions,
            limit,
            score_threshold,
        )

    async def store_code_snippet(
        self,
        snippet_id: str | UUID,
        vector: list[float],
        code: str,
        language: str,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Store a code snippet vector.

        Args:
            snippet_id: Snippet ID
            vector: Code embedding
            code: Source code
            language: Programming language
            metadata: Additional metadata
        """
        payload = {
            "code": code,
            "language": language,
            **(metadata or {}),
        }
        await self.upsert(
            self._settings.qdrant.code_snippets_collection,
            snippet_id,
            vector,
            payload,
        )

    async def search_code_snippets(
        self,
        query_vector: list[float],
        language: str | None = None,
        limit: int = 10,
        score_threshold: float | None = None,
    ) -> list[models.ScoredPoint]:
        """
        Search for similar code snippets.

        Args:
            query_vector: Query embedding
            language: Optional language filter
            limit: Maximum results
            score_threshold: Minimum similarity

        Returns:
            Similar code snippets
        """
        filter_conditions = {}
        if language:
            filter_conditions["language"] = language

        return await self.search_with_payload_filter(
            self._settings.qdrant.code_snippets_collection,
            query_vector,
            filter_conditions,
            limit,
            score_threshold,
        )

    async def store_documentation(
        self,
        doc_id: str | UUID,
        vector: list[float],
        content: str,
        title: str,
        category: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Store a documentation vector.

        Args:
            doc_id: Document ID
            vector: Document embedding
            content: Document content
            title: Document title
            category: Optional category
            metadata: Additional metadata
        """
        payload = {
            "content": content,
            "title": title,
            **({"category": category} if category else {}),
            **(metadata or {}),
        }
        await self.upsert(
            self._settings.qdrant.documentation_collection,
            doc_id,
            vector,
            payload,
        )

    async def search_documentation(
        self,
        query_vector: list[float],
        category: str | None = None,
        limit: int = 10,
        score_threshold: float | None = None,
    ) -> list[models.ScoredPoint]:
        """
        Search for relevant documentation.

        Args:
            query_vector: Query embedding
            category: Optional category filter
            limit: Maximum results
            score_threshold: Minimum similarity

        Returns:
            Relevant documentation
        """
        filter_conditions = {}
        if category:
            filter_conditions["category"] = category

        return await self.search_with_payload_filter(
            self._settings.qdrant.documentation_collection,
            query_vector,
            filter_conditions,
            limit,
            score_threshold,
        )
