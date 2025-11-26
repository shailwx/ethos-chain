# Requirements Document

## Introduction

Sentinel is an AI-powered supply chain auditor that automates the vetting of suppliers against corporate ethical standards. The system uses a multi-agent architecture with AWS Bedrock to analyze supplier information from external sources and evaluate it against internal compliance policies. The system provides procurement teams with automated risk assessments, reducing manual vetting time while improving accuracy in identifying labor rights violations, environmental issues, and ethical concerns.

## Glossary

- **Sentinel System**: The complete AI-powered supply chain auditing application
- **Supervisor Agent**: The orchestrator agent that coordinates the audit workflow and formats final reports
- **Investigator Agent**: The worker agent responsible for gathering external intelligence about suppliers
- **Auditor Agent**: The worker agent responsible for evaluating findings against internal compliance policies
- **Knowledge Base**: The repository containing the organization's Supplier Code of Conduct and ethical policies
- **Risk Score**: A categorical assessment (Red/Yellow/Green) indicating supplier compliance level
- **Finding**: A specific piece of evidence about a supplier from an external source
- **Violation**: A finding that contradicts the organization's ethical policies
- **User Interface**: The Streamlit-based web application for user interaction

## Requirements

### Requirement 1

**User Story:** As a procurement team member, I want to input a supplier name and receive an automated audit, so that I can quickly assess supplier compliance without manual research.

#### Acceptance Criteria

1. WHEN a user submits a supplier name through the interface, THEN the Sentinel System SHALL initiate an audit workflow
2. WHEN the audit workflow completes, THEN the Sentinel System SHALL return results within 30 seconds
3. WHEN the audit completes, THEN the Sentinel System SHALL display a risk score categorized as Red, Yellow, or Green
4. WHEN audit results are displayed, THEN the Sentinel System SHALL present findings in a structured format with sources and dates
5. WHEN the system encounters an error during audit, THEN the Sentinel System SHALL notify the user with a clear error message

### Requirement 2

**User Story:** As a procurement team member, I want to see specific evidence for each risk flag, so that I can verify the findings and make informed decisions.

#### Acceptance Criteria

1. WHEN a violation is identified, THEN the Sentinel System SHALL display the source publication name
2. WHEN a violation is identified, THEN the Sentinel System SHALL display the date of the reported incident
3. WHEN a violation is identified, THEN the Sentinel System SHALL display a text snippet describing the incident
4. WHEN multiple findings exist for a supplier, THEN the Sentinel System SHALL list all findings with their respective evidence
5. WHEN a finding is classified as an allegation versus proven violation, THEN the Sentinel System SHALL distinguish between the two classifications

### Requirement 3

**User Story:** As a procurement team member, I want to see risk broken down by category, so that I can understand which specific areas of concern exist for a supplier.

#### Acceptance Criteria

1. WHEN audit results are displayed, THEN the Sentinel System SHALL categorize findings into Labor, Environment, and Ethics categories
2. WHEN displaying categorized findings, THEN the Sentinel System SHALL show the count of violations per category
3. WHEN displaying categorized findings, THEN the Sentinel System SHALL provide a visual representation of risk distribution across categories
4. WHERE a category has no violations, THEN the Sentinel System SHALL indicate zero violations for that category

### Requirement 4

**User Story:** As the Supervisor Agent, I want to coordinate the audit workflow by delegating tasks to specialized agents, so that the system maintains separation of concerns and produces accurate results.

#### Acceptance Criteria

1. WHEN the Supervisor Agent receives a supplier name, THEN the Supervisor Agent SHALL invoke the Investigator Agent to gather external data
2. WHEN the Investigator Agent returns findings, THEN the Supervisor Agent SHALL invoke the Auditor Agent with those findings
3. WHEN the Auditor Agent returns compliance assessments, THEN the Supervisor Agent SHALL format the results into a structured JSON report
4. WHEN formatting the final report, THEN the Supervisor Agent SHALL include the risk score, categorized findings, and evidence details
5. WHEN any agent fails to respond, THEN the Supervisor Agent SHALL handle the error and return a partial result or error message

### Requirement 5

**User Story:** As the Investigator Agent, I want to search external sources for supplier information, so that I can provide comprehensive intelligence about potential violations.

#### Acceptance Criteria

1. WHEN the Investigator Agent receives a supplier name, THEN the Investigator Agent SHALL search for labor violation reports
2. WHEN the Investigator Agent receives a supplier name, THEN the Investigator Agent SHALL search for environmental violation reports
3. WHEN the Investigator Agent receives a supplier name, THEN the Investigator Agent SHALL search for ethical violation reports
4. WHEN search results are found, THEN the Investigator Agent SHALL extract the date, source, and description for each finding
5. WHEN search results are found, THEN the Investigator Agent SHALL return findings in a structured JSON format with supplier name and findings list

### Requirement 6

**User Story:** As the Auditor Agent, I want to evaluate findings against our internal policies, so that I can determine which findings constitute actual violations.

#### Acceptance Criteria

1. WHEN the Auditor Agent receives findings from the Investigator Agent, THEN the Auditor Agent SHALL query the Knowledge Base for each finding
2. WHEN querying the Knowledge Base, THEN the Auditor Agent SHALL determine if a finding violates the Supplier Code of Conduct
3. WHEN a violation is identified, THEN the Auditor Agent SHALL assign a severity level of Minor, Major, or Critical
4. WHEN a violation is identified, THEN the Auditor Agent SHALL distinguish between allegations and proven violations
5. WHEN all findings are evaluated, THEN the Auditor Agent SHALL return a structured assessment with violation classifications and severity scores

### Requirement 7

**User Story:** As a system administrator, I want the system to use a Knowledge Base containing our ethical policies, so that audits are evaluated against our specific standards.

#### Acceptance Criteria

1. WHEN the system initializes, THEN the Sentinel System SHALL load the Supplier Code of Conduct into the Knowledge Base
2. WHEN the Auditor Agent queries policies, THEN the Knowledge Base SHALL return relevant policy sections
3. WHEN policy documents are updated, THEN the Knowledge Base SHALL reflect the updated policies for subsequent audits
4. WHEN the Knowledge Base is queried, THEN the Knowledge Base SHALL return results within 5 seconds

### Requirement 8

**User Story:** As a system architect, I want all agent communications to use structured JSON formats, so that the system maintains data integrity and enables reliable parsing.

#### Acceptance Criteria

1. WHEN the Investigator Agent returns findings, THEN the Investigator Agent SHALL format the response as valid JSON conforming to the defined schema
2. WHEN the Auditor Agent returns assessments, THEN the Auditor Agent SHALL format the response as valid JSON conforming to the defined schema
3. WHEN the Supervisor Agent produces the final report, THEN the Supervisor Agent SHALL format the response as valid JSON conforming to the defined schema
4. WHEN JSON is generated, THEN the Sentinel System SHALL validate the JSON against the schema before transmission
5. IF JSON validation fails, THEN the Sentinel System SHALL log the error and attempt to correct the format

### Requirement 9

**User Story:** As a compliance officer, I want the system to protect proprietary supplier data, so that we maintain confidentiality and comply with data protection regulations.

#### Acceptance Criteria

1. WHEN processing supplier data, THEN the Sentinel System SHALL not persist proprietary information to the AI model training data
2. WHEN querying external sources, THEN the Sentinel System SHALL only use publicly available information
3. WHEN storing audit results, THEN the Sentinel System SHALL encrypt sensitive supplier information
4. WHEN transmitting data between agents, THEN the Sentinel System SHALL use secure communication channels

### Requirement 10

**User Story:** As a procurement team member, I want the system to handle edge cases gracefully, so that I receive useful information even when data is incomplete or unavailable.

#### Acceptance Criteria

1. WHEN no findings are discovered for a supplier, THEN the Sentinel System SHALL return a Green risk score with an explanation
2. WHEN external sources are unavailable, THEN the Sentinel System SHALL notify the user and suggest retry options
3. WHEN a supplier name is ambiguous, THEN the Sentinel System SHALL request clarification from the user
4. WHEN the Knowledge Base query fails, THEN the Sentinel System SHALL log the error and return findings without policy evaluation
5. IF the audit exceeds the 30-second timeout, THEN the Sentinel System SHALL return partial results with a timeout notification
