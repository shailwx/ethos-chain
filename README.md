# 🌍 Sentinel
## AI Ethics Auditor for Supply Chain

> **Oslo GenAI Hackathon 2025**  
> *Business Innovation & Social Impact Track*

## 🎯 Overview

Sentinel is an intelligent multi-agent system that automates ethical compliance monitoring of suppliers in global supply chains. Built with AWS Bedrock Agents, it helps procurement teams identify labor rights violations, environmental risks, and governance issues in real-time—moving beyond manual research to AI-powered, evidence-based auditing.

### **The Problem**
Procurement teams struggle to manually vet thousands of suppliers for ethical violations. This leads to:
- **Slow, error-prone research** - Hours spent per supplier
- **Missed violations** - Critical news buried in local/obscure reports  
- **Reputational risk** - Non-compliance with regulations like the EU Supply Chain Act
- **Reactive responses** - Issues discovered only after damage is done

### **Our Solution**
A **multi-agent system** that combines AI reasoning with structured policy enforcement:

1. **🕵️ Investigator Agent** - Gathers intelligence from external news, NGO reports, and public data sources
2. **⚖️ Auditor Agent** - Cross-references findings against your internal "Code of Conduct" using RAG (Retrieval-Augmented Generation)
3. **🤖 Supervisor Agent** - Orchestrates the workflow and generates structured audit reports

## ✨ Key Features

- **⚡ 30-Second Audits**: Automated supplier vetting with sub-minute turnaround
- **�� Traffic Light Dashboard**: Red/Yellow/Green risk scores across Labor, Environment, and Governance
- **📊 Evidence-Based Reports**: Every flag cites specific sources with dates and severity scores
- **🎯 Policy-Driven**: RAG-powered compliance checking against your internal Code of Conduct
- **🔍 Nuanced Analysis**: Distinguishes between "Allegations" and "Proven Violations"

## 🏗️ Architecture

### **The Supervisor Pattern**
```
User Query → Supervisor Agent
              ├→ Investigator Agent (External Intelligence)
              │   └→ Search News/Reports/Public Data
              ├→ Auditor Agent (Policy Enforcement)
              │   └→ Query Knowledge Base (RAG)
              └→ Generate Final JSON Report
```

### **Tech Stack**
- **AI Core**: AWS Bedrock Agents (Claude 3.5 Sonnet)
- **Knowledge Base**: AWS Bedrock Knowledge Base (RAG for policy documents)
- **Frontend**: Streamlit (Python)
- **Infrastructure**: AWS Lambda (Action Groups for custom tools)
- **Development Approach**: **Spec-Driven Development** (see `specs/SPECIFICATION.md`)

## 📋 Documentation

This project follows **spec-driven development**. All implementation is based on formal specifications:

- **[PRD.md](./specs/PRD.md)** - Product Requirements (functional/non-functional requirements, KPIs)
- **[SPECIFICATION.md](./specs/SPECIFICATION.md)** - System Specification (architecture, agent definitions, API contracts)
- **[use_case_diagram.mermaid](./specs/use_case_diagram.mermaid)** - Use Case Diagram

> ⚠️ **Development Rule**: All code changes must reference and comply with the specifications above.

## 🎯 Success Metrics (KPIs)

- **Time Saved**: 90% reduction in manual research time per supplier
- **Accuracy**: 80%+ correct identification of violations vs. human audit
- **Latency**: <30 seconds per audit
- **Reliability**: 95%+ schema-compliant JSON outputs

## 📦 Quick Start

### Prerequisites
- AWS Account with Bedrock access enabled
- Python 3.9+
- AWS CLI installed and configured
- Appropriate IAM permissions for CloudFormation, Lambda, S3, and Bedrock

### Local Development Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shailwx/ethos-chain.git
   cd ethos-chain
   ```

2. **Run Setup Script**
   ```bash
   chmod +x scripts/setup.sh
   ./scripts/setup.sh
   ```
   
   This will:
   - Create virtual environment
   - Install all dependencies
   - Create .env configuration file
   - Run initial tests

3. **Configure AWS (if not already done)**
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Key, and preferred region
   ```

4. **Run the Dashboard Locally (with mock data)**
   ```bash
   source venv/bin/activate
   streamlit run src/dashboard/app.py
   ```

### AWS Deployment

For complete AWS deployment with Bedrock Agents:

1. **Deploy Infrastructure**
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```
   
   This automated script will:
   - Deploy CloudFormation stack (S3, Lambda, IAM roles)
   - Upload policy documents to S3
   - Deploy Lambda function code
   - Create .env configuration
   
2. **Create Bedrock Knowledge Base**
   - Go to AWS Bedrock Console → Knowledge Bases
   - Create new Knowledge Base
   - Use the S3 bucket created by CloudFormation
   - Select embedding model: `amazon.titan-embed-text-v1`
   - Note the Knowledge Base ID

3. **Create Bedrock Agents**
   Follow detailed instructions in [`infrastructure/bedrock/README.md`](./infrastructure/bedrock/README.md):
   - Create Investigator Agent (with Lambda Action Group)
   - Create Auditor Agent (with Knowledge Base)
   - Create Supervisor Agent (orchestrates sub-agents)
   - Note all Agent IDs and Alias IDs

4. **Update Configuration**
   Edit `.env` file with your Agent IDs and Knowledge Base ID:
   ```bash
   SUPERVISOR_AGENT_ID=your-agent-id
   SUPERVISOR_ALIAS_ID=your-alias-id
   KNOWLEDGE_BASE_ID=your-kb-id
   # ... etc
   ```

5. **Test the Complete System**
   ```bash
   streamlit run src/dashboard/app.py
   ```

### Quick Test (Mock Data)

To test without AWS deployment:
```bash
# Ensure USE_MOCK_DATA=true in .env
streamlit run src/dashboard/app.py
```

Try these demo suppliers:
- **GreenTech Manufacturing** (Expected: GREEN risk)
- **Global Textiles Inc** (Expected: YELLOW risk)
- **QuickProd Factories** (Expected: RED risk)

5. **Run the Dashboard**
   ```bash
   streamlit run src/dashboard/app.py
   ```

## 🚧 Project Status

**Current Phase**: Ready for Deployment  
**Target**: Oslo GenAI Hackathon 2025 Demo

### ✅ Completed
- [x] Multi-agent system architecture (Supervisor, Investigator, Auditor)
- [x] Streamlit dashboard implementation with traffic light indicators
- [x] CloudFormation infrastructure templates
- [x] Lambda Action Group functions with error handling
- [x] Bedrock Agent configuration files
- [x] Knowledge Base integration setup
- [x] Unit and integration tests (90%+ coverage)
- [x] Mock data for development and demo
- [x] Automated deployment scripts
- [x] Comprehensive documentation

### 🔄 Next Steps for AWS Deployment
1. Enable Bedrock model access in AWS Console
2. Run deployment script: `./scripts/deploy.sh`
3. Create Knowledge Base in AWS Bedrock Console
4. Create three Bedrock Agents (see `infrastructure/bedrock/README.md`)
5. Update .env with Agent IDs and test end-to-end

### 🎯 Demo Ready
The system is fully functional with mock data and ready for hackathon demonstration. AWS deployment is optional but recommended for live data.

## 📚 Additional Documentation

- **[Infrastructure Setup](./infrastructure/iac/README.md)** - CloudFormation deployment guide
- **[Bedrock Agents](./infrastructure/bedrock/README.md)** - Agent creation and configuration
- **[Lambda Functions](./infrastructure/lambda/README.md)** - Action Group implementation
- **[Testing Guide](./tests/README.md)** - Running and writing tests
- **[Deployment Scripts](./scripts/README.md)** - Automation tools
- **[Demo Data](./data/sample/README.md)** - Sample scenarios for presentation

## 🧪 Testing

Run tests with different configurations:

```bash
# Run all tests
./scripts/test.sh all

# Unit tests only
./scripts/test.sh unit

# Integration tests
./scripts/test.sh integration

# With coverage report
./scripts/test.sh coverage

# Code quality checks
./scripts/test.sh lint
```

## 🐛 Troubleshooting

### Common Issues

**"Model access not enabled"**
- Go to AWS Bedrock Console → Model access
- Request access to Claude 3.5 Sonnet and Titan Embeddings
- Wait for approval (usually instant)

**Lambda timeout errors**
- Increase timeout in `infrastructure/iac/template.yaml`
- Deploy updated template

**Knowledge Base sync issues**
- Verify S3 bucket has policy documents
- Manually trigger sync in Bedrock Console
- Check CloudWatch logs for errors

**Dashboard connection errors**
- Verify Agent IDs in .env are correct
- Check AWS credentials are configured
- Ensure you're in the correct AWS region

See individual component READMEs for specific troubleshooting.

## 🤝 Contributing

This is a hackathon project. Contributions are welcome! Please:
1. Read the specifications (`specs/SPECIFICATION.md`)
2. Ensure changes align with the PRD
3. Run tests before submitting: `./scripts/test.sh all`
4. Submit PRs with clear references to spec sections

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Atif Usman** - Lead Architect / Product Owner
- **Naresh Gaddam Reddy** - Tech Lead
- **Shailendra Singh Chauhan** - Chief Engineer

**Event**: Oslo GenAI Hackathon 2025  
**Track**: Business Innovation & Social Impact

---

**Built with ❤️ for ethical supply chains**
