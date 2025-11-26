# Sample Supplier Data

This directory contains sample data for testing and demonstration.

## Files

- `suppliers.json` - Sample supplier information
- `mock_findings.json` - Mock news findings for testing
- `demo_scenarios.json` - Demo scenarios for hackathon presentation
- `expected_output.json` - Example of expected audit report output

## Demo Scenarios

### Scenario 1: Clean Supplier (GREEN)
**Supplier:** GreenTech Manufacturing  
**Expected Result:** Low risk, no violations, compliant with all policies

### Scenario 2: Medium Risk Supplier (YELLOW)
**Supplier:** Global Textiles Inc  
**Expected Result:** Some concerns, requires monitoring, actionable recommendations

### Scenario 3: High Risk Supplier (RED)
**Supplier:** QuickProd Factories  
**Expected Result:** Critical violations, immediate action required

## Using Demo Data

### In Dashboard
Simply enter one of the demo supplier names from `demo_scenarios.json`

### In Tests
```python
import json

with open('data/sample/expected_output.json') as f:
    expected = json.load(f)
    
# Compare actual output with expected
assert actual_report['overall_risk'] == expected['audit_report']['overall_risk']
```

### For Presentations
Use the sample queries in `demo_scenarios.json` to demonstrate different risk levels and audit scenarios.

## Mock Data Behavior

The system uses mock data by default when:
- `USE_MOCK_DATA=true` in .env file
- Bedrock Agents are not yet configured
- Lambda function doesn't have real API keys

This allows for development and testing without AWS resources.
