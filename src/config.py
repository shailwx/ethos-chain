"""
Configuration management for Sentinel.

This module handles all configuration settings using pydantic-settings
for type-safe configuration with validation.
"""

from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AWSSettings(BaseSettings):
    """AWS-specific configuration settings."""
    
    model_config = SettingsConfigDict(
        env_prefix="AWS_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    region: str = Field(default="us-east-1", description="AWS Region")
    profile: Optional[str] = Field(default=None, description="AWS CLI Profile name")
    
    # Bedrock Configuration
    bedrock_runtime_endpoint: Optional[str] = Field(
        default=None,
        description="Custom Bedrock Runtime endpoint"
    )
    bedrock_model_id: str = Field(
        default="anthropic.claude-3-5-sonnet-20241022-v2:0",
        description="Bedrock model ID for agents"
    )
    
    # Agent IDs (set after deployment)
    supervisor_agent_id: Optional[str] = Field(
        default=None,
        description="Supervisor Agent ID"
    )
    investigator_agent_id: Optional[str] = Field(
        default=None,
        description="Investigator Agent ID"
    )
    auditor_agent_id: Optional[str] = Field(
        default=None,
        description="Auditor Agent ID"
    )
    
    # Knowledge Base
    knowledge_base_id: Optional[str] = Field(
        default=None,
        description="Bedrock Knowledge Base ID for policy documents"
    )
    
    # Lambda Configuration
    news_search_lambda_arn: Optional[str] = Field(
        default=None,
        description="ARN for news search Lambda function"
    )


class AppSettings(BaseSettings):
    """Application-level configuration settings."""
    
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    name: str = Field(default="Sentinel", description="Application name")
    version: str = Field(default="0.1.0", description="Application version")
    environment: str = Field(default="development", description="Environment (dev/staging/prod)")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # Audit Configuration
    audit_timeout_seconds: int = Field(
        default=30,
        description="Maximum time for audit completion"
    )
    max_findings_per_audit: int = Field(
        default=50,
        description="Maximum findings to process per audit"
    )
    
    # Risk Scoring Thresholds
    risk_threshold_yellow: int = Field(default=30, description="Threshold for YELLOW risk")
    risk_threshold_red: int = Field(default=70, description="Threshold for RED risk")


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    
    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
    
    level: str = Field(default="INFO", description="Logging level")
    format: str = Field(
        default="json",
        description="Log format: json or console"
    )
    output_file: Optional[str] = Field(
        default=None,
        description="Optional log file path"
    )


class Settings(BaseSettings):
    """Main application settings combining all configuration sections."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    aws: AWSSettings = Field(default_factory=AWSSettings)
    app: AppSettings = Field(default_factory=AppSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get the global settings instance (singleton pattern).
    
    Returns:
        Settings: The application settings
    """
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def reload_settings() -> Settings:
    """
    Force reload of settings (useful for testing).
    
    Returns:
        Settings: Freshly loaded settings
    """
    global _settings
    _settings = Settings()
    return _settings
