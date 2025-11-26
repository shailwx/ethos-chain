# Product Requirement Document (PRD)
**Project Name:** Sentinel - AI Ethics Auditor for Supply Chain  
**Version:** 1.0  
**Date:** 2025-11-26  
**Author:** Shailendra Singh Chauhan

## 1. Executive Summary
Sentinel is an AI-powered supply chain auditor designed to automate the vetting of suppliers against corporate ethical standards. By leveraging AWS Bedrock Agents, it moves beyond simple keyword matching to reason about complex violations in labor rights and environmental sustainability.

## 2. Problem Statement
Procurement teams struggle to monitor thousands of suppliers. Manual vetting is slow, error-prone, and often misses critical news buried in local reports, leading to reputational risk and non-compliance with laws like the EU Supply Chain Act.

## 3. Solution Overview
A multi-agent system where:
- An **Investigator Agent** gathers intelligence.
- An **Auditor Agent** cross-references findings with an internal "Code of Conduct" (Knowledge Base).
- A **Supervisor Agent** orchestrates the workflow and updates a real-time dashboard.

## 4. Functional Requirements

### 4.1 User Interface (Streamlit)
- **FR-01**: Users must be able to input a supplier name for audit.
- **FR-02**: System must display a "Traffic Light" risk score (Red/Yellow/Green).
- **FR-03**: System must list specific evidence (sources) for every flag.
- **FR-04**: System must visualize risk across categories (Labor, Environment, Ethics).

### 4.2 AI Backend (AWS Bedrock)
- **FR-05**: The system must utilize a Knowledge Base containing the "Supplier Code of Conduct".
- **FR-06**: The system must return data in a structured JSON format for UI rendering.
- **FR-07**: The Agent must be able to distinguish between "Allegations" and "Proven Violations".

## 5. Non-Functional Requirements
- **NFR-01 (Latency)**: Audit results should be generated within 30 seconds.
- **NFR-02 (Reliability)**: The JSON output must be schema-compliant 95% of the time.
- **NFR-03 (Security)**: No proprietary supplier data should be trained into the public model.

## 7. Success Metrics (KPIs)
- **Time Saved**: Reduction in manual research time per supplier (Target: 90%).
- **Accuracy**: Percentage of correctly identified violations compared to human audit (Target: 80%).