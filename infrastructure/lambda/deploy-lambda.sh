#!/bin/bash

# Lambda Deployment Script
# Packages and deploys Lambda functions to AWS

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
FUNCTION_NAME="${1:-sentinel-news-search-dev}"
REGION="${AWS_REGION:-us-east-1}"

echo "📦 Deploying Lambda Function: $FUNCTION_NAME"
echo "Region: $REGION"
echo ""

# Check if function name provided
if [ -z "$1" ]; then
    echo "ℹ️  Using default function name: $FUNCTION_NAME"
    echo "   Usage: ./deploy-lambda.sh <function-name>"
fi

# Create deployment package
echo "📁 Creating deployment package..."
cd "$SCRIPT_DIR"

# Create temp directory for package
mkdir -p package
cd package

# Install dependencies
if [ -f ../requirements.txt ]; then
    echo "📥 Installing dependencies..."
    pip install -r ../requirements.txt -t . --quiet
fi

# Copy Lambda function
cp ../news_search.py .

# Create zip file
echo "🗜️  Creating zip file..."
zip -r ../lambda-deployment.zip . -q

cd ..
rm -rf package

# Deploy to AWS
echo "☁️  Deploying to AWS Lambda..."
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://lambda-deployment.zip \
    --region "$REGION" \
    --no-cli-pager

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Lambda function deployed successfully!"
    
    # Update environment variables
    echo ""
    echo "📝 Updating environment variables..."
    aws lambda update-function-configuration \
        --function-name "$FUNCTION_NAME" \
        --environment "Variables={ENABLE_REAL_API=false,NEWS_API_KEY=}" \
        --region "$REGION" \
        --no-cli-pager > /dev/null
    
    echo "✅ Environment variables updated"
    echo ""
    echo "ℹ️  To enable real news API:"
    echo "   1. Get API key from https://newsapi.org"
    echo "   2. Run: aws lambda update-function-configuration \\"
    echo "      --function-name $FUNCTION_NAME \\"
    echo "      --environment Variables={ENABLE_REAL_API=true,NEWS_API_KEY=your_key_here}"
else
    echo "❌ Deployment failed"
    exit 1
fi

# Cleanup
rm -f lambda-deployment.zip

echo ""
echo "🎉 Deployment complete!"
