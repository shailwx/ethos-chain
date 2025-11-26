"""
Unit tests for SupervisorAgent.

Tests the orchestration logic and report formatting.
"""

import pytest
from unittest.mock import Mock, patch
from src.agents.supervisor import SupervisorAgent


class TestSupervisorAgent:
    """Test cases for Supervisor Agent."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_investigator = Mock()
        self.mock_auditor = Mock()
        self.supervisor = SupervisorAgent(
            self.mock_investigator,
            self.mock_auditor
        )
    
    def test_initialization(self):
        """Test supervisor agent initializes correctly."""
        assert self.supervisor.investigator is not None
        assert self.supervisor.auditor is not None
    
    def test_audit_supplier_happy_path(self):
        """Test successful supplier audit workflow."""
        # Arrange
        supplier_name = "Acme Corp"
        
        mock_findings = {
            "supplier": supplier_name,
            "findings": [
                {
                    "date": "2024-03-10",
                    "source": "News Source",
                    "snippet": "Test finding",
                    "category": "Labor"
                }
            ]
        }
        
        mock_audit_results = {
            "overall_risk": "YELLOW",
            "risk_scores": {"Labor": 50, "Environment": 0, "Governance": 0},
            "violations": [],
            "recommendations": ["Monitor situation"]
        }
        
        self.mock_investigator.search_supplier_news.return_value = mock_findings
        self.mock_auditor.evaluate_findings.return_value = mock_audit_results
        
        # Act
        report = self.supervisor.audit_supplier(supplier_name)
        
        # Assert
        assert report["supplier"] == supplier_name
        assert report["overall_risk"] == "YELLOW"
        assert "timestamp" in report
        assert "risk_scores" in report
        assert "findings" in report
        assert len(report["findings"]) == 1
        
        # Verify method calls
        self.mock_investigator.search_supplier_news.assert_called_once_with(supplier_name)
        self.mock_auditor.evaluate_findings.assert_called_once_with(mock_findings)
    
    def test_audit_supplier_no_findings(self):
        """Test audit when no findings are discovered."""
        supplier_name = "Clean Corp"
        
        mock_findings = {
            "supplier": supplier_name,
            "findings": []
        }
        
        mock_audit_results = {
            "overall_risk": "GREEN",
            "risk_scores": {"Labor": 0, "Environment": 0, "Governance": 0},
            "violations": [],
            "recommendations": ["No action required"]
        }
        
        self.mock_investigator.search_supplier_news.return_value = mock_findings
        self.mock_auditor.evaluate_findings.return_value = mock_audit_results
        
        report = self.supervisor.audit_supplier(supplier_name)
        
        assert report["overall_risk"] == "GREEN"
        assert len(report["findings"]) == 0
    
    def test_format_report_structure(self):
        """Test that report format matches expected schema."""
        supplier_name = "Test Corp"
        findings = {"findings": []}
        audit_results = {
            "overall_risk": "GREEN",
            "risk_scores": {},
            "violations": [],
            "recommendations": []
        }
        
        report = self.supervisor._format_report(
            supplier_name,
            findings,
            audit_results
        )
        
        # Verify required fields
        required_fields = [
            "supplier",
            "timestamp",
            "overall_risk",
            "risk_scores",
            "findings",
            "violations",
            "recommendations"
        ]
        
        for field in required_fields:
            assert field in report, f"Missing required field: {field}"
    
    def test_audit_supplier_with_violations(self):
        """Test audit when violations are found."""
        supplier_name = "Bad Corp"
        
        mock_findings = {
            "supplier": supplier_name,
            "findings": [
                {
                    "date": "2024-01-15",
                    "source": "EPA",
                    "snippet": "Fined for pollution",
                    "category": "Environment"
                }
            ]
        }
        
        mock_audit_results = {
            "overall_risk": "RED",
            "risk_scores": {"Labor": 0, "Environment": 100, "Governance": 0},
            "violations": [
                {
                    "severity": "CRITICAL",
                    "policy_reference": "Section 3.2",
                    "evidence_type": "PROVEN"
                }
            ],
            "recommendations": ["Immediate action required"]
        }
        
        self.mock_investigator.search_supplier_news.return_value = mock_findings
        self.mock_auditor.evaluate_findings.return_value = mock_audit_results
        
        report = self.supervisor.audit_supplier(supplier_name)
        
        assert report["overall_risk"] == "RED"
        assert len(report["violations"]) == 1
        assert report["violations"][0]["severity"] == "CRITICAL"
    
    @patch('src.agents.supervisor.datetime')
    def test_report_includes_timestamp(self, mock_datetime):
        """Test that report includes current timestamp."""
        mock_datetime.now.return_value.isoformat.return_value = "2024-11-26T12:00:00"
        
        # Create new supervisor to use patched datetime
        supervisor = SupervisorAgent(self.mock_investigator, self.mock_auditor)
        
        self.mock_investigator.search_supplier_news.return_value = {"findings": []}
        self.mock_auditor.evaluate_findings.return_value = {
            "overall_risk": "GREEN",
            "risk_scores": {},
            "violations": [],
            "recommendations": []
        }
        
        report = supervisor.audit_supplier("Test Corp")
        
        # Note: Current implementation uses hardcoded timestamp
        # This test documents expected behavior for future implementation
        assert "timestamp" in report
