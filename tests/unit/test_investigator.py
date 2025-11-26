"""
Unit tests for InvestigatorAgent.

Tests the news search and finding extraction logic.
"""

import pytest
from src.agents.investigator import InvestigatorAgent


class TestInvestigatorAgent:
    """Test cases for Investigator Agent."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.investigator = InvestigatorAgent()
    
    def test_initialization(self):
        """Test investigator agent initializes correctly."""
        assert self.investigator is not None
        assert self.investigator.news_api is None  # Default
    
    def test_initialization_with_api_client(self):
        """Test initialization with custom API client."""
        mock_api = object()
        investigator = InvestigatorAgent(news_api_client=mock_api)
        assert investigator.news_api is mock_api
    
    def test_search_supplier_news_returns_dict(self):
        """Test search returns proper dictionary structure."""
        supplier_name = "Acme Corp"
        result = self.investigator.search_supplier_news(supplier_name)
        
        assert isinstance(result, dict)
        assert "supplier" in result
        assert "findings" in result
        assert result["supplier"] == supplier_name
    
    def test_search_supplier_news_findings_structure(self):
        """Test that findings have required fields."""
        result = self.investigator.search_supplier_news("Test Corp")
        findings = result["findings"]
        
        assert isinstance(findings, list)
        
        if len(findings) > 0:
            finding = findings[0]
            required_fields = ["date", "source", "snippet", "category", "url"]
            
            for field in required_fields:
                assert field in finding, f"Missing required field: {field}"
    
    def test_mock_search_returns_multiple_findings(self):
        """Test mock search returns multiple findings."""
        findings = self.investigator._mock_search("Sample Corp")
        
        assert isinstance(findings, list)
        assert len(findings) > 0
        assert len(findings) <= 10  # Reasonable limit
    
    def test_mock_search_includes_supplier_name(self):
        """Test mock data includes supplier name in findings."""
        supplier_name = "Unique Corp Name"
        findings = self.investigator._mock_search(supplier_name)
        
        # At least one finding should mention the supplier
        found_mention = False
        for finding in findings:
            if supplier_name in finding["snippet"]:
                found_mention = True
                break
        
        assert found_mention, "Supplier name not found in findings"
    
    def test_findings_have_valid_categories(self):
        """Test that findings use valid categories."""
        valid_categories = {"Labor", "Environment", "Governance"}
        
        result = self.investigator.search_supplier_news("Test Corp")
        
        for finding in result["findings"]:
            assert finding["category"] in valid_categories, \
                f"Invalid category: {finding['category']}"
    
    def test_findings_have_valid_dates(self):
        """Test that findings have properly formatted dates."""
        import re
        date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        
        result = self.investigator.search_supplier_news("Test Corp")
        
        for finding in result["findings"]:
            assert date_pattern.match(finding["date"]), \
                f"Invalid date format: {finding['date']}"
    
    def test_findings_have_valid_urls(self):
        """Test that findings have URL-like strings."""
        result = self.investigator.search_supplier_news("Test Corp")
        
        for finding in result["findings"]:
            assert finding["url"].startswith("http"), \
                f"Invalid URL: {finding['url']}"
    
    def test_empty_supplier_name(self):
        """Test behavior with empty supplier name."""
        result = self.investigator.search_supplier_news("")
        
        # Should still return valid structure
        assert isinstance(result, dict)
        assert "findings" in result
    
    def test_special_characters_in_supplier_name(self):
        """Test handling of special characters in supplier names."""
        special_names = [
            "Corp & Co.",
            "Test-Corp",
            "Corp's Inc.",
            "Corp (Holdings)"
        ]
        
        for name in special_names:
            result = self.investigator.search_supplier_news(name)
            assert result["supplier"] == name
            assert isinstance(result["findings"], list)
