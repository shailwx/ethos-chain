# AWS Bedrock Agent Configurations

This directory contains configuration files for AWS Bedrock Agents.

## Agents

1. **Investigator Agent** - Intelligence gatherer (with Lambda Action Group)
2. **Auditor Agent** - Policy enforcer (with Knowledge Base)
3. **Supervisor Agent** - Orchestrator (coordinates sub-agents)

## Files

- `investigator-agent-config.json` - Configuration for Investigator Agent
- `auditor-agent-config.json` - Configuration for Auditor Agent
- `supervisor-agent-config.json` - Configuration for Supervisor Agent
- `create-agents.sh` - Script to create all agents via AWS CLI
- `knowledge-base-config.json` - Knowledge Base configuration

## Prerequisites

Before creating agents, ensure you have:

1. ✅ Deployed infrastructure (see `../iac/README.md`)
2. ✅ Uploaded policy documents to S3 bucket
3. ✅ Created Knowledge Base in AWS Console
4. ✅ AWS CLI configured with appropriate permissions
5. ✅ Model access enabled for Claude 3.5 Sonnet in Bedrock

## Setup Instructions

### Step 1: Create Knowledge Base

The Auditor Agent requires a Knowledge Base with your Code of Conduct documents.

1. Go to AWS Bedrock Console → Knowledge Bases
2. Click "Create knowledge base"
3. **Name**: `sentinel-ethics-kb`
4. **IAM Role**: Select the role created by CloudFormation (`sentinel-kb-role-dev`)
5. **Data Source**: 
   - Select S3 as data source
   - Choose the bucket created by CloudFormation
   - Prefix: `policies/`
6. **Embedding Model**: `amazon.titan-embed-text-v1`
7. **Vector Store**: Select "Quick create new vector store" (Amazon OpenSearch Serverless)
8. Click "Create"
9. Wait for sync to complete
10. **Note the Knowledge Base ID** (you'll need this for the Auditor Agent)

### Step 2: Update Configuration Files

Before creating agents, update the placeholder values:

**In `auditor-agent-config.json`:**
```bash
# Replace KNOWLEDGE_BASE_ID_PLACEHOLDER with your actual Knowledge Base ID
sed -i 's/KNOWLEDGE_BASE_ID_PLACEHOLDER/YOUR_KB_ID_HERE/g' auditor-agent-config.json
```

**In all config files:**
- Replace `REGION` with your AWS region (e.g., `us-east-1`)
- Replace `ACCOUNT_ID` with your AWS account ID
- Update Lambda ARN in `investigator-agent-config.json`

### Step 3: Create Agents Using AWS Console (Recommended for First Time)

#### Create Investigator Agent

1. Go to AWS Bedrock Console → Agents
2. Click "Create Agent"
3. **Agent name**: `sentinel-investigator`
4. **Description**: Copy from `investigator-agent-config.json`
5. **Model**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
6. **Instructions**: Copy the instruction text from `investigator-agent-config.json`
7. **Action Groups**:
   - Click "Add action group"
   - **Name**: `NewsSearchActions`
   - **Action group type**: Lambda function
   - **Lambda**: Select `sentinel-news-search-dev`
   - **API Schema**: Upload or paste the OpenAPI schema from config
8. Click "Create"
9. Create an alias: `v1` (production-ready)
10. **Note the Agent ID and Alias ARN**

#### Create Auditor Agent

1. Create new agent: `sentinel-auditor`
2. Copy description and instructions from `auditor-agent-config.json`
3. **Model**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
4. **Knowledge Base**:
   - Click "Add knowledge base"
   - Select the Knowledge Base you created in Step 1
   - Instructions: "Query this knowledge base to evaluate if findings violate policy"
5. Click "Create"
6. Create an alias: `v1`
7. **Note the Agent ID and Alias ARN**

#### Create Supervisor Agent

1. Create new agent: `sentinel-supervisor`
2. Copy description and instructions from `supervisor-agent-config.json`
3. **Model**: `anthropic.claude-3-5-sonnet-20241022-v2:0`
4. **Sub-Agents** (if available in your region):
   - Add Investigator Agent alias ARN
   - Add Auditor Agent alias ARN
   
   **Note**: Multi-agent collaboration may not be available in all regions yet. If not available:
   - Configure Supervisor to use Action Groups that invoke the other agents
   - See alternative setup in `multi-agent-workaround.md`
   
5. Click "Create"
6. Create an alias: `v1`
7. **Note the Agent ID and Alias ARN**

### Step 4: Test Agents

Test each agent individually before integrating:

**Test Investigator:**
```bash
aws bedrock-agent-runtime invoke-agent \
    --agent-id YOUR_INVESTIGATOR_AGENT_ID \
    --agent-alias-id YOUR_ALIAS_ID \
    --session-id test-session-1 \
    --input-text "Search for news about Acme Corporation" \
    --region us-east-1 \
    response.txt
```

**Test Auditor:**
```bash
# First, prepare test findings in a file
aws bedrock-agent-runtime invoke-agent \
    --agent-id YOUR_AUDITOR_AGENT_ID \
    --agent-alias-id YOUR_ALIAS_ID \
    --session-id test-session-2 \
    --input-text "Evaluate these findings: Company XYZ was fined $2M for river pollution" \
    --region us-east-1 \
    response.txt
```

**Test Supervisor:**
```bash
aws bedrock-agent-runtime invoke-agent \
    --agent-id YOUR_SUPERVISOR_AGENT_ID \
    --agent-alias-id YOUR_ALIAS_ID \
    --session-id test-session-3 \
    --input-text "Audit supplier: Acme Corporation" \
    --region us-east-1 \
    response.txt
```

### Step 5: Update Application Configuration

After creating agents, update the application config:

1. Copy `.env.example` to `.env` in the project root
2. Add your Agent IDs and Alias ARNs:

```bash
AWS_REGION=us-east-1
SUPERVISOR_AGENT_ID=YOUR_AGENT_ID
SUPERVISOR_ALIAS_ID=YOUR_ALIAS_ID
```

## Alternative: Create Agents via AWS CLI

You can also use the provided script to create agents programmatically:

```bash
chmod +x create-agents.sh
./create-agents.sh
```

Note: This script is a template and needs to be customized with your specific values.

## Agent Architecture

```
┌─────────────────────┐
│  User / Dashboard   │
└──────────┬──────────┘
           │
           v
┌─────────────────────┐
│  Supervisor Agent   │ ← Orchestrates workflow
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     v           v
┌─────────┐ ┌─────────┐
│Investigator│ │ Auditor │
│  Agent   │ │  Agent  │
└─────┬────┘ └────┬────┘
      │           │
      v           v
┌─────────┐ ┌─────────┐
│ Lambda  │ │Knowledge│
│ Actions │ │  Base   │
└─────────┘ └─────────┘
```

## Monitoring

View agent execution logs in CloudWatch:

```bash
aws logs tail /aws/bedrock/agents/sentinel-supervisor --follow
```

## Troubleshooting

### Agent returns empty responses
- Check CloudWatch logs for errors
- Verify IAM permissions are correct
- Ensure Knowledge Base sync completed
- Test Lambda function independently

### "Model access not enabled" error
- Go to Bedrock Console → Model access
- Request access to Claude 3.5 Sonnet
- Wait for approval (usually instant for supported regions)

### Knowledge Base not finding relevant content
- Check S3 bucket has documents in correct path
- Verify Knowledge Base sync status
- Try manual sync in console
- Check embedding model is appropriate for content

### Lambda timeout errors
- Increase timeout in Lambda configuration
- Optimize Lambda code for faster execution
- Add retry logic in Action Group

## Cost Optimization

- Use agent aliases to manage versions
- Set appropriate session TTL (default 600s)
- Monitor token usage in CloudWatch
- Use cheaper embedding models if quality is sufficient

## Next Steps

After setting up agents:
1. Test the complete workflow end-to-end
2. Update the Streamlit dashboard to use real agents
3. Add error handling and retry logic
4. Implement caching for frequently-audited suppliers
5. Set up monitoring and alerting

## Resources

- [AWS Bedrock Agents Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [Knowledge Bases Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Multi-Agent Collaboration](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-multi-agent-collaboration.html)
