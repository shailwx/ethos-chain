#!/bin/bash

# Sentinel Infrastructure Teardown Script
# This script safely deletes the CloudFormation stack

set -e

STACK_NAME="sentinel-infrastructure"
REGION="${AWS_REGION:-us-east-1}"

echo "🗑️  Sentinel Infrastructure Teardown"
echo "===================================="
echo "Stack Name: $STACK_NAME"
echo "Region: $REGION"
echo ""

# Warning prompt
read -p "⚠️  This will DELETE all resources. Are you sure? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

# Get bucket name before deleting stack
echo "📦 Finding S3 bucket..."
BUCKET_NAME=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`KnowledgeBaseBucketName`].OutputValue' \
    --output text 2>/dev/null || echo "")

# Empty S3 bucket first (CloudFormation can't delete non-empty buckets)
if [ ! -z "$BUCKET_NAME" ]; then
    echo "🗑️  Emptying S3 bucket: $BUCKET_NAME"
    aws s3 rm s3://$BUCKET_NAME --recursive --region $REGION 2>/dev/null || echo "Bucket already empty or doesn't exist"
fi

# Delete stack
echo "🔥 Deleting CloudFormation stack..."
aws cloudformation delete-stack \
    --stack-name $STACK_NAME \
    --region $REGION

echo "⏳ Waiting for stack deletion..."
aws cloudformation wait stack-delete-complete \
    --stack-name $STACK_NAME \
    --region $REGION

echo ""
echo "✅ Infrastructure successfully deleted!"
echo ""
echo "Note: You may need to manually delete:"
echo "- Bedrock Agents (if created)"
echo "- Bedrock Knowledge Bases (if created)"
echo "- CloudWatch Log Groups (if retention period hasn't expired)"
