"""
Streamlit Dashboard for EthosChain Supplier Auditing.

Reference: PRD_Version2.md - Functional Requirements FR-01 to FR-04
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.supervisor import SupervisorAgent
from agents.investigator import InvestigatorAgent
from agents.auditor import AuditorAgent


def init_agents():
    """Initialize the multi-agent system."""
    investigator = InvestigatorAgent()
    auditor = AuditorAgent()
    supervisor = SupervisorAgent(investigator, auditor)
    return supervisor


def display_risk_indicator(risk_level: str):
    """
    Display traffic light risk indicator.
    
    Reference: PRD_Version2.md - FR-02: Traffic Light Risk Score
    """
    colors = {
        "GREEN": "🟢",
        "YELLOW": "🟡",
        "RED": "🔴"
    }
    
    color_codes = {
        "GREEN": "#28a745",
        "YELLOW": "#ffc107",
        "RED": "#dc3545"
    }
    
    icon = colors.get(risk_level, "⚪")
    color = color_codes.get(risk_level, "#6c757d")
    
    st.markdown(
        f"""
        <div style="text-align: center; padding: 20px;">
            <h1>{icon} {risk_level}</h1>
            <p style="color: {color}; font-size: 20px; font-weight: bold;">
                Overall Risk Level
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_risk_scores(risk_scores: dict):
    """
    Display risk scores across categories.
    
    Reference: PRD_Version2.md - FR-04: Risk Visualization
    """
    st.subheader("📊 Risk Breakdown by Category")
    
    cols = st.columns(3)
    categories = ["Labor", "Environment", "Governance"]
    icons = ["👷", "🌍", "⚖️"]
    
    for col, category, icon in zip(cols, categories, icons):
        score = risk_scores.get(category, 0)
        
        # Determine color based on score
        if score >= 70:
            color = "red"
        elif score >= 30:
            color = "orange"
        else:
            color = "green"
        
        col.metric(
            label=f"{icon} {category}",
            value=f"{score}/100",
            delta=None
        )
        col.progress(score / 100)


def display_findings(findings: list):
    """
    Display evidence-based findings.
    
    Reference: PRD_Version2.md - FR-03: Evidence Listing
    """
    if not findings:
        st.info("No findings to display.")
        return
    
    st.subheader("🔍 Evidence & Findings")
    
    for idx, finding in enumerate(findings, 1):
        with st.expander(f"Finding #{idx}: {finding.get('source', 'Unknown Source')}"):
            st.markdown(f"**Date:** {finding.get('date', 'N/A')}")
            st.markdown(f"**Category:** {finding.get('category', 'N/A')}")
            st.markdown(f"**Source:** [{finding.get('source', 'N/A')}]({finding.get('url', '#')})")
            st.markdown(f"**Details:** {finding.get('snippet', 'No details available')}")


def display_violations(violations: list):
    """Display policy violations with severity."""
    if not violations:
        st.success("✅ No policy violations detected!")
        return
    
    st.subheader("⚠️ Policy Violations")
    
    for violation in violations:
        severity = violation.get("severity", "UNKNOWN")
        finding = violation.get("finding", {})
        
        severity_colors = {
            "MINOR": "🟡",
            "MAJOR": "🟠",
            "CRITICAL": "🔴"
        }
        
        icon = severity_colors.get(severity, "⚪")
        
        st.warning(f"{icon} **{severity}** - {finding.get('snippet', 'No details')}")
        st.caption(f"Policy Reference: {violation.get('policy_reference', 'N/A')}")
        st.caption(f"Evidence Type: {violation.get('evidence_type', 'N/A')}")


def display_recommendations(recommendations: list):
    """Display actionable recommendations."""
    st.subheader("💡 Recommendations")
    
    for idx, rec in enumerate(recommendations, 1):
        st.markdown(f"{idx}. {rec}")


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="EthosChain - Supplier Ethics Auditor",
        page_icon="🌍",
        layout="wide"
    )
    
    st.title("🌍 EthosChain: AI Supply Chain Ethics Watchdog")
    st.markdown("*Automated supplier vetting powered by AWS Bedrock Agents*")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.info("**Oslo GenAI Hackathon 2025**\n\nTeam:\n- Atif (Lead Architect)\n- Naresh (Tech Lead)\n- Shailendra (Chief Engineer)")
    
    # Main content
    st.markdown("---")
    
    # Input section - FR-01: User input for supplier name
    supplier_name = st.text_input(
        "Enter Supplier Name to Audit",
        placeholder="e.g., Acme Corporation"
    )
    
    if st.button("🔍 Run Audit", type="primary"):
        if not supplier_name:
            st.error("Please enter a supplier name.")
            return
        
        with st.spinner(f"Auditing {supplier_name}... This may take up to 30 seconds."):
            try:
                # Initialize agents
                supervisor = init_agents()
                
                # Run audit
                report = supervisor.audit_supplier(supplier_name)
                
                # Display results
                st.success(f"✅ Audit completed for **{supplier_name}**")
                
                # FR-02: Traffic Light Display
                display_risk_indicator(report.get("overall_risk", "UNKNOWN"))
                
                st.markdown("---")
                
                # FR-04: Risk Visualization
                display_risk_scores(report.get("risk_scores", {}))
                
                st.markdown("---")
                
                # FR-03: Evidence Listing
                col1, col2 = st.columns(2)
                
                with col1:
                    display_findings(report.get("findings", []))
                
                with col2:
                    display_violations(report.get("violations", []))
                
                st.markdown("---")
                
                display_recommendations(report.get("recommendations", []))
                
                # Show raw JSON for debugging
                with st.expander("📄 View Raw JSON Report"):
                    st.json(report)
                
            except Exception as e:
                st.error(f"Error during audit: {str(e)}")


if __name__ == "__main__":
    main()
