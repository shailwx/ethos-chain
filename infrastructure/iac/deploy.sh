#!/bin/bash

# Sentinel Infrastructure Deployment Script
# This script deploys the CloudFormation stack for Sentinel

set -e

# Configuration
STACK_NAME="sentinel-infrastructure"
TEMPLATE_FILE="template.yaml"
REGION="${AWS_REGION:-us-east-1}"
ENVIRONMENT="${ENVIRONMENT:-dev}"

echo "🚀 Deploying Sentinel Infrastructure"
echo "=================================="
echo "Stack Name: $STACK_NAME"
echo "Region: $REGION"
echo "Environment: $ENVIRONMENT"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ Error: AWS CLI is not installed"
    echo "Please install AWS CLI: https://aws.amazon.com/cli/"
    exit 1
fi

# Check if user is authenticated
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Error: Not authenticated with AWS"
    echo "Please run: aws configure"
    exit 1
fi

# Validate template
echo "📋 Validating CloudFormation template..."
aws cloudformation validate-template \
    --template-body file://$TEMPLATE_FILE \
    --region $REGION > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Template validation successful"
else
    echo "❌ Template validation failed"
    exit 1
fi

# Deploy stack
echo ""
echo "🔨 Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file $TEMPLATE_FILE \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        Environment=$ENVIRONMENT \
    --capabilities CAPABILITY_NAMED_IAM \
    --region $REGION \
    --no-fail-on-empty-changeset

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Deployment successful!"
    echo ""
    echo "📊 Stack Outputs:"
    aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs' \
        --output table
else
    echo "❌ Deployment failed"
    exit 1
fi

echo ""
echo "🎉 Infrastructure deployment complete!"
echo ""
echo "Next steps:"
echo "1. Upload policy documents to the S3 bucket"
echo "2. Create Bedrock Knowledge Base using the AWS Console"
echo "3. Create Bedrock Agents (see infrastructure/bedrock/README.md)"
echo "4. Deploy Lambda function code (see infrastructure/lambda/)"
