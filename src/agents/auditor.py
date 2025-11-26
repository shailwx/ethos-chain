"""
Auditor Agent - Applies internal policy to findings using RAG.

Reference: SPEC_Version2.md - Section 2: Agent Definitions
"""

from typing import Dict, Any, List


class AuditorAgent:
    """
    Auditor Agent focuses purely on policy logic and compliance checking.
    
    Responsibilities:
    - Take list of facts from Investigator
    - Query Knowledge Base: "Does [Fact X] violate our policy?"
    - Assign severity scores (Minor/Major/Critical)
    
    Tools: AWS Bedrock Knowledge Base (RAG)
    """
    
    def __init__(self, knowledge_base_client=None):
        """
        Initialize the Auditor Agent.
        
        Args:
            knowledge_base_client: AWS Bedrock Knowledge Base client
        """
        self.kb_client = knowledge_base_client
    
    def evaluate_findings(self, findings_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate findings against the internal Code of Conduct.
        
        Args:
            findings_data: Output from InvestigatorAgent containing findings
            
        Returns:
            Dict containing risk scores and violation details
            
        Reference: SPEC_Version2.md - Section 2: Auditor Agent
        
        Output includes:
        - overall_risk: "GREEN" | "YELLOW" | "RED"
        - risk_scores: {"Labor": score, "Environment": score, "Governance": score}
        - violations: List of violations with severity
        - recommendations: Suggested actions
        """
        findings = findings_data.get("findings", [])
        
        violations = []
        risk_scores = {"Labor": 0, "Environment": 0, "Governance": 0}
        
        for finding in findings:
            violation = self._check_against_policy(finding)
            if violation:
                violations.append(violation)
                # Update risk scores based on category and severity
                category = finding.get("category", "Governance")
                severity_points = self._get_severity_points(violation["severity"])
                risk_scores[category] = max(risk_scores[category], severity_points)
        
        overall_risk = self._calculate_overall_risk(risk_scores)
        recommendations = self._generate_recommendations(violations)
        
        return {
            "overall_risk": overall_risk,
            "risk_scores": risk_scores,
            "violations": violations,
            "recommendations": recommendations
        }
    
    def _check_against_policy(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check a single finding against the policy using Knowledge Base.
        
        TODO: Integrate with AWS Bedrock Knowledge Base
        
        Returns:
            Dict with violation details or None if no violation
        """
        # TODO: Replace with actual RAG query to Knowledge Base
        # For now, mock the policy check
        
        snippet = finding.get("snippet", "").lower()
        
        # Positive findings - no violation
        if any(word in snippet for word in ['award', 'certification', 'certified', 'maintains', 'receives']):
            return None
        
        # Critical violations
        if any(phrase in snippet for phrase in ['critical', 'severe', '$3m', 'hazardous', 'lawsuit', 'abuses']):
            severity = "CRITICAL"
            policy_ref = "Section 2.1: Critical Violations - Zero Tolerance"
        # Major violations
        elif any(word in snippet for word in ['fined', 'violation', 'investigation', 'contamination']):
            severity = "MAJOR"
            policy_ref = "Section 3.2: Environmental and Labor Standards"
        # Minor concerns
        elif any(word in snippet for word in ['concerns', 'questions', 'allegations', 'accused', 'report']):
            severity = "MINOR"
            policy_ref = "Section 4.1: Monitoring and Improvement"
        # No violation found
        else:
            return None
        
        return {
            "finding": finding,
            "severity": severity,  # "MINOR" | "MAJOR" | "CRITICAL"
            "policy_reference": policy_ref,
            "evidence_type": "PROVEN" if any(word in snippet for word in ['fined', 'found', 'confirmed']) else "ALLEGATION"
        }
    
    def _get_severity_points(self, severity: str) -> int:
        """Convert severity to numeric points for risk scoring."""
        severity_map = {
            "MINOR": 30,
            "MAJOR": 70,
            "CRITICAL": 100
        }
        return severity_map.get(severity, 0)
    
    def _calculate_overall_risk(self, risk_scores: Dict[str, int]) -> str:
        """
        Calculate overall risk level based on category scores.
        
        Returns: "GREEN" | "YELLOW" | "RED"
        Reference: PRD_Version2.md - FR-02: Traffic Light Risk Score
        """
        max_score = max(risk_scores.values())
        
        if max_score >= 70:
            return "RED"
        elif max_score >= 30:
            return "YELLOW"
        else:
            return "GREEN"
    
    def _generate_recommendations(self, violations: List[Dict[str, Any]]) -> List[str]:
        """Generate actionable recommendations based on violations."""
        if not violations:
            return ["No immediate action required. Continue monitoring."]
        
        recommendations = []
        
        # Check for critical violations
        critical = [v for v in violations if v["severity"] == "CRITICAL"]
        if critical:
            recommendations.append("URGENT: Conduct immediate audit of supplier operations")
        
        # Check for proven violations
        proven = [v for v in violations if v["evidence_type"] == "PROVEN"]
        if proven:
            recommendations.append("Request supplier remediation plan with timeline")
        
        recommendations.append("Schedule follow-up review in 30 days")
        
        return recommendations
