"""
JWT Authentication

Token creation and validation using python-jose for secure authentication.
Supports access and refresh tokens with configurable expiration.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from hivemind.config import get_settings
from hivemind.observability import get_logger

logger = get_logger(__name__)


class JWTManager:
    """
    JWT token manager for authentication.

    Handles creation and validation of JWT access and refresh tokens.
    """

    def __init__(self):
        """Initialize JWT manager with configuration."""
        self.settings = get_settings()
        self.security = self.settings.security

        self.secret_key = self.security.jwt_secret_key.get_secret_value()
        self.algorithm = self.security.jwt_algorithm
        self.access_token_expire = timedelta(
            minutes=self.security.jwt_access_token_expire_minutes
        )
        self.refresh_token_expire = timedelta(
            days=self.security.jwt_refresh_token_expire_days
        )

    def create_access_token(
        self,
        subject: str,
        additional_claims: dict[str, Any] | None = None,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Create JWT access token.

        Args:
            subject: Token subject (typically user ID)
            additional_claims: Extra claims to include in token
            expires_delta: Custom expiration time

        Returns:
            Encoded JWT token
        """
        expires = expires_delta or self.access_token_expire
        expire_time = datetime.now(timezone.utc) + expires

        claims = {
            "sub": subject,
            "exp": expire_time,
            "iat": datetime.now(timezone.utc),
            "type": "access",
        }

        if additional_claims:
            claims.update(additional_claims)

        try:
            token = jwt.encode(claims, self.secret_key, algorithm=self.algorithm)

            logger.debug(
                f"Access token created for subject '{subject}'",
                extra={
                    "subject": subject,
                    "expires_at": expire_time.isoformat(),
                },
            )

            return token

        except Exception as e:
            logger.error(
                f"Failed to create access token: {e}",
                extra={"subject": subject, "error": str(e)},
            )
            raise

    def create_refresh_token(
        self,
        subject: str,
        additional_claims: dict[str, Any] | None = None,
        expires_delta: timedelta | None = None,
    ) -> str:
        """
        Create JWT refresh token.

        Args:
            subject: Token subject (typically user ID)
            additional_claims: Extra claims to include in token
            expires_delta: Custom expiration time

        Returns:
            Encoded JWT token
        """
        expires = expires_delta or self.refresh_token_expire
        expire_time = datetime.now(timezone.utc) + expires

        claims = {
            "sub": subject,
            "exp": expire_time,
            "iat": datetime.now(timezone.utc),
            "type": "refresh",
        }

        if additional_claims:
            claims.update(additional_claims)

        try:
            token = jwt.encode(claims, self.secret_key, algorithm=self.algorithm)

            logger.debug(
                f"Refresh token created for subject '{subject}'",
                extra={
                    "subject": subject,
                    "expires_at": expire_time.isoformat(),
                },
            )

            return token

        except Exception as e:
            logger.error(
                f"Failed to create refresh token: {e}",
                extra={"subject": subject, "error": str(e)},
            )
            raise

    def decode_token(self, token: str) -> dict[str, Any]:
        """
        Decode JWT token without validation.

        Args:
            token: JWT token to decode

        Returns:
            Token claims

        Raises:
            JWTError: If token is malformed
        """
        try:
            claims = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options={"verify_signature": False},
            )
            return claims

        except JWTError as e:
            logger.warning(
                f"Failed to decode token: {e}",
                extra={"error": str(e)},
            )
            raise

    def verify_token(self, token: str, token_type: str = "access") -> dict[str, Any]:
        """
        Verify and decode JWT token.

        Args:
            token: JWT token to verify
            token_type: Expected token type ("access" or "refresh")

        Returns:
            Token claims if valid

        Raises:
            JWTError: If token is invalid or expired
            ValueError: If token type doesn't match
        """
        try:
            claims = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            # Verify token type
            if claims.get("type") != token_type:
                raise ValueError(
                    f"Invalid token type. Expected '{token_type}', got '{claims.get('type')}'"
                )

            logger.debug(
                f"Token verified for subject '{claims.get('sub')}'",
                extra={
                    "subject": claims.get("sub"),
                    "token_type": token_type,
                },
            )

            return claims

        except JWTError as e:
            logger.warning(
                f"Token verification failed: {e}",
                extra={"error": str(e), "token_type": token_type},
            )
            raise

    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Create new access token from refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            New access token

        Raises:
            JWTError: If refresh token is invalid
        """
        claims = self.verify_token(refresh_token, token_type="refresh")
        subject = claims.get("sub")

        if not subject:
            raise ValueError("Token missing subject claim")

        # Create new access token with same subject
        return self.create_access_token(subject)

    def get_token_subject(self, token: str) -> str | None:
        """
        Extract subject from token without full validation.

        Args:
            token: JWT token

        Returns:
            Token subject or None if not found
        """
        try:
            claims = self.decode_token(token)
            return claims.get("sub")
        except JWTError:
            return None

    def is_token_expired(self, token: str) -> bool:
        """
        Check if token is expired.

        Args:
            token: JWT token

        Returns:
            True if token is expired
        """
        try:
            claims = self.decode_token(token)
            exp = claims.get("exp")

            if not exp:
                return True

            expiry = datetime.fromtimestamp(exp, tz=timezone.utc)
            return datetime.now(timezone.utc) > expiry

        except JWTError:
            return True


# Global JWT manager instance
_jwt_manager: JWTManager | None = None


def get_jwt_manager() -> JWTManager:
    """
    Get or create global JWT manager instance.

    Returns:
        JWT manager instance
    """
    global _jwt_manager

    if _jwt_manager is None:
        _jwt_manager = JWTManager()

    return _jwt_manager


# Convenience functions
def create_access_token(
    subject: str,
    additional_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create JWT access token (convenience function).

    Args:
        subject: Token subject (typically user ID)
        additional_claims: Extra claims to include in token
        expires_delta: Custom expiration time

    Returns:
        Encoded JWT token
    """
    manager = get_jwt_manager()
    return manager.create_access_token(subject, additional_claims, expires_delta)


def create_refresh_token(
    subject: str,
    additional_claims: dict[str, Any] | None = None,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create JWT refresh token (convenience function).

    Args:
        subject: Token subject (typically user ID)
        additional_claims: Extra claims to include in token
        expires_delta: Custom expiration time

    Returns:
        Encoded JWT token
    """
    manager = get_jwt_manager()
    return manager.create_refresh_token(subject, additional_claims, expires_delta)


def verify_token(token: str, token_type: str = "access") -> dict[str, Any]:
    """
    Verify and decode JWT token (convenience function).

    Args:
        token: JWT token to verify
        token_type: Expected token type ("access" or "refresh")

    Returns:
        Token claims if valid

    Raises:
        JWTError: If token is invalid or expired
    """
    manager = get_jwt_manager()
    return manager.verify_token(token, token_type)


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode JWT token without validation (convenience function).

    Args:
        token: JWT token to decode

    Returns:
        Token claims

    Raises:
        JWTError: If token is malformed
    """
    manager = get_jwt_manager()
    return manager.decode_token(token)
