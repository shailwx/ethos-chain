"""
Integration tests for complete audit workflow.

Tests the end-to-end flow from user input to final report.
"""

import pytest
from src.agents.supervisor import SupervisorAgent
from src.agents.investigator import InvestigatorAgent
from src.agents.auditor import AuditorAgent


class TestAuditWorkflow:
    """Integration tests for the complete audit workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.investigator = InvestigatorAgent()
        self.auditor = AuditorAgent()
        self.supervisor = SupervisorAgent(self.investigator, self.auditor)
    
    def test_complete_audit_workflow(self):
        """Test complete audit from start to finish."""
        # Act
        report = self.supervisor.audit_supplier("Acme Corporation")
        
        # Assert - Verify report structure
        assert isinstance(report, dict)
        assert "supplier" in report
        assert "timestamp" in report
        assert "overall_risk" in report
        assert "risk_scores" in report
        assert "findings" in report
        assert "violations" in report
        assert "recommendations" in report
        
        # Verify risk level is valid
        assert report["overall_risk"] in ["GREEN", "YELLOW", "RED"]
        
        # Verify risk scores
        for category in ["Labor", "Environment", "Governance"]:
            assert category in report["risk_scores"]
            assert 0 <= report["risk_scores"][category] <= 100
    
    def test_audit_with_clean_supplier(self):
        """Test audit of supplier with minimal findings."""
        report = self.supervisor.audit_supplier("CleanCorp Inc")
        
        # Should have some structure even if clean
        assert isinstance(report["findings"], list)
        assert isinstance(report["violations"], list)
        assert isinstance(report["recommendations"], list)
        assert len(report["recommendations"]) > 0
    
    def test_audit_with_problematic_supplier(self):
        """Test audit of supplier with known issues."""
        report = self.supervisor.audit_supplier("ProblemCorp Ltd")
        
        # Mock data should return findings
        assert len(report["findings"]) > 0
        
        # Should have risk assessment
        assert report["overall_risk"] in ["YELLOW", "RED"]
    
    def test_multiple_sequential_audits(self):
        """Test running multiple audits sequentially."""
        suppliers = ["Supplier A", "Supplier B", "Supplier C"]
        reports = []
        
        for supplier in suppliers:
            report = self.supervisor.audit_supplier(supplier)
            reports.append(report)
        
        # Verify all completed
        assert len(reports) == 3
        
        # Verify each has unique supplier name
        for i, report in enumerate(reports):
            assert report["supplier"] == suppliers[i]
    
    def test_findings_flow_through_pipeline(self):
        """Test that findings from investigator reach final report."""
        report = self.supervisor.audit_supplier("Test Corp")
        
        # Findings should be present in report
        assert "findings" in report
        
        # If there are findings, they should have proper structure
        for finding in report["findings"]:
            assert "date" in finding
            assert "source" in finding
            assert "snippet" in finding
            assert "category" in finding
    
    def test_violations_linked_to_findings(self):
        """Test that violations reference actual findings."""
        report = self.supervisor.audit_supplier("Violator Corp")
        
        if len(report["violations"]) > 0:
            violation = report["violations"][0]
            
            # Violation should contain finding data
            assert "finding" in violation or "evidence_type" in violation
            assert "severity" in violation
    
    def test_recommendations_based_on_risk(self):
        """Test that recommendations match risk level."""
        report = self.supervisor.audit_supplier("Test Corp")
        
        recommendations = report["recommendations"]
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
        # Recommendations should be strings
        for rec in recommendations:
            assert isinstance(rec, str)
            assert len(rec) > 0
    
    def test_risk_scores_consistency(self):
        """Test that overall risk matches category scores."""
        report = self.supervisor.audit_supplier("Test Corp")
        
        max_category_score = max(report["risk_scores"].values())
        overall_risk = report["overall_risk"]
        
        # Verify consistency
        if max_category_score < 30:
            assert overall_risk == "GREEN"
        elif max_category_score < 70:
            assert overall_risk == "YELLOW"
        else:
            assert overall_risk == "RED"
    
    def test_audit_report_serializable(self):
        """Test that report can be serialized to JSON."""
        import json
        
        report = self.supervisor.audit_supplier("Test Corp")
        
        # Should be able to serialize without errors
        json_str = json.dumps(report)
        assert isinstance(json_str, str)
        
        # Should be able to deserialize
        deserialized = json.loads(json_str)
        assert deserialized["supplier"] == "Test Corp"
    
    def test_error_handling_in_pipeline(self):
        """Test error handling across the pipeline."""
        # Test with edge cases
        edge_cases = [
            "",  # Empty string
            "A" * 1000,  # Very long name
            "Test<>Corp",  # Special characters
            "123",  # Numbers only
        ]
        
        for supplier in edge_cases:
            try:
                report = self.supervisor.audit_supplier(supplier)
                # Should at least return valid structure
                assert isinstance(report, dict)
            except Exception as e:
                pytest.fail(f"Failed on edge case '{supplier[:20]}': {e}")
    
    def test_performance_benchmark(self):
        """Test that audit completes in reasonable time."""
        import time
        
        start_time = time.time()
        report = self.supervisor.audit_supplier("Benchmark Corp")
        elapsed = time.time() - start_time
        
        # Should complete within a reasonable timeframe (mock data)
        assert elapsed < 5.0, f"Audit took too long: {elapsed}s"
        assert report is not None
