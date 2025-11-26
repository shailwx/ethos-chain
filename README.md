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
- AWS Account with Bedrock access
- Python 3.9+
- AWS CLI configured

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/shailwx/ethos-chain.git
   cd ethos-chain
   ```

2. **Set Up Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure AWS**
   ```bash
   aws configure
   # Ensure you have access to AWS Bedrock in your region
   ```

4. **Deploy Infrastructure**
   ```bash
   # Deploy AWS Bedrock Agents and Knowledge Base
   # (Deployment scripts coming soon)
   ```

5. **Run the Dashboard**
   ```bash
   streamlit run src/dashboard/app.py
   ```

## 🚧 Project Status

**Current Phase**: Initial Development  
**Target**: Oslo GenAI Hackathon 2025 Demo

### Roadmap
- [ ] AWS Bedrock Agent setup (Supervisor, Investigator, Auditor)
- [ ] Knowledge Base integration (Code of Conduct documents)
- [ ] Lambda Action Groups for external data retrieval
- [ ] Streamlit dashboard implementation
- [ ] JSON schema validation
- [ ] Mock data for demo
- [ ] Live deployment

## 🤝 Contributing

This is a hackathon project. Contributions are welcome! Please:
1. Read the specifications (`specs/SPECIFICATION.md`)
2. Ensure changes align with the PRD
3. Submit PRs with clear references to spec sections

## 📄 License

[Add License Information]

## 👥 Team

- **Atif Usman** - Lead Architect / Product Owner
- **Naresh Gaddam Reddy** - Tech Lead
- **Shailendra Singh Chauhan** - Chief Engineer

**Event**: Oslo GenAI Hackathon 2025  
**Track**: Business Innovation & Social Impact

---

**Built with ❤️ for ethical supply chains**
