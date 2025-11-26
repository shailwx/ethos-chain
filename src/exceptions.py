"""
Custom exceptions for EthosChain.

This module defines domain-specific exceptions for better error handling.
"""


class EthosChainError(Exception):
    """Base exception for all EthosChain errors."""
    pass


class ConfigurationError(EthosChainError):
    """Raised when there's a configuration issue."""
    pass


class AWSServiceError(EthosChainError):
    """Raised when AWS service calls fail."""
    pass


class BedrockAgentError(AWSServiceError):
    """Raised when Bedrock Agent operations fail."""
    pass


class KnowledgeBaseError(AWSServiceError):
    """Raised when Knowledge Base operations fail."""
    pass


class InvestigationError(EthosChainError):
    """Raised when investigation phase fails."""
    pass


class AuditError(EthosChainError):
    """Raised when audit phase fails."""
    pass


class ValidationError(EthosChainError):
    """Raised when data validation fails."""
    pass


class TimeoutError(EthosChainError):
    """Raised when an operation times out."""
    pass
