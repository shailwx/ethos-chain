"""
Custom exceptions for Sentinel.

This module defines domain-specific exceptions for better error handling.
"""


class SentinelError(Exception):
    """Base exception for all Sentinel errors."""
    pass


class ConfigurationError(SentinelError):
    """Raised when there's a configuration issue."""
    pass


class AWSServiceError(SentinelError):
    """Raised when AWS service calls fail."""
    pass


class BedrockAgentError(AWSServiceError):
    """Raised when Bedrock Agent operations fail."""
    pass


class KnowledgeBaseError(AWSServiceError):
    """Raised when Knowledge Base operations fail."""
    pass


class InvestigationError(SentinelError):
    """Raised when investigation phase fails."""
    pass


class AuditError(SentinelError):
    """Raised when audit phase fails."""
    pass


class ValidationError(SentinelError):
    """Raised when data validation fails."""
    pass


class TimeoutError(SentinelError):
    """Raised when an operation times out."""
    pass
