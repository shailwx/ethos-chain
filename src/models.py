"""
Data models for Sentinel audit system.

This module defines Pydantic models for type-safe data structures
used throughout the application.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl, field_validator


class RiskLevel(str, Enum):
    """Risk level classification."""
    GREEN = "GREEN"
    YELLOW = "YELLOW"
    RED = "RED"
    UNKNOWN = "UNKNOWN"


class Severity(str, Enum):
    """Violation severity levels."""
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    CRITICAL = "CRITICAL"


class EvidenceType(str, Enum):
    """Type of evidence supporting a finding."""
    PROVEN = "PROVEN"
    ALLEGATION = "ALLEGATION"
    UNDER_INVESTIGATION = "UNDER_INVESTIGATION"


class Category(str, Enum):
    """Audit category classification."""
    LABOR = "Labor"
    ENVIRONMENT = "Environment"
    GOVERNANCE = "Governance"


class Finding(BaseModel):
    """
    A single finding from the investigation phase.
    
    Represents a piece of evidence or news about a supplier.
    """
    date: str = Field(
        ...,
        description="Date of the finding (ISO format or human-readable)"
    )
    source: str = Field(..., description="Source of the information")
    snippet: str = Field(..., description="Brief description of the finding")
    category: Category = Field(..., description="Category of the finding")
    url: Optional[str] = Field(default=None, description="URL to the source")
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v: str) -> str:
        """Validate and normalize date format."""
        # Try to parse various date formats
        try:
            # If it's already a valid date string, keep it
            datetime.fromisoformat(v.replace('Z', '+00:00'))
            return v
        except ValueError:
            # Return as-is if not parseable (human-readable format)
            return v


class Violation(BaseModel):
    """
    A policy violation detected during the audit phase.
    
    Links a finding to a specific policy breach with severity.
    """
    finding: Finding = Field(..., description="The underlying finding")
    severity: Severity = Field(..., description="Severity of the violation")
    policy_reference: str = Field(
        ...,
        description="Reference to the violated policy section"
    )
    evidence_type: EvidenceType = Field(
        ...,
        description="Type of evidence supporting this violation"
    )


class RiskScores(BaseModel):
    """Risk scores across different categories."""
    labor: int = Field(default=0, ge=0, le=100, alias="Labor")
    environment: int = Field(default=0, ge=0, le=100, alias="Environment")
    governance: int = Field(default=0, ge=0, le=100, alias="Governance")
    
    class Config:
        populate_by_name = True


class AuditReport(BaseModel):
    """
    Complete audit report for a supplier.
    
    This is the final output format consumed by the dashboard.
    Reference: SPEC_Version2.md - Section 3: API Contracts
    """
    supplier: str = Field(..., description="Name of the audited supplier")
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="Timestamp of the audit"
    )
    overall_risk: RiskLevel = Field(
        ...,
        description="Overall risk level (traffic light)"
    )
    risk_scores: RiskScores = Field(
        ...,
        description="Detailed risk scores by category"
    )
    findings: List[Finding] = Field(
        default_factory=list,
        description="All findings from investigation"
    )
    violations: List[Violation] = Field(
        default_factory=list,
        description="Policy violations detected"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Actionable recommendations"
    )
    
    @property
    def has_critical_violations(self) -> bool:
        """Check if report contains any critical violations."""
        return any(v.severity == Severity.CRITICAL for v in self.violations)
    
    @property
    def violation_count(self) -> int:
        """Total number of violations."""
        return len(self.violations)


class InvestigatorResponse(BaseModel):
    """
    Response format from the Investigator Agent.
    
    Reference: SPEC_Version2.md - Interface: Investigator -> Supervisor
    """
    supplier: str = Field(..., description="Name of the investigated supplier")
    findings: List[Finding] = Field(
        default_factory=list,
        description="List of findings discovered"
    )


class AuditorResponse(BaseModel):
    """
    Response format from the Auditor Agent.
    
    Reference: SPEC_Version2.md - Interface: Auditor -> Supervisor
    """
    overall_risk: RiskLevel = Field(..., description="Overall risk assessment")
    risk_scores: RiskScores = Field(..., description="Category risk scores")
    violations: List[Violation] = Field(
        default_factory=list,
        description="Detected violations"
    )
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommendations based on audit"
    )
