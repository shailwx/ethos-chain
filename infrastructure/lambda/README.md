# Lambda Functions

This directory contains AWS Lambda functions used as Action Groups for Bedrock Agents.

## Files

- `news_search.py` - Lambda function for searching news and reports about suppliers
- `requirements.txt` - Python dependencies for Lambda functions
- `deploy-lambda.sh` - Deployment script

## Functions

### news_search.py

**Purpose**: Searches news sources and public databases for information about suppliers.

**Invoked by**: Investigator Agent (as an Action Group)

**Parameters**:
- `supplier_name` (required): Name of the supplier to search for
- `categories` (optional): Array of categories to focus on (labor, environment, governance)
- `date_range` (optional): Time range for search (e.g., "2y" for 2 years)

**Returns**: JSON with findings including date, source, URL, category, and snippet

**Environment Variables**:
- `NEWS_API_KEY`: API key for NewsAPI.org (optional)
- `ENABLE_REAL_API`: Set to "true" to use real API instead of mock data

## Local Testing

Test Lambda function locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Create test event
cat > test_event.json << EOF
{
  "supplier_name": "Acme Corporation",
  "categories": ["labor", "environment"],
  "date_range": "2y"
}
EOF

# Run locally using Python
python3 << EOF
import json
from news_search import lambda_handler

with open('test_event.json') as f:
    event = json.load(f)

class Context:
    def __init__(self):
        self.function_name = "test"
        self.memory_limit_in_mb = 256
        self.invoked_function_arn = "arn:aws:lambda:test"
        self.aws_request_id = "test-id"

result = lambda_handler(event, Context())
print(json.dumps(result, indent=2))
EOF
```

## Deployment

### Prerequisites

1. Infrastructure deployed (see `../iac/README.md`)
2. Lambda function created by CloudFormation
3. AWS CLI configured

### Deploy Function

```bash
chmod +x deploy-lambda.sh
./deploy-lambda.sh
```

Or specify function name:

```bash
./deploy-lambda.sh sentinel-news-search-prod
```

### Manual Deployment

If the script doesn't work, deploy manually:

```bash
# Install dependencies
mkdir -p package
pip install -r requirements.txt -t package/
cp news_search.py package/

# Create zip
cd package
zip -r ../lambda-deployment.zip .
cd ..

# Deploy
aws lambda update-function-code \
    --function-name sentinel-news-search-dev \
    --zip-file fileb://lambda-deployment.zip

# Cleanup
rm -rf package lambda-deployment.zip
```

## Enable Real News API

To use real NewsAPI instead of mock data:

1. Sign up at https://newsapi.org and get an API key

2. Update Lambda environment variables:

```bash
aws lambda update-function-configuration \
    --function-name sentinel-news-search-dev \
    --environment Variables="{ENABLE_REAL_API=true,NEWS_API_KEY=your_api_key_here}"
```

3. Test the function:

```bash
aws lambda invoke \
    --function-name sentinel-news-search-dev \
    --payload '{"supplier_name":"Tesla","categories":["labor","environment"]}' \
    response.json

cat response.json
```

## Monitoring

View Lambda logs:

```bash
# Tail logs
aws logs tail /aws/lambda/sentinel-news-search-dev --follow

# Get recent logs
aws logs filter-log-events \
    --log-group-name /aws/lambda/sentinel-news-search-dev \
    --start-time $(date -d '1 hour ago' +%s)000
```

## Error Handling

The Lambda function includes:
- Parameter validation
- Timeout handling (30 seconds)
- Structured error responses for Bedrock Agent
- Detailed CloudWatch logging
- Graceful fallback to mock data

## Cost Optimization

- Function timeout: 30 seconds (adjust if needed)
- Memory: 256 MB (increase if processing large datasets)
- Reserved concurrency: Not set (can add for production)
- Provisioned concurrency: Not enabled (overkill for this use case)

Estimated cost: ~$0.20 per 1M invocations (after free tier)

## Future Enhancements

Possible improvements:
- Add caching layer (DynamoDB or ElastiCache)
- Integrate multiple news APIs for broader coverage
- Add web scraping for NGO reports
- Implement rate limiting and retry logic
- Add support for multiple languages
- Store search history for audit trail

## Troubleshooting

### Function times out
- Increase timeout in CloudFormation template
- Optimize API calls (parallel requests, caching)
- Check network connectivity to external APIs

### "Unable to import module" error
- Ensure all dependencies are in the deployment package
- Check Python version compatibility (Lambda uses 3.11)
- Verify package structure (files should be at root of zip)

### Bedrock Agent can't invoke function
- Check Lambda resource-based policy allows Bedrock
- Verify Action Group configuration in Agent
- Check Lambda function ARN is correct
- Review CloudWatch logs for invocation errors

## Security

- Function uses IAM role with least-privilege permissions
- Environment variables encrypted at rest
- No sensitive data logged
- API keys stored in environment variables (consider AWS Secrets Manager for production)
