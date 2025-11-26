# 📚 Sentinel Documentation

Welcome to the comprehensive documentation for **Sentinel** - an AI Ethics Auditor for Supply Chain compliance using AWS Bedrock Agents.

---

## 📑 Table of Contents

### 🎯 Quick Start
- [Main README](../README.md) - Project overview and setup instructions
- [Pitch Guide](./PITCH_GUIDE.md) - 3-minute hackathon presentation script
- [Presentation Slides](./PRESENTATION.md) - Complete slide deck content

### 📋 Specifications
- [Product Requirements (PRD)](../specs/PRD.md) - Functional and non-functional requirements
- [Technical Specification](../specs/SPECIFICATION.md) - System architecture and API contracts
- [Use Case Diagram](../specs/use_case_diagram.mermaid) - User interaction flows

### 📊 Visual Documentation
- [Diagram Overview](./README_DIAGRAMS.md) - Guide to all visual documentation
- [Architecture Diagram (Simple)](./architecture_diagram_simple.mermaid) - High-level system overview
- [Architecture Diagram (Detailed)](./architecture_diagram.mermaid) - Complete system architecture
- [Audit Process Flow](./audit_process_flow.mermaid) - Step-by-step audit workflow
- [Data Flow Diagram](./data_flow_diagram.mermaid) - Data transformation pipeline
- [Deployment Diagram](./deployment_diagram.mermaid) - AWS infrastructure layout
- [Agent Interaction Diagram](./agent_interaction_diagram.mermaid) - Multi-agent state machine

---

## 🗂️ Documentation Structure

```
docs/
├── README.md                           # This file - Documentation index
├── PITCH_GUIDE.md                      # Hackathon presentation guide
├── PRESENTATION.md                     # Slide deck content
├── README_DIAGRAMS.md                  # Visual documentation guide
├── architecture_diagram_simple.mermaid # Simple architecture
├── architecture_diagram.mermaid        # Detailed architecture
├── audit_process_flow.mermaid         # Audit workflow
├── data_flow_diagram.mermaid          # Data pipeline
├── deployment_diagram.mermaid         # Infrastructure
└── agent_interaction_diagram.mermaid  # Agent states

specs/
├── PRD.md                             # Product requirements
├── SPECIFICATION.md                   # Technical spec
└── use_case_diagram.mermaid          # Use cases
```

---

## 🎯 Document Purpose Guide

### For Developers
**Start here:**
1. [Main README](../README.md) - Understand the project
2. [Technical Specification](../specs/SPECIFICATION.md) - Implementation details
3. [Architecture Diagram](./architecture_diagram.mermaid) - System design
4. [Agent Interaction Diagram](./agent_interaction_diagram.mermaid) - Agent behavior

**Key principle:** All code must reference and comply with the specifications.

### For Product Managers
**Start here:**
1. [Product Requirements (PRD)](../specs/PRD.md) - Business requirements and KPIs
2. [Use Case Diagram](../specs/use_case_diagram.mermaid) - User interactions
3. [Audit Process Flow](./audit_process_flow.mermaid) - How the system works
4. [Presentation](./PRESENTATION.md) - Business value and impact

### For DevOps Engineers
**Start here:**
1. [Deployment Diagram](./deployment_diagram.mermaid) - Infrastructure setup
2. [Architecture Diagram](./architecture_diagram.mermaid) - Component relationships
3. [Technical Specification](../specs/SPECIFICATION.md) - AWS service requirements

### For Hackathon Presentation
**Start here:**
1. [Pitch Guide](./PITCH_GUIDE.md) - 3-minute script and Q&A prep
2. [Presentation Slides](./PRESENTATION.md) - Complete deck
3. Demo checklist and backup plans

### For Stakeholders
**Start here:**
1. [Main README](../README.md) - Project overview
2. [Presentation](./PRESENTATION.md) - Business value and impact
3. [Architecture Diagram (Simple)](./architecture_diagram_simple.mermaid) - High-level design

---

## 🚀 Key Concepts

### The Multi-Agent System
Sentinel uses three specialized AI agents orchestrated by AWS Bedrock:

1. **🧠 Supervisor Agent** - Orchestrates the workflow and generates final reports
2. **🕵️ Investigator Agent** - Gathers intelligence from external sources
3. **⚖️ Auditor Agent** - Evaluates findings against your Code of Conduct using RAG

### Core Technologies
- **AWS Bedrock Agents** - Multi-agent orchestration
- **Claude 3.5 Sonnet** - LLM reasoning engine
- **AWS Bedrock Knowledge Base** - RAG for policy documents
- **AWS Lambda** - Custom action groups
- **Streamlit** - Interactive dashboard

### Workflow
```
User Query → Supervisor Agent
              ├→ Investigator (External Intelligence)
              ├→ Auditor (Policy Enforcement)
              └→ Generate Risk Report (Red/Yellow/Green)
```

---

## 📖 Reading Recommendations

### New to the Project?
1. Start with [Main README](../README.md)
2. Review [Architecture Diagram (Simple)](./architecture_diagram_simple.mermaid)
3. Watch the demo flow in [Audit Process Flow](./audit_process_flow.mermaid)
4. Deep dive into [Technical Specification](../specs/SPECIFICATION.md)

### Building Features?
1. Check [PRD.md](../specs/PRD.md) for requirements
2. Review [SPECIFICATION.md](../specs/SPECIFICATION.md) for implementation details
3. Reference [Agent Interaction Diagram](./agent_interaction_diagram.mermaid)
4. Follow the spec-driven development approach

### Preparing for Demo?
1. Study [Pitch Guide](./PITCH_GUIDE.md) thoroughly
2. Review [Presentation](./PRESENTATION.md) slides
3. Practice with the demo checklist
4. Prepare for Q&A scenarios

### Deploying Infrastructure?
1. Study [Deployment Diagram](./deployment_diagram.mermaid)
2. Follow AWS Bedrock setup in [Technical Specification](../specs/SPECIFICATION.md)
3. Check infrastructure requirements in [Main README](../README.md)

---

## 🔄 Viewing Diagrams

### VS Code (Recommended)
1. Install **Mermaid Preview** extension
2. Open any `.mermaid` file
3. Press `Ctrl+Shift+V` (or `Cmd+Shift+V` on Mac)

### GitHub
- Diagrams render automatically in GitHub's Markdown viewer

### Online Editor
1. Visit [mermaid.live](https://mermaid.live)
2. Copy diagram content
3. Paste for interactive viewing

### Generate Images
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i architecture_diagram.mermaid -o architecture_diagram.png
```

See [README_DIAGRAMS.md](./README_DIAGRAMS.md) for detailed instructions.

---

## 📊 Success Metrics (KPIs)

As defined in the [PRD](../specs/PRD.md):

- **Time Saved**: 90% reduction in manual research per supplier
- **Accuracy**: 80%+ correct identification vs. human audit
- **Latency**: <30 seconds per audit
- **Reliability**: 95%+ schema-compliant JSON outputs

---

## 🎯 Development Approach

This project follows **Spec-Driven Development**:

1. ✅ Requirements defined in [PRD.md](../specs/PRD.md)
2. ✅ System design in [SPECIFICATION.md](../specs/SPECIFICATION.md)
3. ✅ Visual documentation in diagrams
4. ✅ Implementation follows specs
5. ✅ All changes reference spec sections

**Rule**: No code changes without specification compliance.

---

## 🤝 Contributing

When contributing to documentation:

1. **Update diagrams** when architecture changes
2. **Keep specs in sync** with implementation
3. **Update this README** when adding new docs
4. **Follow conventions** in [README_DIAGRAMS.md](./README_DIAGRAMS.md)

### Diagram Update Guidelines

| Change Type | Update These Files |
|-------------|-------------------|
| New agent/component | Architecture diagrams, Agent interaction |
| New workflow step | Audit process flow, Data flow |
| Infrastructure change | Deployment diagram |
| New user feature | Use case diagram, PRD |
| Policy/requirement change | PRD, Specification |

---

## 📞 Support & Questions

**For hackathon participants:**
- Review [Pitch Guide](./PITCH_GUIDE.md) for presentation tips
- Check [Presentation](./PRESENTATION.md) for content
- Use [Technical Specification](../specs/SPECIFICATION.md) for Q&A prep

**For developers:**
- Start with [Main README](../README.md)
- Deep dive into [SPECIFICATION.md](../specs/SPECIFICATION.md)
- Reference diagrams in this folder

**For stakeholders:**
- Executive overview in [Main README](../README.md)
- Business case in [Presentation](./PRESENTATION.md)
- Requirements in [PRD](../specs/PRD.md)

---

## 📅 Project Information

- **Project**: Sentinel - AI Ethics Auditor for Supply Chain
- **Event**: Oslo GenAI Hackathon 2025
- **Track**: Business Innovation & Social Impact
- **Repository**: [github.com/shailwx/ethos-chain](https://github.com/shailwx/ethos-chain)

### Team
- **Atif Usman** - Lead Architect / Product Owner
- **Naresh Gaddam Reddy** - Tech Lead
- **Shailendra Singh Chauhan** - Chief Engineer

---

## 🔗 External Resources

- [AWS Bedrock Agents Documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents.html)
- [AWS Bedrock Knowledge Bases](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html)
- [Anthropic Claude 3.5 Sonnet](https://www.anthropic.com/claude)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Mermaid Diagram Syntax](https://mermaid.js.org/)

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-26 | Initial documentation structure |

---

**Built with ❤️ for ethical supply chains**

---

*Last Updated: November 26, 2025*
