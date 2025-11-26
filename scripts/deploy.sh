#!/bin/bash

# Sentinel Complete Deployment Script
# This script orchestrates the entire deployment process

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

echo "🚀 Sentinel - Complete Deployment"
echo "=================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step tracker
STEP=1

print_step() {
    echo ""
    echo -e "${GREEN}Step $STEP: $1${NC}"
    echo "----------------------------------------"
    ((STEP++))
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Check prerequisites
print_step "Checking Prerequisites"

if ! command -v aws &> /dev/null; then
    print_error "AWS CLI not installed"
    echo "Install from: https://aws.amazon.com/cli/"
    exit 1
fi
print_success "AWS CLI installed"

if ! aws sts get-caller-identity &> /dev/null; then
    print_error "Not authenticated with AWS"
    echo "Run: aws configure"
    exit 1
fi
print_success "AWS credentials configured"

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not installed"
    exit 1
fi
print_success "Python 3 installed"

# Get AWS account info
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=${AWS_REGION:-us-east-1}

echo ""
echo "Account ID: $AWS_ACCOUNT_ID"
echo "Region: $AWS_REGION"

# Confirm deployment
echo ""
read -p "Proceed with deployment? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Deployment cancelled"
    exit 0
fi

# Deploy infrastructure
print_step "Deploying Infrastructure (CloudFormation)"
cd "$PROJECT_ROOT/infrastructure/iac"
chmod +x deploy.sh
./deploy.sh

if [ $? -ne 0 ]; then
    print_error "Infrastructure deployment failed"
    exit 1
fi
print_success "Infrastructure deployed"

# Get outputs from CloudFormation
print_step "Retrieving Infrastructure Outputs"
KB_BUCKET=$(aws cloudformation describe-stacks \
    --stack-name sentinel-infrastructure \
    --query 'Stacks[0].Outputs[?OutputKey==`KnowledgeBaseBucketName`].OutputValue' \
    --output text \
    --region $AWS_REGION)

LAMBDA_ARN=$(aws cloudformation describe-stacks \
    --stack-name sentinel-infrastructure \
    --query 'Stacks[0].Outputs[?OutputKey==`NewsSearchFunctionArn`].OutputValue' \
    --output text \
    --region $AWS_REGION)

echo "S3 Bucket: $KB_BUCKET"
echo "Lambda ARN: $LAMBDA_ARN"

# Upload policy documents
print_step "Uploading Policy Documents to S3"
if [ -d "$PROJECT_ROOT/data/policies" ]; then
    aws s3 cp "$PROJECT_ROOT/data/policies/" "s3://$KB_BUCKET/policies/" \
        --recursive \
        --region $AWS_REGION
    
    print_success "Policy documents uploaded"
else
    print_warning "Policy documents directory not found"
fi

# Deploy Lambda function code
print_step "Deploying Lambda Function Code"
cd "$PROJECT_ROOT/infrastructure/lambda"
chmod +x deploy-lambda.sh
./deploy-lambda.sh

if [ $? -ne 0 ]; then
    print_error "Lambda deployment failed"
    exit 1
fi
print_success "Lambda function deployed"

# Create .env file if it doesn't exist
print_step "Creating Environment Configuration"
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    
    # Update with actual values
    sed -i "s/AWS_REGION=.*/AWS_REGION=$AWS_REGION/" "$PROJECT_ROOT/.env"
    sed -i "s/AWS_ACCOUNT_ID=.*/AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID/" "$PROJECT_ROOT/.env"
    sed -i "s|KNOWLEDGE_BASE_BUCKET=.*|KNOWLEDGE_BASE_BUCKET=$KB_BUCKET|" "$PROJECT_ROOT/.env"
    sed -i "s|NEWS_SEARCH_LAMBDA_ARN=.*|NEWS_SEARCH_LAMBDA_ARN=$LAMBDA_ARN|" "$PROJECT_ROOT/.env"
    
    print_success ".env file created"
else
    print_warning ".env file already exists (not modified)"
fi

# Install Python dependencies
print_step "Installing Python Dependencies"
cd "$PROJECT_ROOT"
if [ -f "requirements.txt" ]; then
    python3 -m pip install -r requirements.txt --quiet
    print_success "Dependencies installed"
else
    print_warning "requirements.txt not found"
fi

# Summary
print_step "Deployment Summary"
echo "🎉 Infrastructure deployment complete!"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Create Knowledge Base:"
echo "   - Go to AWS Bedrock Console → Knowledge Bases"
echo "   - Create new Knowledge Base"
echo "   - Use S3 bucket: $KB_BUCKET"
echo "   - Select embedding model: amazon.titan-embed-text-v1"
echo "   - Note the Knowledge Base ID"
echo ""
echo "2. Create Bedrock Agents:"
echo "   - See: infrastructure/bedrock/README.md"
echo "   - Create Investigator, Auditor, and Supervisor agents"
echo "   - Note the Agent IDs and Alias IDs"
echo ""
echo "3. Update Configuration:"
echo "   - Edit .env file with your Agent IDs and Knowledge Base ID"
echo ""
echo "4. Test the System:"
echo "   cd $PROJECT_ROOT"
echo "   streamlit run src/dashboard/app.py"
echo ""
echo "📚 Documentation:"
echo "   - Infrastructure: infrastructure/iac/README.md"
echo "   - Bedrock Agents: infrastructure/bedrock/README.md"
echo "   - Lambda Functions: infrastructure/lambda/README.md"
echo ""
print_success "Deployment complete!"
