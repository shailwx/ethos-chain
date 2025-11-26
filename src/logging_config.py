"""
Logging configuration for EthosChain.

Provides structured logging using structlog for consistent log output.
"""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.types import EventDict, Processor

from src.config import get_settings


def add_app_context(logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
    """Add application context to log entries."""
    settings = get_settings()
    event_dict["app_name"] = settings.app.name
    event_dict["app_version"] = settings.app.version
    event_dict["environment"] = settings.app.environment
    return event_dict


def configure_logging() -> None:
    """
    Configure structured logging for the application.
    
    Sets up structlog with appropriate processors and formatters
    based on the LOG_FORMAT setting.
    """
    settings = get_settings()
    
    # Set logging level
    log_level = getattr(logging, settings.logging.level.upper(), logging.INFO)
    
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )
    
    # Determine processors based on format
    if settings.logging.format.lower() == "json":
        processors: list[Processor] = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper(fmt="iso"),
            add_app_context,
            structlog.processors.JSONRenderer(),
        ]
    else:
        # Console format for development
        processors = [
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            add_app_context,
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.BoundLogger:
    """
    Get a logger instance for the given name.
    
    Args:
        name: Logger name (typically __name__)
        
    Returns:
        Configured structlog logger
    """
    return structlog.get_logger(name)
