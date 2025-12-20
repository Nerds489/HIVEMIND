"""
Authentication Middleware

FastAPI dependencies and decorators for JWT authentication and role-based access control.
"""

from __future__ import annotations

from enum import Enum
from functools import wraps
from typing import Any, Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from hivemind.observability import get_logger
from hivemind.security.auth import get_jwt_manager

logger = get_logger(__name__)


class UserRole(str, Enum):
    """User role enumeration."""
    ADMIN = "admin"
    USER = "user"
    SERVICE = "service"
    READONLY = "readonly"


class User:
    """
    Authenticated user representation.

    Extracted from JWT token claims.
    """

    def __init__(self, claims: dict[str, Any]):
        """
        Initialize user from JWT claims.

        Args:
            claims: JWT token claims
        """
        self.user_id: str = claims.get("sub", "")
        self.username: str = claims.get("username", "")
        self.email: str = claims.get("email", "")
        self.roles: list[str] = claims.get("roles", [])
        self.claims: dict[str, Any] = claims

    def has_role(self, role: str | UserRole) -> bool:
        """
        Check if user has a specific role.

        Args:
            role: Role to check

        Returns:
            True if user has the role
        """
        role_str = role.value if isinstance(role, UserRole) else role
        return role_str in self.roles

    def has_any_role(self, roles: list[str | UserRole]) -> bool:
        """
        Check if user has any of the specified roles.

        Args:
            roles: List of roles to check

        Returns:
            True if user has at least one role
        """
        return any(self.has_role(role) for role in roles)

    def has_all_roles(self, roles: list[str | UserRole]) -> bool:
        """
        Check if user has all of the specified roles.

        Args:
            roles: List of roles to check

        Returns:
            True if user has all roles
        """
        return all(self.has_role(role) for role in roles)

    def __repr__(self) -> str:
        """String representation."""
        return f"User(user_id={self.user_id}, username={self.username}, roles={self.roles})"


# HTTP Bearer token security scheme
security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    FastAPI dependency to get current authenticated user.

    Validates JWT token from Authorization header and returns User object.

    Args:
        credentials: HTTP bearer credentials from request

    Returns:
        Authenticated User object

    Raises:
        HTTPException: If token is invalid or expired

    Usage:
        @app.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user_id": user.user_id}
    """
    token = credentials.credentials

    try:
        jwt_manager = get_jwt_manager()
        claims = jwt_manager.verify_token(token, token_type="access")

        user = User(claims)

        logger.debug(
            f"User authenticated: {user.user_id}",
            extra={
                "user_id": user.user_id,
                "username": user.username,
            },
        )

        return user

    except JWTError as e:
        logger.warning(
            f"JWT validation failed: {e}",
            extra={"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except ValueError as e:
        logger.warning(
            f"Token validation failed: {e}",
            extra={"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(
            f"Authentication error: {e}",
            extra={"error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error",
        )


async def optional_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(optional_security),
) -> User | None:
    """
    FastAPI dependency for optional authentication.

    Returns User if valid token is provided, otherwise None.
    Does not raise exception if token is missing.

    Args:
        credentials: Optional HTTP bearer credentials

    Returns:
        User object if authenticated, None otherwise

    Usage:
        @app.get("/public")
        async def public_route(user: User | None = Depends(optional_auth)):
            if user:
                return {"message": f"Hello {user.username}"}
            return {"message": "Hello guest"}
    """
    if not credentials:
        return None

    try:
        jwt_manager = get_jwt_manager()
        claims = jwt_manager.verify_token(credentials.credentials, token_type="access")
        return User(claims)
    except (JWTError, ValueError):
        # Token provided but invalid - return None instead of raising
        logger.debug("Optional auth: invalid token provided")
        return None
    except Exception as e:
        logger.error(
            f"Optional auth error: {e}",
            extra={"error": str(e)},
        )
        return None


def require_role(
    *roles: str | UserRole,
    require_all: bool = False,
) -> Callable:
    """
    Decorator to require specific roles for endpoint access.

    Args:
        *roles: Required role(s)
        require_all: If True, user must have all roles. If False, any role is sufficient.

    Returns:
        Decorated function with role checking

    Raises:
        HTTPException: If user lacks required role(s)

    Usage:
        @app.get("/admin")
        @require_role(UserRole.ADMIN)
        async def admin_only(user: User = Depends(get_current_user)):
            return {"message": "Admin access granted"}

        @app.get("/elevated")
        @require_role(UserRole.ADMIN, UserRole.SERVICE)
        async def elevated_access(user: User = Depends(get_current_user)):
            return {"message": "Elevated access granted"}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Extract user from kwargs (injected by Depends)
            user: User | None = kwargs.get("user")

            if not user:
                # Check if user is in args (positional dependency)
                for arg in args:
                    if isinstance(arg, User):
                        user = arg
                        break

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )

            # Check roles
            role_check = user.has_all_roles(list(roles)) if require_all else user.has_any_role(list(roles))

            if not role_check:
                logger.warning(
                    f"Access denied for user {user.user_id}: insufficient roles",
                    extra={
                        "user_id": user.user_id,
                        "user_roles": user.roles,
                        "required_roles": [r.value if isinstance(r, UserRole) else r for r in roles],
                        "require_all": require_all,
                    },
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient privileges",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator


def get_user_id_from_token(token: str) -> str | None:
    """
    Extract user ID from token without full validation.

    Useful for rate limiting before full authentication.

    Args:
        token: JWT token

    Returns:
        User ID if extractable, None otherwise
    """
    try:
        jwt_manager = get_jwt_manager()
        return jwt_manager.get_token_subject(token)
    except Exception:
        return None
