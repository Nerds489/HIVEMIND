"""
Input Validation and Sanitization

Provides utilities for validating and sanitizing user input to prevent
injection attacks and ensure data integrity.
"""

from __future__ import annotations

import html
import json
import re
from typing import Any
from urllib.parse import urlparse

import bleach

from hivemind.observability import get_logger

logger = get_logger(__name__)


class ValidationError(Exception):
    """Raised when input validation fails."""

    pass


# Regular expressions for validation
EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

# Allowed HTML tags for sanitization (very restrictive)
ALLOWED_TAGS = [
    "p", "br", "strong", "em", "u", "a", "ul", "ol", "li",
    "h1", "h2", "h3", "h4", "h5", "h6", "code", "pre", "blockquote",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["src", "alt"],
}


def sanitize_input(
    value: str,
    max_length: int | None = None,
    allow_empty: bool = True,
    strip: bool = True,
) -> str:
    """
    Sanitize string input by removing dangerous characters.

    Args:
        value: Input string to sanitize
        max_length: Maximum allowed length
        allow_empty: Whether to allow empty strings
        strip: Whether to strip whitespace

    Returns:
        Sanitized string

    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}")

    # Strip whitespace if requested
    if strip:
        value = value.strip()

    # Check if empty
    if not value and not allow_empty:
        raise ValidationError("Input cannot be empty")

    # Check length
    if max_length is not None and len(value) > max_length:
        raise ValidationError(
            f"Input exceeds maximum length of {max_length} characters"
        )

    # Escape HTML entities to prevent XSS
    sanitized = html.escape(value)

    # Remove null bytes
    sanitized = sanitized.replace("\x00", "")

    # Remove other control characters (except newlines and tabs)
    sanitized = "".join(
        char for char in sanitized
        if char >= " " or char in "\n\t\r"
    )

    logger.debug(
        "Input sanitized",
        extra={
            "original_length": len(value),
            "sanitized_length": len(sanitized),
        },
    )

    return sanitized


def sanitize_html(
    value: str,
    allowed_tags: list[str] | None = None,
    allowed_attributes: dict[str, list[str]] | None = None,
    strip: bool = True,
) -> str:
    """
    Sanitize HTML content using bleach.

    Args:
        value: HTML string to sanitize
        allowed_tags: List of allowed HTML tags
        allowed_attributes: Dict of allowed attributes per tag
        strip: Whether to strip disallowed tags

    Returns:
        Sanitized HTML string

    Raises:
        ValidationError: If validation fails
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}")

    tags = allowed_tags or ALLOWED_TAGS
    attrs = allowed_attributes or ALLOWED_ATTRIBUTES

    # Clean HTML with bleach
    sanitized = bleach.clean(
        value,
        tags=tags,
        attributes=attrs,
        strip=strip,
    )

    # Also linkify URLs
    sanitized = bleach.linkify(sanitized)

    logger.debug(
        "HTML sanitized",
        extra={
            "original_length": len(value),
            "sanitized_length": len(sanitized),
        },
    )

    return sanitized


def validate_email(email: str) -> str:
    """
    Validate and sanitize email address.

    Args:
        email: Email address to validate

    Returns:
        Validated email address (lowercase)

    Raises:
        ValidationError: If email is invalid
    """
    if not isinstance(email, str):
        raise ValidationError(f"Expected string, got {type(email).__name__}")

    email = email.strip().lower()

    # Check format
    if not EMAIL_REGEX.match(email):
        raise ValidationError(f"Invalid email format: {email}")

    # Check length constraints
    if len(email) > 254:  # RFC 5321
        raise ValidationError("Email address is too long")

    local, domain = email.rsplit("@", 1)

    if len(local) > 64:  # RFC 5321
        raise ValidationError("Email local part is too long")

    if len(domain) > 253:  # RFC 1035
        raise ValidationError("Email domain is too long")

    logger.debug(
        "Email validated",
        extra={"email": email},
    )

    return email


def validate_url(
    url: str,
    allowed_schemes: list[str] | None = None,
    allow_localhost: bool = False,
) -> str:
    """
    Validate URL format and scheme.

    Args:
        url: URL to validate
        allowed_schemes: List of allowed schemes (default: http, https)
        allow_localhost: Whether to allow localhost URLs

    Returns:
        Validated URL

    Raises:
        ValidationError: If URL is invalid
    """
    if not isinstance(url, str):
        raise ValidationError(f"Expected string, got {type(url).__name__}")

    url = url.strip()

    if not url:
        raise ValidationError("URL cannot be empty")

    schemes = allowed_schemes or ["http", "https"]

    try:
        parsed = urlparse(url)

        # Check scheme
        if parsed.scheme not in schemes:
            raise ValidationError(
                f"URL scheme '{parsed.scheme}' not allowed. Must be one of: {schemes}"
            )

        # Check netloc exists
        if not parsed.netloc:
            raise ValidationError("URL must have a valid domain")

        # Check for localhost if not allowed
        if not allow_localhost:
            if parsed.netloc.lower() in ["localhost", "127.0.0.1", "::1"]:
                raise ValidationError("Localhost URLs are not allowed")

        logger.debug(
            "URL validated",
            extra={"url": url, "scheme": parsed.scheme},
        )

        return url

    except ValueError as e:
        raise ValidationError(f"Invalid URL format: {e}")


def validate_json(
    value: str,
    max_size: int | None = None,
) -> dict[str, Any] | list[Any]:
    """
    Validate and parse JSON string.

    Args:
        value: JSON string to validate
        max_size: Maximum allowed size in bytes

    Returns:
        Parsed JSON object

    Raises:
        ValidationError: If JSON is invalid
    """
    if not isinstance(value, str):
        raise ValidationError(f"Expected string, got {type(value).__name__}")

    # Check size
    if max_size is not None and len(value.encode("utf-8")) > max_size:
        raise ValidationError(
            f"JSON exceeds maximum size of {max_size} bytes"
        )

    try:
        parsed = json.loads(value)

        logger.debug(
            "JSON validated",
            extra={"size_bytes": len(value.encode("utf-8"))},
        )

        return parsed

    except json.JSONDecodeError as e:
        raise ValidationError(f"Invalid JSON: {e}")


def validate_username(
    username: str,
    min_length: int = 3,
    max_length: int = 32,
    allow_special_chars: bool = False,
) -> str:
    """
    Validate username format.

    Args:
        username: Username to validate
        min_length: Minimum length
        max_length: Maximum length
        allow_special_chars: Whether to allow special characters

    Returns:
        Validated username

    Raises:
        ValidationError: If username is invalid
    """
    if not isinstance(username, str):
        raise ValidationError(f"Expected string, got {type(username).__name__}")

    username = username.strip()

    # Check length
    if len(username) < min_length:
        raise ValidationError(
            f"Username must be at least {min_length} characters"
        )

    if len(username) > max_length:
        raise ValidationError(
            f"Username must be at most {max_length} characters"
        )

    # Check characters
    if allow_special_chars:
        # Allow alphanumeric, underscore, hyphen, dot
        pattern = r"^[a-zA-Z0-9._-]+$"
    else:
        # Only alphanumeric and underscore
        pattern = r"^[a-zA-Z0-9_]+$"

    if not re.match(pattern, username):
        raise ValidationError(
            "Username contains invalid characters"
        )

    # Cannot start or end with special chars
    if username[0] in "._-" or username[-1] in "._-":
        raise ValidationError(
            "Username cannot start or end with special characters"
        )

    logger.debug(
        "Username validated",
        extra={"username": username},
    )

    return username


def validate_filename(
    filename: str,
    allowed_extensions: list[str] | None = None,
    max_length: int = 255,
) -> str:
    """
    Validate filename for safe filesystem operations.

    Args:
        filename: Filename to validate
        allowed_extensions: List of allowed file extensions
        max_length: Maximum filename length

    Returns:
        Validated filename

    Raises:
        ValidationError: If filename is invalid
    """
    if not isinstance(filename, str):
        raise ValidationError(f"Expected string, got {type(filename).__name__}")

    filename = filename.strip()

    # Check length
    if len(filename) > max_length:
        raise ValidationError(
            f"Filename exceeds maximum length of {max_length} characters"
        )

    # Check for path traversal attempts
    if ".." in filename or "/" in filename or "\\" in filename:
        raise ValidationError(
            "Filename contains invalid path characters"
        )

    # Check for null bytes
    if "\x00" in filename:
        raise ValidationError("Filename contains null bytes")

    # Validate extension if specified
    if allowed_extensions:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in allowed_extensions:
            raise ValidationError(
                f"File extension '.{ext}' not allowed. Must be one of: {allowed_extensions}"
            )

    logger.debug(
        "Filename validated",
        extra={"filename": filename},
    )

    return filename


def sanitize_sql_identifier(identifier: str) -> str:
    """
    Sanitize SQL identifier (table/column name).

    Args:
        identifier: SQL identifier to sanitize

    Returns:
        Sanitized identifier

    Raises:
        ValidationError: If identifier is invalid
    """
    if not isinstance(identifier, str):
        raise ValidationError(f"Expected string, got {type(identifier).__name__}")

    identifier = identifier.strip()

    # SQL identifiers must start with letter or underscore
    # and contain only alphanumeric and underscore
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", identifier):
        raise ValidationError(
            "Invalid SQL identifier. Must start with letter/underscore "
            "and contain only alphanumeric characters and underscores"
        )

    # Check for SQL reserved words (basic list)
    reserved = {
        "select", "insert", "update", "delete", "drop", "create",
        "alter", "table", "where", "from", "join", "union",
    }

    if identifier.lower() in reserved:
        raise ValidationError(
            f"SQL identifier '{identifier}' is a reserved word"
        )

    logger.debug(
        "SQL identifier sanitized",
        extra={"identifier": identifier},
    )

    return identifier
