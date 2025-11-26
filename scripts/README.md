# Deployment and Utility Scripts

This directory contains scripts for deploying, testing, and managing Sentinel.

## Scripts

### `deploy.sh`
Complete deployment script that:
- Validates prerequisites (AWS CLI, Python, credentials)
- Deploys CloudFormation infrastructure
- Uploads policy documents to S3
- Deploys Lambda functions
- Creates .env configuration file
- Installs Python dependencies

**Usage:**
```bash
./scripts/deploy.sh
```

**Prerequisites:**
- AWS CLI installed and configured
- Appropriate AWS permissions
- Python 3.9+

### `setup.sh`
Local development environment setup:
- Creates Python virtual environment
- Installs all dependencies
- Creates .env file from template
- Runs initial tests

**Usage:**
```bash
./scripts/setup.sh
```

Run this before starting local development.

### `test.sh`
Test runner with multiple modes:
- Unit tests only
- Integration tests only
- Tests with coverage reports
- Code quality checks (linting, formatting, type checking)

**Usage:**
```bash
# Run all tests
./scripts/test.sh all

# Run specific test type
./scripts/test.sh unit
./scripts/test.sh integration
./scripts/test.sh coverage
./scripts/test.sh lint
```

## Quick Start Workflow

### For New Project Setup:
```bash
# 1. Setup local environment
./scripts/setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run tests
./scripts/test.sh

# 4. Deploy to AWS (when ready)
./scripts/deploy.sh
```

### For Development:
```bash
# Activate environment
source venv/bin/activate

# Run tests during development
./scripts/test.sh unit

# Run full test suite before committing
./scripts/test.sh all

# Check code quality
./scripts/test.sh lint
```

## Script Permissions

All scripts should be executable:
```bash
chmod +x scripts/*.sh
```

## Environment Variables

Scripts respect these environment variables:
- `AWS_REGION` - AWS region for deployment (default: us-east-1)
- `ENVIRONMENT` - Deployment environment (dev/staging/prod, default: dev)

Example:
```bash
AWS_REGION=us-west-2 ENVIRONMENT=prod ./scripts/deploy.sh
```

## Troubleshooting

### "Permission denied" errors
Make scripts executable:
```bash
chmod +x scripts/*.sh
```

### AWS CLI errors
Verify AWS credentials:
```bash
aws sts get-caller-identity
```

### Python import errors
Activate virtual environment:
```bash
source venv/bin/activate
```

### Test failures
Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

## CI/CD Integration

These scripts can be integrated into CI/CD pipelines:

**GitHub Actions Example:**
```yaml
- name: Setup
  run: ./scripts/setup.sh

- name: Run Tests
  run: ./scripts/test.sh coverage

- name: Deploy
  run: ./scripts/deploy.sh
  if: github.ref == 'refs/heads/main'
```

## Adding New Scripts

When adding new scripts:
1. Place in `scripts/` directory
2. Add shebang: `#!/bin/bash`
3. Add `set -e` for error handling
4. Make executable: `chmod +x`
5. Document in this README
6. Add usage information in script help text
