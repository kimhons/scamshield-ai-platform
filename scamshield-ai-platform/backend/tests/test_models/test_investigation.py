"""
ScamShield AI - Investigation Model Tests

Comprehensive tests for Investigation, Evidence, Report, and ScamDatabase models.
"""

import pytest
from datetime import datetime, timezone
import json

from models.investigation import (
    Investigation, Evidence, Report, ScamDatabase,
    InvestigationStatus, ThreatLevel, EvidenceType
)


@pytest.mark.unit
class TestInvestigationModel:
    """Test cases for Investigation model"""
    
    def test_investigation_creation(self, db, user):
        """Test basic investigation creation"""
        investigation = Investigation(
            user_id=user.id,
            title='Test Phishing Email',
            investigation_type='deep_analysis',
            model_tier='professional'
        )
        db.session.add(investigation)
        db.session.commit()
        
        assert investigation.id is not None
        assert investigation.user_id == user.id
        assert investigation.title == 'Test Phishing Email'
        assert investigation.investigation_type == 'deep_analysis'
        assert investigation.model_tier == 'professional'
        assert investigation.status == InvestigationStatus.PENDING
        assert investigation.priority == 'normal'
        assert investigation.created_at is not None
        assert investigation.updated_at is not None
    
    def test_investigation_with_optional_fields(self, db, user):
        """Test investigation creation with optional fields"""
        investigation = Investigation(
            user_id=user.id,
            title='Complex Scam Investigation',
            description='Detailed description of the scam',
            investigation_type='comprehensive',
            model_tier='enterprise',
            priority='high'
        )
        db.session.add(investigation)
        db.session.commit()
        
        assert investigation.description == 'Detailed description of the scam'
        assert investigation.priority == 'high'
    
    def test_investigation_start_processing(self, db, user):
        """Test starting investigation processing"""
        investigation = Investigation(
            user_id=user.id,
            title='Test Investigation',
            investigation_type='quick_scan',
            model_tier='basic'
        )
        db.session.add(investigation)
        db.session.commit()
        
        assert investigation.status == InvestigationStatus.PENDING
        assert investigation.started_at is None
        
        investigation.start_processing()
        
        assert investigation.status == InvestigationStatus.PROCESSING
        assert investigation.started_at is not None
    
    def test_investigation_complete_processing(self, db, user):
        """Test completing investigation processing"""
        investigation = Investigation(
            user_id=user.id,
            title='Test Investigation',
            investigation_type='quick_scan',
            model_tier='basic'
        )
        investigation.start_processing()
        db.session.add(investigation)
        db.session.commit()
        
        results = {
            'confidence_score': 0.85,
            'threat_level': 'high',
            'executive_summary': 'This appears to be a phishing attempt.',
            'detailed_findings': {'indicators': ['suspicious_url', 'fake_sender']},
            'recommendations': ['Block sender', 'Report to authorities'],
            'models_used': ['gpt-4', 'claude-3'],
            'processing_time': 15.5,
            'cost': 3.5
        }
        
        investigation.complete_processing(results, credits_consumed=5)
        
        assert investigation.status == InvestigationStatus.COMPLETED
        assert investigation.completed_at is not None
        assert investigation.confidence_score == 0.85
        assert investigation.threat_level == ThreatLevel.HIGH
        assert investigation.executive_summary == 'This appears to be a phishing attempt.'
        assert investigation.detailed_findings == {'indicators': ['suspicious_url', 'fake_sender']}
        assert investigation.recommendations == ['Block sender', 'Report to authorities']
        assert investigation.models_used == ['gpt-4', 'claude-3']
        assert investigation.processing_time == 15.5
        assert investigation.cost == 3.5
        assert investigation.credits_consumed == 5
    
    def test_investigation_fail_processing(self, db, user):
        """Test failing investigation processing"""
        investigation = Investigation(
            user_id=user.id,
            title='Test Investigation',
            investigation_type='quick_scan',
            model_tier='basic'
        )
        investigation.start_processing()
        db.session.add(investigation)
        db.session.commit()
        
        error_message = 'AI model timeout'
        investigation.fail_processing(error_message)
        
        assert investigation.status == InvestigationStatus.FAILED
        assert investigation.completed_at is not None
        assert investigation.detailed_findings == {'error': error_message}
    
    def test_investigation_to_dict(self, db, user):
        """Test investigation to_dict conversion"""
        investigation = Investigation(
            user_id=user.id,
            title='Test Investigation',
            description='Test description',
            investigation_type='deep_analysis',
            model_tier='professional',
            priority='high'
        )
        
        results = {
            'confidence_score': 0.75,
            'threat_level': 'medium',
            'executive_summary': 'Moderate risk detected.',
            'detailed_findings': {'score': 0.75},
            'recommendations': ['Monitor closely'],
            'models_used': ['gpt-4'],
            'processing_time': 12.3,
            'cost': 2.8
        }
        investigation.complete_processing(results, credits_consumed=3)
        db.session.add(investigation)
        db.session.commit()
        
        investigation_dict = investigation.to_dict()
        
        assert investigation_dict['id'] == investigation.id
        assert investigation_dict['user_id'] == user.id
        assert investigation_dict['title'] == 'Test Investigation'
        assert investigation_dict['description'] == 'Test description'
        assert investigation_dict['status'] == 'completed'
        assert investigation_dict['threat_level'] == 'medium'
        assert investigation_dict['investigation_type'] == 'deep_analysis'
        assert investigation_dict['model_tier'] == 'professional'
        assert investigation_dict['priority'] == 'high'
        assert investigation_dict['confidence_score'] == 0.75
        assert investigation_dict['executive_summary'] == 'Moderate risk detected.'
        assert investigation_dict['detailed_findings'] == {'score': 0.75}
        assert investigation_dict['recommendations'] == ['Monitor closely']
        assert investigation_dict['models_used'] == ['gpt-4']
        assert investigation_dict['processing_time'] == 12.3
        assert investigation_dict['cost'] == 2.8
        assert investigation_dict['credits_consumed'] == 3
    
    def test_investigation_to_dict_without_detailed(self, db, user):
        """Test investigation to_dict without detailed information"""
        investigation = Investigation(
            user_id=user.id,
            title='Test Investigation',
            investigation_type='quick_scan',
            model_tier='basic'
        )
        db.session.add(investigation)
        db.session.commit()
        
        investigation_dict = investigation.to_dict(include_detailed=False)
        
        assert 'detailed_findings' not in investigation_dict
        assert 'recommendations' not in investigation_dict
        assert 'models_used' not in investigation_dict
    
    def test_investigation_repr(self, db, user):
        """Test investigation string representation"""
        investigation = Investigation(
            user_id=user.id,
            title='Test Investigation',
            investigation_type='quick_scan',
            model_tier='basic'
        )
        db.session.add(investigation)
        db.session.commit()
        
        expected_repr = f'<Investigation {investigation.id}: Test Investigation>'
        assert repr(investigation) == expected_repr


@pytest.mark.unit
class TestEvidenceModel:
    """Test cases for Evidence model"""
    
    def test_evidence_creation(self, db, investigation):
        """Test basic evidence creation"""
        evidence = Evidence(
            investigation_id=investigation.id,
            evidence_type=EvidenceType.URL,
            content='https://suspicious-website.com'
        )
        db.session.add(evidence)
        db.session.commit()
        
        assert evidence.id is not None
        assert evidence.investigation_id == investigation.id
        assert evidence.evidence_type == EvidenceType.URL
        assert evidence.content == 'https://suspicious-website.com'
        assert evidence.created_at is not None
        assert evidence.analyzed_at is None
    
    def test_evidence_with_metadata(self, db, investigation):
        """Test evidence creation with metadata"""
        metadata = {
            'user_agent': 'Mozilla/5.0...',
            'referrer': 'https://google.com',
            'timestamp': '2025-01-09T15:30:00Z'
        }
        
        evidence = Evidence(
            investigation_id=investigation.id,
            evidence_type=EvidenceType.EMAIL,
            content='phishing@scammer.com',
            source='User report',
            metadata=metadata
        )
        db.session.add(evidence)
        db.session.commit()
        
        assert evidence.source == 'User report'
        assert evidence.metadata == metadata
    
    def test_evidence_update_analysis(self, db, investigation):
        """Test updating evidence with analysis results"""
        evidence = Evidence(
            investigation_id=investigation.id,
            evidence_type=EvidenceType.PHONE,
            content='+1-800-SCAMMER'
        )
        db.session.add(evidence)
        db.session.commit()
        
        analysis_results = {
            'reputation_score': 0.1,
            'known_scammer': True,
            'reported_count': 150
        }
        
        evidence.update_analysis(analysis_results, risk_score=0.9, is_malicious=True)
        
        assert evidence.analysis_results == analysis_results
        assert evidence.risk_score == 0.9
        assert evidence.is_malicious is True
        assert evidence.analyzed_at is not None
    
    def test_evidence_to_dict(self, db, investigation):
        """Test evidence to_dict conversion"""
        evidence = Evidence(
            investigation_id=investigation.id,
            evidence_type=EvidenceType.IMAGE,
            content='/path/to/screenshot.png',
            source='User upload'
        )
        
        analysis_results = {'contains_text': 'Bank alert', 'suspicious_elements': ['urgent_action']}
        evidence.update_analysis(analysis_results, risk_score=0.7, is_malicious=True)
        db.session.add(evidence)
        db.session.commit()
        
        evidence_dict = evidence.to_dict()
        
        assert evidence_dict['id'] == evidence.id
        assert evidence_dict['investigation_id'] == investigation.id
        assert evidence_dict['evidence_type'] == 'image'
        assert evidence_dict['content'] == '/path/to/screenshot.png'
        assert evidence_dict['source'] == 'User upload'
        assert evidence_dict['analysis_results'] == analysis_results
        assert evidence_dict['risk_score'] == 0.7
        assert evidence_dict['is_malicious'] is True
    
    def test_evidence_repr(self, db, investigation):
        """Test evidence string representation"""
        evidence = Evidence(
            investigation_id=investigation.id,
            evidence_type=EvidenceType.DOMAIN,
            content='scammer-site.com'
        )
        db.session.add(evidence)
        db.session.commit()
        
        expected_repr = f'<Evidence {evidence.id}: domain>'
        assert repr(evidence) == expected_repr


@pytest.mark.unit
class TestReportModel:
    """Test cases for Report model"""
    
    def test_report_creation(self, db, investigation):
        """Test basic report creation"""
        content = """
        # Investigation Report
        
        ## Summary
        This investigation found evidence of phishing activity.
        
        ## Recommendations
        1. Block the sender
        2. Report to authorities
        """
        
        report = Report(
            investigation_id=investigation.id,
            report_type='executive',
            format='html',
            title='Phishing Investigation Report',
            content=content
        )
        db.session.add(report)
        db.session.commit()
        
        assert report.id is not None
        assert report.investigation_id == investigation.id
        assert report.report_type == 'executive'
        assert report.format == 'html'
        assert report.title == 'Phishing Investigation Report'
        assert report.content == content
        assert report.created_at is not None
    
    def test_report_with_metadata(self, db, investigation):
        """Test report creation with metadata"""
        report = Report(
            investigation_id=investigation.id,
            report_type='technical',
            format='pdf',
            title='Technical Analysis Report',
            content='Detailed technical content...',
            template_version='2.1',
            generated_by='GPT-4',
            file_path='/reports/tech_report_123.pdf',
            file_size=256000
        )
        db.session.add(report)
        db.session.commit()
        
        assert report.template_version == '2.1'
        assert report.generated_by == 'GPT-4'
        assert report.file_path == '/reports/tech_report_123.pdf'
        assert report.file_size == 256000
    
    def test_report_to_dict(self, db, investigation):
        """Test report to_dict conversion"""
        report = Report(
            investigation_id=investigation.id,
            report_type='legal',
            format='docx',
            title='Legal Evidence Report',
            content='Legal analysis content...',
            template_version='1.5',
            generated_by='Claude-3',
            file_size=128000
        )
        db.session.add(report)
        db.session.commit()
        
        report_dict = report.to_dict()
        
        assert report_dict['id'] == report.id
        assert report_dict['investigation_id'] == investigation.id
        assert report_dict['report_type'] == 'legal'
        assert report_dict['format'] == 'docx'
        assert report_dict['title'] == 'Legal Evidence Report'
        assert report_dict['template_version'] == '1.5'
        assert report_dict['generated_by'] == 'Claude-3'
        assert report_dict['file_size'] == 128000
        # Content should not be included in dict for performance
        assert 'content' not in report_dict
    
    def test_report_repr(self, db, investigation):
        """Test report string representation"""
        report = Report(
            investigation_id=investigation.id,
            report_type='summary',
            format='json',
            title='Investigation Summary',
            content='{"summary": "test"}'
        )
        db.session.add(report)
        db.session.commit()
        
        expected_repr = f'<Report {report.id}: Investigation Summary>'
        assert repr(report) == expected_repr


@pytest.mark.unit
class TestScamDatabaseModel:
    """Test cases for ScamDatabase model"""
    
    def test_scam_database_creation(self, db):
        """Test basic scam database entry creation"""
        scam_entry = ScamDatabase(
            scam_type='phishing',
            indicator_type='url',
            indicator_value='https://fake-bank.scammer.com',
            threat_level=ThreatLevel.HIGH
        )
        db.session.add(scam_entry)
        db.session.commit()
        
        assert scam_entry.id is not None
        assert scam_entry.scam_type == 'phishing'
        assert scam_entry.indicator_type == 'url'
        assert scam_entry.indicator_value == 'https://fake-bank.scammer.com'
        assert scam_entry.threat_level == ThreatLevel.HIGH
        assert scam_entry.confidence == 1.0  # Default value
        assert scam_entry.is_verified is False
        assert scam_entry.false_positive_count == 0
        assert scam_entry.created_at is not None
    
    def test_scam_database_with_metadata(self, db):
        """Test scam database entry with metadata"""
        tags = ['banking', 'credential_theft', 'urgent_action']
        related_indicators = [
            'fake-bank-support.com',
            'urgent-account-verification.net'
        ]
        
        scam_entry = ScamDatabase(
            scam_type='business_email_compromise',
            indicator_type='email',
            indicator_value='ceo@company-typo.com',
            threat_level=ThreatLevel.CRITICAL,
            description='CEO impersonation attempt targeting finance department',
            source='Security team report',
            confidence=0.95,
            tags=tags,
            related_indicators=related_indicators
        )
        db.session.add(scam_entry)
        db.session.commit()
        
        assert scam_entry.description == 'CEO impersonation attempt targeting finance department'
        assert scam_entry.source == 'Security team report'
        assert scam_entry.confidence == 0.95
        assert scam_entry.tags == tags
        assert scam_entry.related_indicators == related_indicators
    
    def test_scam_database_update_last_seen(self, db):
        """Test updating last seen timestamp"""
        scam_entry = ScamDatabase(
            scam_type='romance_scam',
            indicator_type='phone',
            indicator_value='+1-555-LOVE-ME',
            threat_level=ThreatLevel.MEDIUM
        )
        db.session.add(scam_entry)
        db.session.commit()
        
        assert scam_entry.last_seen is None
        
        scam_entry.update_last_seen()
        
        assert scam_entry.last_seen is not None
        assert (datetime.now(timezone.utc) - scam_entry.last_seen).total_seconds() < 5
    
    def test_scam_database_report_false_positive(self, db):
        """Test reporting false positives"""
        scam_entry = ScamDatabase(
            scam_type='tech_support',
            indicator_type='phone',
            indicator_value='+1-800-MICROSOFT',
            threat_level=ThreatLevel.HIGH
        )
        db.session.add(scam_entry)
        db.session.commit()
        
        assert scam_entry.false_positive_count == 0
        
        scam_entry.report_false_positive()
        assert scam_entry.false_positive_count == 1
        
        scam_entry.report_false_positive()
        assert scam_entry.false_positive_count == 2
    
    def test_scam_database_to_dict(self, db):
        """Test scam database to_dict conversion"""
        scam_entry = ScamDatabase(
            scam_type='crypto_scam',
            indicator_type='cryptocurrency',
            indicator_value='1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
            threat_level=ThreatLevel.CRITICAL,
            description='Bitcoin address used in fake investment scheme',
            source='Blockchain analysis',
            confidence=0.99,
            tags=['cryptocurrency', 'investment_fraud'],
            is_verified=True,
            verified_by='Security analyst'
        )
        scam_entry.update_last_seen()
        scam_entry.report_false_positive()
        db.session.add(scam_entry)
        db.session.commit()
        
        scam_dict = scam_entry.to_dict()
        
        assert scam_dict['id'] == scam_entry.id
        assert scam_dict['scam_type'] == 'crypto_scam'
        assert scam_dict['indicator_type'] == 'cryptocurrency'
        assert scam_dict['indicator_value'] == '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2'
        assert scam_dict['threat_level'] == 'critical'
        assert scam_dict['description'] == 'Bitcoin address used in fake investment scheme'
        assert scam_dict['source'] == 'Blockchain analysis'
        assert scam_dict['confidence'] == 0.99
        assert scam_dict['tags'] == ['cryptocurrency', 'investment_fraud']
        assert scam_dict['is_verified'] is True
        assert scam_dict['verified_by'] == 'Security analyst'
        assert scam_dict['false_positive_count'] == 1
        assert scam_dict['last_seen'] is not None
    
    def test_scam_database_repr(self, db):
        """Test scam database string representation"""
        scam_entry = ScamDatabase(
            scam_type='lottery_scam',
            indicator_type='email',
            indicator_value='winner@mega-lottery-intl.com',
            threat_level=ThreatLevel.MEDIUM
        )
        db.session.add(scam_entry)
        db.session.commit()
        
        expected_repr = '<ScamDatabase lottery_scam: winner@mega-lottery-intl.com>'
        assert repr(scam_entry) == expected_repr


@pytest.mark.integration
class TestInvestigationRelationships:
    """Test relationships between investigation models"""
    
    def test_investigation_evidence_relationship(self, db, investigation):
        """Test investigation-evidence relationship"""
        evidence1 = Evidence(
            investigation_id=investigation.id,
            evidence_type=EvidenceType.URL,
            content='https://scam1.com'
        )
        evidence2 = Evidence(
            investigation_id=investigation.id,
            evidence_type=EvidenceType.EMAIL,
            content='scammer@fake.com'
        )
        
        db.session.add_all([evidence1, evidence2])
        db.session.commit()
        
        # Test forward relationship
        assert len(investigation.evidence) == 2
        assert evidence1 in investigation.evidence
        assert evidence2 in investigation.evidence
        
        # Test backward relationship
        assert evidence1.investigation == investigation
        assert evidence2.investigation == investigation
    
    def test_investigation_report_relationship(self, db, investigation):
        """Test investigation-report relationship"""
        report1 = Report(
            investigation_id=investigation.id,
            report_type='executive',
            format='pdf',
            title='Executive Summary',
            content='Summary content'
        )
        report2 = Report(
            investigation_id=investigation.id,
            report_type='technical',
            format='html',
            title='Technical Report',
            content='Technical content'
        )
        
        db.session.add_all([report1, report2])
        db.session.commit()
        
        # Test forward relationship
        assert len(investigation.reports) == 2
        assert report1 in investigation.reports
        assert report2 in investigation.reports
        
        # Test backward relationship
        assert report1.investigation == investigation
        assert report2.investigation == investigation
    
    def test_cascade_delete(self, db, user):
        """Test cascade delete behavior"""
        investigation = Investigation(
            user_id=user.id,
            title='Test Cascade Delete',
            investigation_type='quick_scan',
            model_tier='basic'
        )
        db.session.add(investigation)
        db.session.commit()
        
        evidence = Evidence(
            investigation_id=investigation.id,
            evidence_type=EvidenceType.URL,
            content='https://test.com'
        )
        report = Report(
            investigation_id=investigation.id,
            report_type='summary',
            format='json',
            title='Test Report',
            content='{"test": true}'
        )
        
        db.session.add_all([evidence, report])
        db.session.commit()
        
        evidence_id = evidence.id
        report_id = report.id
        
        # Delete investigation should cascade to evidence and reports
        db.session.delete(investigation)
        db.session.commit()
        
        # Verify cascade delete worked
        assert Evidence.query.get(evidence_id) is None
        assert Report.query.get(report_id) is None
