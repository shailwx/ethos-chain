"""
AWS client utilities for Sentinel.

Provides factory functions for creating AWS service clients with
proper configuration and error handling.
"""

from functools import lru_cache
from typing import Any, Optional

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from src.config import get_settings
from src.exceptions import AWSServiceError, BedrockAgentError, KnowledgeBaseError
from src.logging_config import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=10)
def get_boto3_session(profile_name: Optional[str] = None) -> boto3.Session:
    """
    Get or create a boto3 session.
    
    Args:
        profile_name: Optional AWS profile name
        
    Returns:
        Configured boto3 Session
    """
    settings = get_settings()
    profile = profile_name or settings.aws.profile
    
    try:
        if profile:
            session = boto3.Session(
                profile_name=profile,
                region_name=settings.aws.region
            )
            logger.info("Created boto3 session", profile=profile, region=settings.aws.region)
        else:
            session = boto3.Session(region_name=settings.aws.region)
            logger.info("Created boto3 session", region=settings.aws.region)
        
        return session
    except Exception as e:
        logger.error("Failed to create boto3 session", error=str(e))
        raise AWSServiceError(f"Failed to create AWS session: {e}")


def get_boto_config() -> Config:
    """
    Get boto3 client configuration.
    
    Returns:
        Botocore Config object with retry and timeout settings
    """
    settings = get_settings()
    
    return Config(
        region_name=settings.aws.region,
        retries={
            'max_attempts': 3,
            'mode': 'adaptive'
        },
        connect_timeout=5,
        read_timeout=settings.app.audit_timeout_seconds,
    )


@lru_cache(maxsize=5)
def get_bedrock_agent_runtime_client(session: Optional[boto3.Session] = None) -> Any:
    """
    Get Bedrock Agent Runtime client.
    
    Args:
        session: Optional boto3 session
        
    Returns:
        Bedrock Agent Runtime client
    """
    settings = get_settings()
    
    if session is None:
        session = get_boto3_session()
    
    try:
        client = session.client(
            'bedrock-agent-runtime',
            config=get_boto_config(),
            endpoint_url=settings.aws.bedrock_runtime_endpoint
        )
        logger.info("Created Bedrock Agent Runtime client")
        return client
    except (BotoCoreError, ClientError) as e:
        logger.error("Failed to create Bedrock Agent Runtime client", error=str(e))
        raise BedrockAgentError(f"Failed to create Bedrock Agent Runtime client: {e}")


@lru_cache(maxsize=5)
def get_bedrock_agent_client(session: Optional[boto3.Session] = None) -> Any:
    """
    Get Bedrock Agent client for management operations.
    
    Args:
        session: Optional boto3 session
        
    Returns:
        Bedrock Agent client
    """
    if session is None:
        session = get_boto3_session()
    
    try:
        client = session.client('bedrock-agent', config=get_boto_config())
        logger.info("Created Bedrock Agent client")
        return client
    except (BotoCoreError, ClientError) as e:
        logger.error("Failed to create Bedrock Agent client", error=str(e))
        raise BedrockAgentError(f"Failed to create Bedrock Agent client: {e}")


@lru_cache(maxsize=5)
def get_lambda_client(session: Optional[boto3.Session] = None) -> Any:
    """
    Get Lambda client.
    
    Args:
        session: Optional boto3 session
        
    Returns:
        Lambda client
    """
    if session is None:
        session = get_boto3_session()
    
    try:
        client = session.client('lambda', config=get_boto_config())
        logger.info("Created Lambda client")
        return client
    except (BotoCoreError, ClientError) as e:
        logger.error("Failed to create Lambda client", error=str(e))
        raise AWSServiceError(f"Failed to create Lambda client: {e}")


def invoke_bedrock_agent(
    agent_id: str,
    agent_alias_id: str,
    session_id: str,
    input_text: str,
    session: Optional[boto3.Session] = None
) -> dict:
    """
    Invoke a Bedrock Agent.
    
    Args:
        agent_id: The agent ID
        agent_alias_id: The agent alias ID
        session_id: Session ID for the conversation
        input_text: Input text to send to the agent
        session: Optional boto3 session
        
    Returns:
        Agent response dict
        
    Raises:
        BedrockAgentError: If invocation fails
    """
    client = get_bedrock_agent_runtime_client(session)
    
    try:
        logger.info(
            "Invoking Bedrock agent",
            agent_id=agent_id,
            session_id=session_id
        )
        
        response = client.invoke_agent(
            agentId=agent_id,
            agentAliasId=agent_alias_id,
            sessionId=session_id,
            inputText=input_text
        )
        
        logger.info("Bedrock agent invoked successfully", agent_id=agent_id)
        return response
        
    except ClientError as e:
        logger.error(
            "Failed to invoke Bedrock agent",
            agent_id=agent_id,
            error=str(e)
        )
        raise BedrockAgentError(f"Failed to invoke agent {agent_id}: {e}")


def query_knowledge_base(
    knowledge_base_id: str,
    query_text: str,
    max_results: int = 5,
    session: Optional[boto3.Session] = None
) -> dict:
    """
    Query a Bedrock Knowledge Base.
    
    Args:
        knowledge_base_id: Knowledge Base ID
        query_text: Query text
        max_results: Maximum number of results to return
        session: Optional boto3 session
        
    Returns:
        Query results dict
        
    Raises:
        KnowledgeBaseError: If query fails
    """
    client = get_bedrock_agent_runtime_client(session)
    
    try:
        logger.info(
            "Querying Knowledge Base",
            kb_id=knowledge_base_id,
            query=query_text
        )
        
        response = client.retrieve(
            knowledgeBaseId=knowledge_base_id,
            retrievalQuery={'text': query_text},
            retrievalConfiguration={
                'vectorSearchConfiguration': {
                    'numberOfResults': max_results
                }
            }
        )
        
        logger.info(
            "Knowledge Base queried successfully",
            kb_id=knowledge_base_id,
            result_count=len(response.get('retrievalResults', []))
        )
        return response
        
    except ClientError as e:
        logger.error(
            "Failed to query Knowledge Base",
            kb_id=knowledge_base_id,
            error=str(e)
        )
        raise KnowledgeBaseError(f"Failed to query Knowledge Base {knowledge_base_id}: {e}")
