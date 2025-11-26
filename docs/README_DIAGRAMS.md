# 📊 Sentinel - AI Ethics Auditor for Supply Chain
## Diagrams Documentation

This directory contains comprehensive visual documentation of the Sentinel system architecture and processes.

## 📁 Available Diagrams

### 1a. **Simple Architecture Diagram** (`architecture_diagram_simple.mermaid`)
**Purpose**: High-level overview of the core system architecture.

**Shows**:
- User interaction with Streamlit Dashboard
- Three main agents (Supervisor, Investigator, Auditor)
- External data sources and Knowledge Base
- Simple workflow between components

**Use Case**: Quick understanding of the system, presentation slides, executive overview.

---

### 1b. **Detailed Architecture Diagram** (`architecture_diagram.mermaid`)
**Purpose**: Comprehensive system architecture showing all components and their relationships.

**Shows**:
- User interface layer (Streamlit Dashboard)
- AWS Bedrock multi-agent system (Supervisor, Investigator, Auditor)
- Knowledge Base with RAG engine
- Lambda action groups
- External data sources
- Data storage layer

**Use Case**: Understanding the overall system structure, technology stack, and component interactions.

---

### 2. **Audit Process Flow** (`audit_process_flow.mermaid`)
**Purpose**: Step-by-step sequence diagram of a complete audit workflow.

**Shows**:
- User interaction flow
- Agent orchestration sequence
- Intelligence gathering process
- Policy evaluation steps
- Report generation workflow

**Use Case**: Understanding how an audit request flows through the system from start to finish.

---

### 3. **Data Flow Diagram** (`data_flow_diagram.mermaid`)
**Purpose**: Tracks how data transforms as it moves through the system.

**Shows**:
- Input layer (supplier name, policy documents)
- Processing phases (Investigation → Analysis → Synthesis)
- Output layer (reports, dashboards, evidence)
- Data stores and caching

**Use Case**: Understanding data transformations and where data is stored/processed.

---

### 4. **Deployment Diagram** (`deployment_diagram.mermaid`)
**Purpose**: Infrastructure and deployment architecture on AWS.

**Shows**:
- AWS services used (EC2, Lambda, Bedrock, S3, etc.)
- Network topology (VPC, security groups)
- External service integrations
- Monitoring and logging setup

**Use Case**: DevOps, infrastructure planning, and deployment strategies.

---

### 5. **Agent Interaction Diagram** (`agent_interaction_diagram.mermaid`)
**Purpose**: State machine showing internal agent behavior and communication.

**Shows**:
- Supervisor agent orchestration logic
- Investigator agent search phases
- Auditor agent evaluation loop
- State transitions and decision points

**Use Case**: Understanding agent-level implementation details and state management.

---

### 6. **Use Case Diagram** (`../specs/use_case_diagram.mermaid`)
**Purpose**: User-centric view of system functionality.

**Shows**:
- Actor interactions (Procurement Officer)
- System use cases
- External system relationships

**Use Case**: Functional requirements and user stories.

---

## 🎨 Viewing the Diagrams

### Option 1: VS Code (Recommended)
1. Install the **Mermaid Preview** extension
2. Open any `.mermaid` file
3. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac) to preview

### Option 2: GitHub
- GitHub automatically renders Mermaid diagrams in Markdown files
- View the diagrams directly in the repository

### Option 3: Online Mermaid Editor
1. Visit [mermaid.live](https://mermaid.live)
2. Copy the content of any `.mermaid` file
3. Paste into the editor for interactive viewing

### Option 4: Generate Images
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Generate PNG images
mmdc -i architecture_diagram.mermaid -o architecture_diagram.png
mmdc -i audit_process_flow.mermaid -o audit_process_flow.png
mmdc -i data_flow_diagram.mermaid -o data_flow_diagram.png
mmdc -i deployment_diagram.mermaid -o deployment_diagram.png
mmdc -i agent_interaction_diagram.mermaid -o agent_interaction_diagram.png
```

---

## 📖 Diagram Relationships

```
Use Case Diagram (What users do)
         ↓
Architecture Diagram (How it's built)
         ↓
Audit Process Flow (How it works)
         ↓
Agent Interaction (Agent-level details)
         ↓
Data Flow Diagram (Data transformations)
         ↓
Deployment Diagram (Infrastructure)
```

---

## 🔄 Update Guidelines

When making system changes, update the relevant diagrams:

| Change Type | Update These Diagrams |
|-------------|----------------------|
| New agent/component | Architecture, Agent Interaction |
| New workflow step | Audit Process Flow, Data Flow |
| Infrastructure change | Deployment Diagram |
| New user feature | Use Case Diagram |
| Data structure change | Data Flow Diagram |

---

## 🎯 Quick Reference

**For Developers**: Start with Architecture → Agent Interaction → Data Flow  
**For Product Managers**: Start with Use Case → Audit Process Flow  
**For DevOps**: Start with Deployment → Architecture  
**For Stakeholders**: Start with Architecture → Audit Process Flow  

---

## 📝 Diagram Conventions

### Color Coding
- 🔵 Blue (`#e1f5ff`) - Supervisor/Orchestration
- 🟡 Yellow (`#fff4e1`) - Investigation/Search
- 🔴 Red (`#ffe1e1`) - Audit/Compliance
- 🟢 Green (`#e1ffe1`) - Knowledge/Data
- 🟣 Purple (`#f0e1ff`) - User Interface

### Icons
- 👤 User/Actor
- 🧠 Supervisor Agent
- 🕵️ Investigator Agent
- ⚖️ Auditor Agent
- 📊 Dashboard/Visualization
- 📚 Knowledge Base
- ⚡ Lambda/Action
- 🌐 External Service
- 💾 Storage

---

## 📚 Related Documentation

- **[PRD.md](../specs/PRD.md)** - Product requirements
- **[SPECIFICATION.md](../specs/SPECIFICATION.md)** - Technical specifications
- **[README.md](../README.md)** - Project overview
- **[PRESENTATION.md](./PRESENTATION.md)** - Hackathon presentation

---

**Last Updated**: 2025-11-26  
**Version**: 1.0  
**Author**: Shailendra Singh Chauhan
