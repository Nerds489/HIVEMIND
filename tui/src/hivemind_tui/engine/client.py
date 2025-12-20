"""
API Client for HIVEMIND TUI.

Provides async HTTP client for communicating with HIVEMIND backend.
"""

import asyncio
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

import httpx

from ..models.agents import Agent, AgentStatus


class APIClientError(Exception):
    """Base exception for API client errors."""

    pass


class ConnectionError(APIClientError):
    """Raised when connection to backend fails."""

    pass


class SessionError(APIClientError):
    """Raised when session operations fail."""

    pass


class APIClient:
    """Async HTTP client for HIVEMIND backend API."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        """Initialize API client.

        Args:
            base_url: Base URL for backend API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self._client: Optional[httpx.AsyncClient] = None
        self._session_id: Optional[str] = None

    async def __aenter__(self):
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Connect to the backend API."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(self.timeout),
                follow_redirects=True,
            )
            # Test connection
            try:
                await self.get_status()
            except Exception as e:
                await self.close()
                raise ConnectionError(f"Failed to connect to backend: {e}")

    async def close(self) -> None:
        """Close the API client connection."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return self._client is not None and not self._client.is_closed

    async def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs,
    ) -> httpx.Response:
        """Make an HTTP request with retry logic.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional request parameters

        Returns:
            HTTP response

        Raises:
            ConnectionError: If connection fails
            APIClientError: If request fails after retries
        """
        if not self.is_connected:
            await self.connect()

        url = f"{self.base_url}{endpoint}"
        last_error = None

        for attempt in range(self.max_retries):
            try:
                response = await self._client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code < 500:
                    # Client error, don't retry
                    raise APIClientError(f"API error: {e.response.status_code} - {e.response.text}")
            except httpx.RequestError as e:
                last_error = e
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue

        raise ConnectionError(f"Request failed after {self.max_retries} attempts: {last_error}")

    async def get_status(self) -> Dict[str, Any]:
        """Get backend status.

        Returns:
            Status information

        Raises:
            APIClientError: If request fails
        """
        response = await self._request("GET", "/v1/status")
        return response.json()

    async def create_session(self, metadata: Optional[Dict] = None) -> str:
        """Create a new session.

        Args:
            metadata: Optional session metadata

        Returns:
            Session ID

        Raises:
            SessionError: If session creation fails
        """
        try:
            payload = {"metadata": metadata or {}}
            response = await self._request("POST", "/v1/sessions", json=payload)
            data = response.json()
            self._session_id = data.get("session_id")
            if not self._session_id:
                raise SessionError("No session_id in response")
            return self._session_id
        except Exception as e:
            raise SessionError(f"Failed to create session: {e}")

    async def get_session(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Get session information.

        Args:
            session_id: Session ID (uses current session if not provided)

        Returns:
            Session information

        Raises:
            SessionError: If session retrieval fails
        """
        sid = session_id or self._session_id
        if not sid:
            raise SessionError("No active session")

        try:
            response = await self._request("GET", f"/v1/sessions/{sid}")
            return response.json()
        except Exception as e:
            raise SessionError(f"Failed to get session: {e}")

    async def send_completion(
        self,
        messages: List[Dict[str, str]],
        agent_id: Optional[str] = None,
        stream: bool = False,
        **kwargs,
    ) -> Dict[str, Any]:
        """Send a completion request.

        Args:
            messages: List of message dictionaries
            agent_id: Optional agent ID to use
            stream: Whether to stream response (not used in sync mode)
            **kwargs: Additional completion parameters

        Returns:
            Completion response

        Raises:
            APIClientError: If request fails
        """
        if not self._session_id:
            await self.create_session()

        payload = {
            "messages": messages,
            "session_id": self._session_id,
            "stream": False,  # Sync mode for this method
            **kwargs,
        }

        if agent_id:
            payload["agent_id"] = agent_id

        try:
            response = await self._request("POST", "/v1/completions", json=payload)
            return response.json()
        except Exception as e:
            raise APIClientError(f"Completion request failed: {e}")

    async def get_agents(self) -> List[Agent]:
        """Get list of available agents.

        Returns:
            List of Agent objects

        Raises:
            APIClientError: If request fails
        """
        try:
            response = await self._request("GET", "/v1/agents")
            data = response.json()
            agents = []
            for agent_data in data.get("agents", []):
                try:
                    agent = Agent.from_dict(agent_data)
                    agents.append(agent)
                except Exception as e:
                    # Skip invalid agent data
                    continue
            return agents
        except Exception as e:
            raise APIClientError(f"Failed to get agents: {e}")

    async def get_agent(self, agent_id: str) -> Agent:
        """Get a specific agent.

        Args:
            agent_id: Agent ID

        Returns:
            Agent object

        Raises:
            APIClientError: If request fails
        """
        try:
            response = await self._request("GET", f"/v1/agents/{agent_id}")
            data = response.json()
            return Agent.from_dict(data)
        except Exception as e:
            raise APIClientError(f"Failed to get agent: {e}")

    async def update_agent_status(self, agent_id: str, status: AgentStatus) -> None:
        """Update agent status.

        Args:
            agent_id: Agent ID
            status: New status

        Raises:
            APIClientError: If request fails
        """
        try:
            payload = {"status": status.value}
            await self._request("PATCH", f"/v1/agents/{agent_id}", json=payload)
        except Exception as e:
            raise APIClientError(f"Failed to update agent status: {e}")

    @property
    def session_id(self) -> Optional[str]:
        """Get current session ID."""
        return self._session_id

    @session_id.setter
    def session_id(self, value: Optional[str]) -> None:
        """Set session ID."""
        self._session_id = value
