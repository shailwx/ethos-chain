"""
AWS Lambda function for news search action group.

This Lambda function is invoked by the Investigator Agent to search
for news and reports about suppliers.

Reference: SPEC_Version2.md - Investigator Agent Tools
"""

import json
import os
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import traceback

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Environment variables
NEWS_API_KEY = os.environ.get('NEWS_API_KEY', '')
ENABLE_REAL_API = os.environ.get('ENABLE_REAL_API', 'false').lower() == 'true'


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for news search.
    
    Args:
        event: Lambda event from Bedrock Agent containing parameters
        context: Lambda context
        
    Returns:
        Dict with news search results in Bedrock Agent response format
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Extract parameters from Bedrock Agent event structure
        # Bedrock agents send parameters in different structures
        parameters = extract_parameters(event)
        
        supplier_name = parameters.get("supplier_name", "")
        categories = parameters.get("categories", ["labor", "environment", "governance"])
        date_range = parameters.get("date_range", "2y")
        
        if not supplier_name:
            return create_error_response(400, "supplier_name is required")
        
        logger.info(f"Searching news for supplier: {supplier_name}")
        logger.info(f"Categories: {categories}, Date range: {date_range}")
        
        # Search for news
        if ENABLE_REAL_API and NEWS_API_KEY:
            results = search_real_news(supplier_name, categories, date_range)
        else:
            logger.info("Using mock data (real API not enabled)")
            results = mock_news_search(supplier_name, categories)
        
        logger.info(f"Found {len(results.get('findings', []))} findings")
        
        # Return response in Bedrock Agent format
        return create_success_response(results)
        
    except Exception as e:
        logger.error(f"Error in lambda_handler: {str(e)}")
        logger.error(traceback.format_exc())
        return create_error_response(500, str(e))


def extract_parameters(event: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract parameters from Bedrock Agent event structure.
    
    Bedrock Agent events can have different structures depending on
    how they're invoked.
    """
    # Check for direct parameters
    if "supplier_name" in event:
        return event
    
    # Check for requestBody structure (common in Bedrock Agent invocations)
    if "requestBody" in event:
        body = event["requestBody"]
        if "content" in body:
            content = body["content"]
            if "application/json" in content:
                json_content = content["application/json"]
                if "properties" in json_content:
                    # Extract from properties array
                    properties = json_content["properties"]
                    params = {}
                    for prop in properties:
                        params[prop["name"]] = prop["value"]
                    return params
    
    # Check for parameters in apiPath
    if "parameters" in event:
        params = {}
        for param in event["parameters"]:
            params[param["name"]] = param["value"]
        return params
    
    return {}


def create_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a successful response in Bedrock Agent format."""
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": "NewsSearchActions",
            "apiPath": "/search-news",
            "httpMethod": "POST",
            "httpStatusCode": 200,
            "responseBody": {
                "application/json": {
                    "body": json.dumps(data)
                }
            }
        }
    }


def create_error_response(status_code: int, error_message: str) -> Dict[str, Any]:
    """Create an error response in Bedrock Agent format."""
    return {
        "messageVersion": "1.0",
        "response": {
            "actionGroup": "NewsSearchActions",
            "apiPath": "/search-news",
            "httpMethod": "POST",
            "httpStatusCode": status_code,
            "responseBody": {
                "application/json": {
                    "body": json.dumps({"error": error_message})
                }
            }
        }
    }


def search_real_news(
    supplier_name: str, 
    categories: List[str], 
    date_range: str
) -> Dict[str, Any]:
    """
    Search real news APIs for supplier information.
    
    TODO: Integrate with actual news APIs:
    - NewsAPI.org
    - Google News API
    - Bing News Search API
    - Custom scrapers for NGO reports
    """
    import requests
    
    findings = []
    
    # Parse date range (e.g., "2y" = 2 years)
    days_back = parse_date_range(date_range)
    from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
    
    # Example: NewsAPI integration
    if NEWS_API_KEY:
        try:
            # Build search query with categories
            category_keywords = {
                "labor": "labor OR workers OR strike OR wages OR safety OR union",
                "environment": "pollution OR environmental OR emissions OR fine OR EPA",
                "governance": "corruption OR bribery OR fraud OR ethics OR scandal"
            }
            
            for category in categories:
                keywords = category_keywords.get(category, "")
                query = f'"{supplier_name}" AND ({keywords})'
                
                url = "https://newsapi.org/v2/everything"
                params = {
                    "q": query,
                    "from": from_date,
                    "sortBy": "relevancy",
                    "language": "en",
                    "apiKey": NEWS_API_KEY
                }
                
                response = requests.get(url, params=params, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get("articles", [])
                    
                    for article in articles[:5]:  # Limit to 5 per category
                        findings.append({
                            "date": article.get("publishedAt", "")[:10],
                            "source": article.get("source", {}).get("name", "Unknown"),
                            "url": article.get("url", ""),
                            "category": category.capitalize(),
                            "snippet": article.get("description", article.get("title", ""))
                        })
                        
        except Exception as e:
            logger.error(f"Error fetching from NewsAPI: {str(e)}")
    
    return {
        "supplier": supplier_name,
        "search_date": datetime.now().isoformat(),
        "findings": findings
    }


def parse_date_range(date_range: str) -> int:
    """Parse date range string to days (e.g., '2y' -> 730 days)."""
    try:
        value = int(date_range[:-1])
        unit = date_range[-1].lower()
        
        if unit == 'd':
            return value
        elif unit == 'w':
            return value * 7
        elif unit == 'm':
            return value * 30
        elif unit == 'y':
            return value * 365
    except:
        pass
    
    return 730  # Default to 2 years


def mock_news_search(supplier_name: str, categories: List[str]) -> Dict[str, Any]:
    """
    Mock news search for development and testing.
    
    Returns realistic mock data based on the supplier name.
    """
    mock_data_templates = {
        "labor": [
            {
                "date": "2024-03-15",
                "source": "Labor Rights Watch",
                "snippet": f"Workers at {supplier_name} factory report unsafe working conditions and lack of protective equipment.",
                "category": "Labor",
                "url": "https://example.com/labor/unsafe-conditions-123"
            },
            {
                "date": "2024-01-20",
                "source": "International Labor Organization",
                "snippet": f"{supplier_name} faces allegations of excessive overtime without proper compensation.",
                "category": "Labor",
                "url": "https://example.com/labor/overtime-456"
            }
        ],
        "environment": [
            {
                "date": "2024-06-10",
                "source": "Environmental Protection Agency",
                "snippet": f"{supplier_name} fined $2.5 million for river pollution violations and failure to maintain proper waste disposal systems.",
                "category": "Environment",
                "url": "https://example.com/env/pollution-fine-789"
            },
            {
                "date": "2024-04-05",
                "source": "Green Earth Coalition",
                "snippet": f"Investigation finds {supplier_name} exceeded emission limits for three consecutive months.",
                "category": "Environment",
                "url": "https://example.com/env/emissions-012"
            }
        ],
        "governance": [
            {
                "date": "2024-02-28",
                "source": "Corporate Ethics Quarterly",
                "snippet": f"{supplier_name} executive under investigation for potential conflict of interest in procurement deals.",
                "category": "Governance",
                "url": "https://example.com/gov/ethics-345"
            }
        ]
    }
    
    findings = []
    for category in categories:
        if category.lower() in mock_data_templates:
            findings.extend(mock_data_templates[category.lower()])
    
    return {
        "supplier": supplier_name,
        "search_date": datetime.now().isoformat(),
        "findings": findings,
        "note": "MOCK DATA - Enable ENABLE_REAL_API for live results"
    }
