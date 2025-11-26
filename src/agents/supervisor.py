"""
Supervisor Agent - Orchestrates the multi-agent audit workflow.

Reference: SPEC_Version2.md - Section 2: Agent Definitions
"""

import json
from typing import Dict, Any


class SupervisorAgent:
    """
    Supervisor Agent coordinates the audit process by delegating work to
    the Investigator and Auditor agents, then formats the final report.
    
    Responsibilities:
    1. Receive user query (e.g., "Audit Acme Corp")
    2. Call Investigator to get raw data
    3. Call Auditor with that data to get compliance score
    4. Format final JSON for UI rendering
    """
    
    def __init__(self, investigator_agent, auditor_agent):
        """
        Initialize the Supervisor Agent.
        
        Args:
            investigator_agent: Instance of InvestigatorAgent
            auditor_agent: Instance of AuditorAgent
        """
        self.investigator = investigator_agent
        self.auditor = auditor_agent
    
    def audit_supplier(self, supplier_name: str) -> Dict[str, Any]:
        """
        Orchestrate the complete supplier audit workflow.
        
        Args:
            supplier_name: Name of the supplier to audit
            
        Returns:
            Dict containing the complete audit report in JSON format
            
        Reference: SPEC_Version2.md - Section 3: API Contracts
        """
        # Step 1: Gather intelligence
        findings = self.investigator.search_supplier_news(supplier_name)
        
        # Step 2: Audit against policy
        audit_results = self.auditor.evaluate_findings(findings)
        
        # Step 3: Format final report
        report = self._format_report(supplier_name, findings, audit_results)
        
        return report
    
    def _format_report(
        self, 
        supplier_name: str, 
        findings: Dict[str, Any], 
        audit_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Format the final JSON report for UI consumption.
        
        Returns structured JSON with risk scores and evidence.
        Reference: SPEC_Version2.md - Section 3: API Contracts
        """
        return {
            "supplier": supplier_name,
            "timestamp": "2025-11-26T00:00:00Z",  # TODO: Use actual timestamp
            "overall_risk": audit_results.get("overall_risk", "UNKNOWN"),
            "risk_scores": audit_results.get("risk_scores", {}),
            "findings": findings.get("findings", []),
            "violations": audit_results.get("violations", []),
            "recommendations": audit_results.get("recommendations", [])
        }
