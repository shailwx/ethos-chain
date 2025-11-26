# Infrastructure as Code (IaC)

This directory contains Infrastructure as Code templates for deploying Sentinel to AWS.

## Files

- `template.yaml` - CloudFormation template for AWS resources
- `deploy.sh` - Deployment script
- `teardown.sh` - Script to delete the stack

## Prerequisites

1. AWS CLI installed and configured
2. AWS Account with Bedrock access enabled
3. Sufficient IAM permissions to create resources

## What Gets Deployed

The CloudFormation template creates:

- **S3 Bucket** - For storing Knowledge Base documents (Code of Conduct)
- **IAM Roles** - For Lambda functions, Bedrock Agents, and Knowledge Base
- **Lambda Function** - For news search action group
- **CloudWatch Log Groups** - For Lambda logging

**Note:** Bedrock Agents and Knowledge Bases must be created manually through the AWS Console or using the Bedrock API, as CloudFormation support is limited.

## Deployment

### 1. Deploy Infrastructure

```bash
cd infrastructure/iac
chmod +x deploy.sh
./deploy.sh
```

The script will:
- Validate the CloudFormation template
- Deploy the stack
- Display outputs (bucket names, ARNs, etc.)

### 2. Upload Policy Documents

After deployment, upload your Code of Conduct documents to the S3 bucket:

```bash
# Get bucket name from stack outputs
BUCKET_NAME=$(aws cloudformation describe-stacks \
    --stack-name sentinel-infrastructure \
    --query 'Stacks[0].Outputs[?OutputKey==`KnowledgeBaseBucketName`].OutputValue' \
    --output text)

# Upload policy documents
aws s3 cp ../../data/policies/ s3://$BUCKET_NAME/policies/ --recursive
```

### 3. Create Bedrock Knowledge Base

Use the AWS Console or CLI to create a Knowledge Base:

1. Go to AWS Bedrock Console → Knowledge Bases
2. Create new Knowledge Base
3. Select S3 bucket created by CloudFormation
4. Choose embedding model (e.g., `amazon.titan-embed-text-v1`)
5. Configure sync settings
6. Note the Knowledge Base ID for later use

### 4. Create Bedrock Agents

See `../bedrock/README.md` for instructions on creating the three agents:
- Supervisor Agent
- Investigator Agent
- Auditor Agent

### 5. Deploy Lambda Code

Update the Lambda function with actual code:

```bash
cd ../lambda
zip news_search.zip news_search.py
aws lambda update-function-code \
    --function-name sentinel-news-search-dev \
    --zip-file fileb://news_search.zip
```

## Configuration

You can customize deployment parameters by editing environment variables:

```bash
export AWS_REGION=us-west-2
export ENVIRONMENT=prod
./deploy.sh
```

## Cleanup

To delete all resources:

```bash
./teardown.sh
```

**Warning:** This will delete all resources including the S3 bucket. Ensure you have backups of important data.

## Cost Estimate

Approximate monthly costs (us-east-1):
- S3 Storage: ~$0.023/GB
- Lambda: First 1M requests free, then $0.20 per 1M requests
- Bedrock Knowledge Base: Based on storage and queries
- Bedrock Agents: Based on token usage (~$0.003 per 1K input tokens)

For a hackathon/demo with moderate usage: **~$5-20/month**

## Troubleshooting

### Stack creation fails with "Model access not enabled"

You need to enable model access in AWS Bedrock:
1. Go to AWS Bedrock Console
2. Click "Model access" in the left sidebar
3. Request access to Claude 3.5 Sonnet and Titan Embeddings

### "Access Denied" errors

Ensure your IAM user has these permissions:
- CloudFormation full access
- IAM role creation
- S3 bucket creation
- Lambda function creation
- Bedrock full access

## Security Notes

- S3 bucket has encryption enabled by default
- Public access is blocked on all buckets
- IAM roles follow least-privilege principle
- CloudWatch logs retain for 7 days (adjust as needed)

## Support

For issues or questions, refer to:
- AWS Bedrock Documentation: https://docs.aws.amazon.com/bedrock/
- CloudFormation Documentation: https://docs.aws.amazon.com/cloudformation/
