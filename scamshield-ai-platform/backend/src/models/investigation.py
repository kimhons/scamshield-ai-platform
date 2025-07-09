"""
ScamShield AI - Investigation Models

Database models for investigations, reports, evidence, and scam database.
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import uuid
import json
from enum import Enum

from .user import db

class InvestigationStatus(Enum):
    """Investigation status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ThreatLevel(Enum):
    """Threat level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EvidenceType(Enum):
    """Evidence type enumeration"""
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    IMAGE = "image"
    DOCUMENT = "document"
    SOCIAL_MEDIA = "social_media"
    CRYPTOCURRENCY = "cryptocurrency"
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"

class Investigation(db.Model):
    """Investigation model for tracking fraud investigations"""
    
    __tablename__ = 'investigations'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Investigation details
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(InvestigationStatus), default=InvestigationStatus.PENDING, nullable=False, index=True)
    threat_level = db.Column(db.Enum(ThreatLevel), nullable=True, index=True)
    
    # Investigation configuration
    investigation_type = db.Column(db.String(50), nullable=False)  # quick_scan, deep_analysis, etc.
    model_tier = db.Column(db.String(50), nullable=False)  # basic, professional, enterprise, intelligence
    priority = db.Column(db.String(20), default='normal', nullable=False)  # low, normal, high, urgent
    
    # Results
    confidence_score = db.Column(db.Float, nullable=True)  # 0.0 to 1.0
    executive_summary = db.Column(db.Text, nullable=True)
    detailed_findings = db.Column(db.JSON, nullable=True)
    recommendations = db.Column(db.JSON, nullable=True)  # List of recommendation strings
    models_used = db.Column(db.JSON, nullable=True)  # List of AI models used
    
    # Processing metadata
    processing_time = db.Column(db.Float, nullable=True)  # Processing time in seconds
    cost = db.Column(db.Float, nullable=True)  # Cost in credits
    credits_consumed = db.Column(db.Integer, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), nullable=True)
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='investigations')
    evidence = db.relationship('Evidence', back_populates='investigation', cascade='all, delete-orphan')
    reports = db.relationship('Report', back_populates='investigation', cascade='all, delete-orphan')
    
    def __init__(self, user_id: str, title: str, investigation_type: str, model_tier: str, **kwargs):
        """Initialize investigation with required fields"""
        self.user_id = user_id
        self.title = title
        self.investigation_type = investigation_type
        self.model_tier = model_tier
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def start_processing(self) -> None:
        """Mark investigation as started"""
        self.status = InvestigationStatus.PROCESSING
        self.started_at = datetime.now(timezone.utc)
    
    def complete_processing(self, results: Dict[str, Any], credits_consumed: int) -> None:
        """Mark investigation as completed with results"""
        self.status = InvestigationStatus.COMPLETED
        self.completed_at = datetime.now(timezone.utc)
        self.credits_consumed = credits_consumed
        
        # Update results
        if 'confidence_score' in results:
            self.confidence_score = results['confidence_score']
        if 'threat_level' in results:
            self.threat_level = ThreatLevel(results['threat_level'])
        if 'executive_summary' in results:
            self.executive_summary = results['executive_summary']
        if 'detailed_findings' in results:
            self.detailed_findings = results['detailed_findings']
        if 'recommendations' in results:
            self.recommendations = results['recommendations']
        if 'models_used' in results:
            self.models_used = results['models_used']
        if 'processing_time' in results:
            self.processing_time = results['processing_time']
        if 'cost' in results:
            self.cost = results['cost']
    
    def fail_processing(self, error_message: str) -> None:
        """Mark investigation as failed"""
        self.status = InvestigationStatus.FAILED
        self.detailed_findings = {'error': error_message}
        self.completed_at = datetime.now(timezone.utc)
    
    def to_dict(self, include_detailed: bool = True) -> Dict[str, Any]:
        """Convert investigation to dictionary representation"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'status': self.status.value,
            'threat_level': self.threat_level.value if self.threat_level else None,
            'investigation_type': self.investigation_type,
            'model_tier': self.model_tier,
            'priority': self.priority,
            'confidence_score': self.confidence_score,
            'executive_summary': self.executive_summary,
            'credits_consumed': self.credits_consumed,
            'processing_time': self.processing_time,
            'cost': self.cost,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
        }
        
        if include_detailed:
            data.update({
                'detailed_findings': self.detailed_findings,
                'recommendations': self.recommendations,
                'models_used': self.models_used,
            })
        
        return data
    
    def __repr__(self) -> str:
        return f'<Investigation {self.id}: {self.title}>'

class Evidence(db.Model):
    """Evidence model for storing investigation artifacts"""
    
    __tablename__ = 'evidence'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    investigation_id = db.Column(db.String(36), db.ForeignKey('investigations.id'), nullable=False, index=True)
    
    # Evidence details
    evidence_type = db.Column(db.Enum(EvidenceType), nullable=False, index=True)
    content = db.Column(db.Text, nullable=False)  # The actual evidence content/URL/data
    source = db.Column(db.String(255), nullable=True)  # Source of the evidence
    metadata = db.Column(db.JSON, nullable=True)  # Additional metadata
    
    # Analysis results
    analysis_results = db.Column(db.JSON, nullable=True)
    risk_score = db.Column(db.Float, nullable=True)  # 0.0 to 1.0
    is_malicious = db.Column(db.Boolean, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    analyzed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    # Relationships
    investigation = db.relationship('Investigation', back_populates='evidence')
    
    def __init__(self, investigation_id: str, evidence_type: EvidenceType, content: str, **kwargs):
        """Initialize evidence with required fields"""
        self.investigation_id = investigation_id
        self.evidence_type = evidence_type
        self.content = content
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update_analysis(self, results: Dict[str, Any], risk_score: float = None, is_malicious: bool = None) -> None:
        """Update evidence with analysis results"""
        self.analysis_results = results
        self.analyzed_at = datetime.now(timezone.utc)
        if risk_score is not None:
            self.risk_score = risk_score
        if is_malicious is not None:
            self.is_malicious = is_malicious
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert evidence to dictionary representation"""
        return {
            'id': self.id,
            'investigation_id': self.investigation_id,
            'evidence_type': self.evidence_type.value,
            'content': self.content,
            'source': self.source,
            'metadata': self.metadata,
            'analysis_results': self.analysis_results,
            'risk_score': self.risk_score,
            'is_malicious': self.is_malicious,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'analyzed_at': self.analyzed_at.isoformat() if self.analyzed_at else None,
        }
    
    def __repr__(self) -> str:
        return f'<Evidence {self.id}: {self.evidence_type.value}>'

class Report(db.Model):
    """Report model for generated investigation reports"""
    
    __tablename__ = 'reports'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    investigation_id = db.Column(db.String(36), db.ForeignKey('investigations.id'), nullable=False, index=True)
    
    # Report details
    report_type = db.Column(db.String(50), nullable=False)  # executive, technical, legal, etc.
    format = db.Column(db.String(20), nullable=False)  # pdf, html, json
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Metadata
    template_version = db.Column(db.String(20), nullable=True)
    generated_by = db.Column(db.String(100), nullable=True)  # AI model or user
    file_path = db.Column(db.String(500), nullable=True)  # File storage path
    file_size = db.Column(db.Integer, nullable=True)  # File size in bytes
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    investigation = db.relationship('Investigation', back_populates='reports')
    
    def __init__(self, investigation_id: str, report_type: str, format: str, title: str, content: str, **kwargs):
        """Initialize report with required fields"""
        self.investigation_id = investigation_id
        self.report_type = report_type
        self.format = format
        self.title = title
        self.content = content
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary representation"""
        return {
            'id': self.id,
            'investigation_id': self.investigation_id,
            'report_type': self.report_type,
            'format': self.format,
            'title': self.title,
            'template_version': self.template_version,
            'generated_by': self.generated_by,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self) -> str:
        return f'<Report {self.id}: {self.title}>'

class ScamDatabase(db.Model):
    """ScamDatabase model for known scam patterns and indicators"""
    
    __tablename__ = 'scam_database'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Scam details
    scam_type = db.Column(db.String(100), nullable=False, index=True)
    indicator_type = db.Column(db.String(50), nullable=False, index=True)  # url, email, phone, etc.
    indicator_value = db.Column(db.String(500), nullable=False, index=True)
    threat_level = db.Column(db.Enum(ThreatLevel), nullable=False, index=True)
    
    # Scam information
    description = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(255), nullable=True)  # Where this scam was reported
    confidence = db.Column(db.Float, nullable=False, default=1.0)  # Confidence in this indicator
    
    # Metadata
    tags = db.Column(db.JSON, nullable=True)  # Tags for categorization
    related_indicators = db.Column(db.JSON, nullable=True)  # Related scam indicators
    
    # Verification
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    verified_by = db.Column(db.String(100), nullable=True)
    false_positive_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen = db.Column(db.DateTime(timezone=True), nullable=True)
    
    def __init__(self, scam_type: str, indicator_type: str, indicator_value: str, threat_level: ThreatLevel, **kwargs):
        """Initialize scam database entry with required fields"""
        self.scam_type = scam_type
        self.indicator_type = indicator_type
        self.indicator_value = indicator_value
        self.threat_level = threat_level
        
        # Set optional fields
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def update_last_seen(self) -> None:
        """Update last seen timestamp"""
        self.last_seen = datetime.now(timezone.utc)
    
    def report_false_positive(self) -> None:
        """Report this indicator as a false positive"""
        self.false_positive_count += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert scam database entry to dictionary representation"""
        return {
            'id': self.id,
            'scam_type': self.scam_type,
            'indicator_type': self.indicator_type,
            'indicator_value': self.indicator_value,
            'threat_level': self.threat_level.value,
            'description': self.description,
            'source': self.source,
            'confidence': self.confidence,
            'tags': self.tags,
            'related_indicators': self.related_indicators,
            'is_verified': self.is_verified,
            'verified_by': self.verified_by,
            'false_positive_count': self.false_positive_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
        }
    
    def __repr__(self) -> str:
        return f'<ScamDatabase {self.scam_type}: {self.indicator_value}>'
