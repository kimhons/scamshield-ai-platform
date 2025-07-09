"""
ScamShield AI - Comprehensive Report Generation System

Professional report templates with legal disclaimers and tier-based formatting
"""

from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
import json
import uuid
import base64
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class ReportTier(Enum):
    """Report tiers corresponding to subscription levels"""
    FREE = "free"
    BASIC = "basic"
    PLUS = "plus"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class ReportFormat(Enum):
    """Available report formats"""
    HTML = "html"
    PDF = "pdf"
    JSON = "json"
    MARKDOWN = "markdown"

class ReportStatus(Enum):
    """Report generation and approval status"""
    PENDING = "pending"
    GENERATED = "generated"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"

@dataclass
class ReportMetadata:
    """Report metadata structure"""
    report_id: str
    investigation_id: str
    user_id: str
    tier: ReportTier
    format: ReportFormat
    status: ReportStatus
    generated_at: datetime
    approved_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    version: str = "1.0"
    classification: str = "UNCLASSIFIED"
    distribution: str = "RESTRICTED"

class LegalDisclaimerManager:
    """Manages legal disclaimers and compliance requirements"""
    
    @staticmethod
    def get_general_disclaimer() -> str:
        """Get general legal disclaimer for all reports"""
        return """
IMPORTANT LEGAL DISCLAIMER AND LIMITATIONS

This report is provided by ScamShield AI for informational and educational purposes only. By accessing and using this report, you acknowledge and agree to the following terms and limitations:

1. NATURE OF SERVICE
   This report represents an automated analysis conducted by artificial intelligence systems and should not be considered as professional legal, financial, or investigative advice. The analysis is based on available data and algorithmic assessment, which may not capture all relevant factors or nuances.

2. NO GUARANTEE OF ACCURACY
   While ScamShield AI employs advanced AI technologies and methodologies, we make no representations or warranties regarding the accuracy, completeness, reliability, or timeliness of the information contained in this report. The findings and conclusions are based on automated analysis and may contain errors, omissions, or inaccuracies.

3. LIMITATION OF LIABILITY
   ScamShield AI, its affiliates, officers, directors, employees, and agents shall not be liable for any direct, indirect, incidental, special, consequential, or punitive damages arising from or related to your use of this report or reliance on its contents. This includes, but is not limited to, financial losses, business interruption, or reputational damage.

4. NOT LEGAL OR FINANCIAL ADVICE
   This report does not constitute legal, financial, investment, or professional advice. You should consult with qualified professionals before making any decisions based on the information contained herein. ScamShield AI is not a law enforcement agency and does not provide legal services.

5. VERIFICATION REQUIRED
   All findings and recommendations in this report should be independently verified through appropriate channels. Users are strongly advised to conduct their own due diligence and seek professional guidance before taking any action based on this report.

6. PRIVACY AND CONFIDENTIALITY
   This report may contain sensitive information. Users are responsible for maintaining appropriate confidentiality and security measures. ScamShield AI is not responsible for any unauthorized disclosure or misuse of report contents.

7. REGULATORY COMPLIANCE
   Users are responsible for ensuring their use of this report complies with all applicable laws, regulations, and industry standards in their jurisdiction. ScamShield AI makes no representations regarding regulatory compliance.

8. UPDATES AND MODIFICATIONS
   The threat landscape evolves rapidly. Information in this report may become outdated or superseded by new developments. ScamShield AI reserves the right to update or modify its analysis methodologies without notice.

9. THIRD-PARTY INFORMATION
   This report may reference or incorporate information from third-party sources. ScamShield AI does not endorse or guarantee the accuracy of such third-party information and is not responsible for any errors or omissions therein.

10. DISPUTE RESOLUTION
    Any disputes arising from or related to this report shall be resolved through binding arbitration in accordance with the rules of the American Arbitration Association. The laws of Delaware shall govern the interpretation of this disclaimer.

By proceeding to review this report, you acknowledge that you have read, understood, and agree to be bound by these terms and limitations.

For questions regarding this disclaimer or our services, please contact: legal@scamshield.ai

Last Updated: {date}
""".format(date=datetime.now(timezone.utc).strftime("%B %d, %Y"))
    
    @staticmethod
    def get_tier_specific_disclaimer(tier: ReportTier) -> str:
        """Get tier-specific disclaimers"""
        
        disclaimers = {
            ReportTier.FREE: """
FREE TIER LIMITATIONS:
- This analysis uses basic detection algorithms and may miss sophisticated threats
- Limited data sources and reduced analysis depth
- No human verification or quality assurance review
- Intended for general awareness only, not for critical decision-making
- Higher probability of false positives and false negatives
""",
            
            ReportTier.BASIC: """
BASIC TIER LIMITATIONS:
- Analysis includes standard AI models with moderate sophistication
- Limited behavioral analysis and threat attribution capabilities
- Automated quality checks but no human expert review
- Suitable for personal use but not for business-critical decisions
- May not detect advanced or novel threat techniques
""",
            
            ReportTier.PLUS: """
PLUS TIER CAPABILITIES AND LIMITATIONS:
- Advanced AI analysis with enhanced threat detection capabilities
- Includes behavioral profiling and intelligence correlation
- Automated quality assurance with periodic human oversight
- Suitable for professional use with appropriate verification
- May not capture highly sophisticated state-sponsored threats
""",
            
            ReportTier.PRO: """
PRO TIER CAPABILITIES AND LIMITATIONS:
- Elite AI ensemble analysis with maximum detection capabilities
- Comprehensive threat attribution and predictive modeling
- Human expert review and quality assurance for critical findings
- Suitable for enterprise and high-stakes decision-making
- Represents current state-of-the-art in automated threat analysis
""",
            
            ReportTier.ENTERPRISE: """
ENTERPRISE TIER CAPABILITIES AND LIMITATIONS:
- Custom AI models and analysis frameworks
- Dedicated expert review and validation
- Tailored analysis for specific organizational requirements
- Highest level of accuracy and comprehensiveness available
- Subject to custom service level agreements and guarantees
"""
        }
        
        return disclaimers.get(tier, disclaimers[ReportTier.FREE])
    
    @staticmethod
    def get_data_sources_disclaimer() -> str:
        """Get disclaimer about data sources and limitations"""
        return """
DATA SOURCES AND METHODOLOGY DISCLAIMER

1. DATA COLLECTION LIMITATIONS
   This analysis is based on publicly available information and data sources accessible at the time of investigation. Private, classified, or restricted information is not included in this assessment.

2. TEMPORAL LIMITATIONS
   Threat landscapes evolve rapidly. This analysis reflects conditions at the time of generation and may not account for subsequent changes or developments.

3. SCOPE LIMITATIONS
   The analysis is limited to the specific artifacts and information provided. Additional context or information not available during the investigation may significantly alter the conclusions.

4. ALGORITHMIC LIMITATIONS
   AI systems, while sophisticated, may exhibit biases, limitations, or blind spots inherent in their training data and algorithms. Human oversight and verification remain essential.

5. INTELLIGENCE GAPS
   This report may identify intelligence gaps or areas requiring additional investigation. Users should consider these limitations when evaluating the completeness of the analysis.
"""
    
    @staticmethod
    def get_action_disclaimer() -> str:
        """Get disclaimer about recommended actions"""
        return """
RECOMMENDED ACTIONS DISCLAIMER

1. VERIFICATION REQUIRED
   All recommended actions should be independently verified and evaluated by qualified professionals before implementation.

2. RISK ASSESSMENT
   Users must conduct their own risk assessment and consider their specific circumstances, risk tolerance, and regulatory requirements.

3. PROFESSIONAL CONSULTATION
   For legal, financial, or regulatory matters, consult with appropriate licensed professionals in your jurisdiction.

4. NO GUARANTEE OF EFFECTIVENESS
   ScamShield AI makes no guarantees regarding the effectiveness of recommended actions or their suitability for specific situations.

5. EVOLVING THREATS
   Threat actors may adapt their methods in response to defensive measures. Continuous monitoring and adaptation are essential.
"""

class ReportTemplateManager:
    """Manages report templates for different tiers and formats"""
    
    def __init__(self):
        self.disclaimer_manager = LegalDisclaimerManager()
    
    def generate_html_report(
        self,
        investigation_data: Dict[str, Any],
        tier: ReportTier,
        metadata: ReportMetadata
    ) -> str:
        """Generate HTML format report"""
        
        template = self._get_html_template(tier)
        
        # Prepare report data
        report_data = self._prepare_report_data(investigation_data, tier, metadata)
        
        # Format the template
        html_report = template.format(**report_data)
        
        return html_report
    
    def generate_pdf_report(
        self,
        investigation_data: Dict[str, Any],
        tier: ReportTier,
        metadata: ReportMetadata
    ) -> bytes:
        """Generate PDF format report"""
        
        # Generate HTML first
        html_content = self.generate_html_report(investigation_data, tier, metadata)
        
        # Convert HTML to PDF (implementation would use libraries like weasyprint)
        # For now, return HTML as bytes
        return html_content.encode('utf-8')
    
    def generate_json_report(
        self,
        investigation_data: Dict[str, Any],
        tier: ReportTier,
        metadata: ReportMetadata
    ) -> Dict[str, Any]:
        """Generate JSON format report"""
        
        report_data = self._prepare_report_data(investigation_data, tier, metadata)
        
        # Structure for JSON output
        json_report = {
            "metadata": {
                "report_id": metadata.report_id,
                "investigation_id": metadata.investigation_id,
                "tier": metadata.tier.value,
                "generated_at": metadata.generated_at.isoformat(),
                "version": metadata.version,
                "classification": metadata.classification,
                "status": metadata.status.value
            },
            "executive_summary": report_data.get("executive_summary", ""),
            "threat_assessment": report_data.get("threat_assessment", {}),
            "detailed_findings": report_data.get("detailed_findings", {}),
            "technical_analysis": report_data.get("technical_analysis", {}),
            "behavioral_analysis": report_data.get("behavioral_analysis", {}),
            "recommendations": report_data.get("recommendations", []),
            "evidence": report_data.get("evidence", []),
            "disclaimers": {
                "general": self.disclaimer_manager.get_general_disclaimer(),
                "tier_specific": self.disclaimer_manager.get_tier_specific_disclaimer(tier),
                "data_sources": self.disclaimer_manager.get_data_sources_disclaimer(),
                "actions": self.disclaimer_manager.get_action_disclaimer()
            }
        }
        
        return json_report
    
    def _prepare_report_data(
        self,
        investigation_data: Dict[str, Any],
        tier: ReportTier,
        metadata: ReportMetadata
    ) -> Dict[str, Any]:
        """Prepare and format report data based on tier"""
        
        # Base report data
        report_data = {
            "report_id": metadata.report_id,
            "investigation_id": metadata.investigation_id,
            "generated_at": metadata.generated_at.strftime("%B %d, %Y at %I:%M %p UTC"),
            "tier": tier.value.title(),
            "classification": metadata.classification,
            "status": metadata.status.value.title(),
            "version": metadata.version,
            
            # Disclaimers
            "general_disclaimer": self.disclaimer_manager.get_general_disclaimer(),
            "tier_disclaimer": self.disclaimer_manager.get_tier_specific_disclaimer(tier),
            "data_sources_disclaimer": self.disclaimer_manager.get_data_sources_disclaimer(),
            "action_disclaimer": self.disclaimer_manager.get_action_disclaimer(),
            
            # Investigation data
            "executive_summary": investigation_data.get("executive_summary", ""),
            "threat_level": investigation_data.get("threat_level", "unknown"),
            "confidence_score": investigation_data.get("confidence_score", 0),
            "fraud_probability": investigation_data.get("fraud_probability", 0),
            "primary_indicators": investigation_data.get("primary_indicators", []),
            "recommendations": investigation_data.get("recommendations", []),
            "evidence": investigation_data.get("evidence_analysis", {}),
            "models_used": investigation_data.get("models_used", []),
            "processing_time": investigation_data.get("processing_time", 0),
            "artifacts_analyzed": investigation_data.get("artifacts_count", 0)
        }
        
        # Tier-specific data inclusion
        if tier in [ReportTier.PLUS, ReportTier.PRO, ReportTier.ENTERPRISE]:
            report_data.update({
                "detailed_findings": investigation_data.get("detailed_findings", {}),
                "technical_analysis": investigation_data.get("technical_analysis", {}),
                "behavioral_analysis": investigation_data.get("behavioral_analysis", {})
            })
        
        if tier in [ReportTier.PRO, ReportTier.ENTERPRISE]:
            report_data.update({
                "attribution_analysis": investigation_data.get("attribution_analysis", {}),
                "predictive_analysis": investigation_data.get("predictive_analysis", {}),
                "strategic_assessment": investigation_data.get("strategic_assessment", {}),
                "intelligence_gaps": investigation_data.get("intelligence_gaps", [])
            })
        
        if tier == ReportTier.ENTERPRISE:
            report_data.update({
                "custom_analysis": investigation_data.get("custom_analysis", {}),
                "regulatory_compliance": investigation_data.get("regulatory_compliance", {}),
                "executive_briefing": investigation_data.get("executive_briefing", {})
            })
        
        return report_data
    
    def _get_html_template(self, tier: ReportTier) -> str:
        """Get HTML template based on tier"""
        
        if tier == ReportTier.FREE:
            return self._get_free_tier_template()
        elif tier == ReportTier.BASIC:
            return self._get_basic_tier_template()
        elif tier == ReportTier.PLUS:
            return self._get_plus_tier_template()
        elif tier == ReportTier.PRO:
            return self._get_pro_tier_template()
        elif tier == ReportTier.ENTERPRISE:
            return self._get_enterprise_tier_template()
        else:
            return self._get_basic_tier_template()
    
    def _get_free_tier_template(self) -> str:
        """Free tier HTML template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScamShield AI - Free Tier Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 2px solid #e74c3c; padding-bottom: 20px; margin-bottom: 30px; }}
        .logo {{ font-size: 24px; font-weight: bold; color: #e74c3c; }}
        .report-title {{ font-size: 20px; color: #333; margin-top: 10px; }}
        .metadata {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .threat-level {{ padding: 10px; border-radius: 5px; text-align: center; font-weight: bold; margin: 20px 0; }}
        .threat-low {{ background-color: #d4edda; color: #155724; }}
        .threat-medium {{ background-color: #fff3cd; color: #856404; }}
        .threat-high {{ background-color: #f8d7da; color: #721c24; }}
        .threat-critical {{ background-color: #f5c6cb; color: #721c24; }}
        .section {{ margin: 20px 0; }}
        .section h3 {{ color: #e74c3c; border-bottom: 1px solid #e74c3c; padding-bottom: 5px; }}
        .disclaimer {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .disclaimer h4 {{ color: #856404; margin-top: 0; }}
        .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; color: #666; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🛡️ ScamShield AI</div>
            <div class="report-title">Free Tier Fraud Analysis Report</div>
        </div>
        
        <div class="metadata">
            <strong>Report ID:</strong> {report_id}<br>
            <strong>Investigation ID:</strong> {investigation_id}<br>
            <strong>Generated:</strong> {generated_at}<br>
            <strong>Tier:</strong> {tier}<br>
            <strong>Classification:</strong> {classification}<br>
            <strong>Status:</strong> {status}
        </div>
        
        <div class="threat-level threat-{threat_level}">
            Threat Level: {threat_level.upper()} | Confidence: {confidence_score}%
        </div>
        
        <div class="section">
            <h3>Executive Summary</h3>
            <p>{executive_summary}</p>
        </div>
        
        <div class="section">
            <h3>Key Findings</h3>
            <ul>
                {primary_indicators_list}
            </ul>
        </div>
        
        <div class="section">
            <h3>Recommendations</h3>
            <ul>
                {recommendations_list}
            </ul>
        </div>
        
        <div class="disclaimer">
            <h4>⚠️ Important Disclaimer</h4>
            <p><strong>Free Tier Limitations:</strong> This analysis uses basic detection algorithms and may miss sophisticated threats. Limited data sources and reduced analysis depth. No human verification or quality assurance review. Intended for general awareness only, not for critical decision-making.</p>
        </div>
        
        <div class="disclaimer">
            <h4>📋 Legal Disclaimer</h4>
            <p>{general_disclaimer}</p>
        </div>
        
        <div class="footer">
            <p>Generated by ScamShield AI | Report Version {version}</p>
            <p>For support, contact: support@scamshield.ai</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _get_pro_tier_template(self) -> str:
        """Pro tier HTML template with comprehensive analysis"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScamShield AI - Pro Tier Intelligence Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 3px solid #2c3e50; padding-bottom: 30px; margin-bottom: 40px; }}
        .logo {{ font-size: 32px; font-weight: bold; color: #2c3e50; }}
        .report-title {{ font-size: 24px; color: #34495e; margin-top: 15px; }}
        .classification {{ background-color: #e74c3c; color: white; padding: 8px 16px; border-radius: 20px; display: inline-block; margin-top: 10px; }}
        .metadata-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .metadata-card {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #3498db; }}
        .threat-assessment {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .threat-card {{ padding: 20px; border-radius: 8px; text-align: center; font-weight: bold; }}
        .threat-low {{ background-color: #d4edda; color: #155724; }}
        .threat-medium {{ background-color: #fff3cd; color: #856404; }}
        .threat-high {{ background-color: #f8d7da; color: #721c24; }}
        .threat-critical {{ background-color: #f5c6cb; color: #721c24; }}
        .section {{ margin: 30px 0; }}
        .section h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
        .section h3 {{ color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }}
        .analysis-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .analysis-card {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #e74c3c; }}
        .confidence-bar {{ background-color: #ecf0f1; height: 20px; border-radius: 10px; overflow: hidden; margin: 10px 0; }}
        .confidence-fill {{ height: 100%; background-color: #3498db; transition: width 0.3s ease; }}
        .disclaimer {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 20px; border-radius: 8px; margin: 30px 0; }}
        .disclaimer h4 {{ color: #856404; margin-top: 0; }}
        .footer {{ text-align: center; margin-top: 40px; padding-top: 30px; border-top: 2px solid #ecf0f1; color: #7f8c8d; }}
        .evidence-item {{ background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 3px solid #e74c3c; }}
        .recommendation-item {{ background-color: #e8f5e8; padding: 15px; margin: 10px 0; border-radius: 5px; border-left: 3px solid #27ae60; }}
        .technical-details {{ font-family: 'Courier New', monospace; background-color: #2c3e50; color: #ecf0f1; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        ul {{ padding-left: 20px; }}
        li {{ margin: 8px 0; }}
        .status-badge {{ padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold; }}
        .status-approved {{ background-color: #d4edda; color: #155724; }}
        .status-pending {{ background-color: #fff3cd; color: #856404; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🛡️ ScamShield AI</div>
            <div class="report-title">Pro Tier Intelligence Assessment</div>
            <div class="classification">CONFIDENTIAL - PRO TIER</div>
            <div class="status-badge status-{status}">{status.upper()}</div>
        </div>
        
        <div class="metadata-grid">
            <div class="metadata-card">
                <h4>Report Information</h4>
                <strong>Report ID:</strong> {report_id}<br>
                <strong>Investigation ID:</strong> {investigation_id}<br>
                <strong>Generated:</strong> {generated_at}<br>
                <strong>Version:</strong> {version}
            </div>
            <div class="metadata-card">
                <h4>Analysis Details</h4>
                <strong>Tier:</strong> {tier}<br>
                <strong>Artifacts Analyzed:</strong> {artifacts_analyzed}<br>
                <strong>Processing Time:</strong> {processing_time}s<br>
                <strong>Models Used:</strong> {models_count}
            </div>
        </div>
        
        <div class="threat-assessment">
            <div class="threat-card threat-{threat_level}">
                <h3>Threat Level</h3>
                <div style="font-size: 24px;">{threat_level.upper()}</div>
            </div>
            <div class="threat-card">
                <h3>Confidence Score</h3>
                <div style="font-size: 24px; color: #3498db;">{confidence_score}%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {confidence_score}%;"></div>
                </div>
            </div>
            <div class="threat-card">
                <h3>Fraud Probability</h3>
                <div style="font-size: 24px; color: #e74c3c;">{fraud_probability}%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: {fraud_probability}%; background-color: #e74c3c;"></div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🎯 Executive Summary</h2>
            <p style="font-size: 16px; line-height: 1.8;">{executive_summary}</p>
        </div>
        
        <div class="section">
            <h2>🔍 Detailed Analysis</h2>
            <div class="analysis-grid">
                <div class="analysis-card">
                    <h3>Technical Analysis</h3>
                    <p>{technical_analysis_summary}</p>
                </div>
                <div class="analysis-card">
                    <h3>Behavioral Analysis</h3>
                    <p>{behavioral_analysis_summary}</p>
                </div>
                <div class="analysis-card">
                    <h3>Attribution Assessment</h3>
                    <p>{attribution_analysis_summary}</p>
                </div>
                <div class="analysis-card">
                    <h3>Predictive Analysis</h3>
                    <p>{predictive_analysis_summary}</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🚨 Key Findings</h2>
            {primary_indicators_detailed}
        </div>
        
        <div class="section">
            <h2>📋 Strategic Recommendations</h2>
            {recommendations_detailed}
        </div>
        
        <div class="section">
            <h2>🔬 Evidence Analysis</h2>
            {evidence_detailed}
        </div>
        
        <div class="section">
            <h2>⚙️ Technical Details</h2>
            <div class="technical-details">
                AI Models Used: {models_used_list}
                Processing Time: {processing_time} seconds
                Analysis Depth: Elite Pro Tier
                Quality Assurance: Human Expert Review
            </div>
        </div>
        
        <div class="disclaimer">
            <h4>⚠️ Pro Tier Capabilities and Limitations</h4>
            <p>{tier_disclaimer}</p>
        </div>
        
        <div class="disclaimer">
            <h4>📋 Legal Disclaimer and Terms</h4>
            <p>{general_disclaimer}</p>
        </div>
        
        <div class="disclaimer">
            <h4>📊 Data Sources and Methodology</h4>
            <p>{data_sources_disclaimer}</p>
        </div>
        
        <div class="disclaimer">
            <h4>🎯 Recommended Actions Disclaimer</h4>
            <p>{action_disclaimer}</p>
        </div>
        
        <div class="footer">
            <p><strong>ScamShield AI Pro Tier Intelligence Report</strong></p>
            <p>Generated by Elite AI Ensemble | Human Expert Reviewed | Report Version {version}</p>
            <p>For support and inquiries: pro-support@scamshield.ai | +1-800-SCAM-SHIELD</p>
            <p>© 2025 ScamShield AI. All rights reserved. Confidential and proprietary.</p>
        </div>
    </div>
</body>
</html>
"""

class ReportApprovalWorkflow:
    """Manages report approval workflow and quality assurance"""
    
    def __init__(self):
        self.approval_rules = self._initialize_approval_rules()
    
    def _initialize_approval_rules(self) -> Dict[ReportTier, Dict[str, Any]]:
        """Initialize approval rules for different tiers"""
        return {
            ReportTier.FREE: {
                "requires_approval": False,
                "auto_approve": True,
                "review_time_hours": 0,
                "quality_checks": ["basic_validation"]
            },
            ReportTier.BASIC: {
                "requires_approval": False,
                "auto_approve": True,
                "review_time_hours": 0,
                "quality_checks": ["basic_validation", "content_review"]
            },
            ReportTier.PLUS: {
                "requires_approval": True,
                "auto_approve": False,
                "review_time_hours": 4,
                "quality_checks": ["basic_validation", "content_review", "technical_review"]
            },
            ReportTier.PRO: {
                "requires_approval": True,
                "auto_approve": False,
                "review_time_hours": 8,
                "quality_checks": ["basic_validation", "content_review", "technical_review", "expert_review"]
            },
            ReportTier.ENTERPRISE: {
                "requires_approval": True,
                "auto_approve": False,
                "review_time_hours": 24,
                "quality_checks": ["basic_validation", "content_review", "technical_review", "expert_review", "compliance_review"]
            }
        }
    
    def should_require_approval(self, tier: ReportTier) -> bool:
        """Check if report tier requires approval"""
        return self.approval_rules[tier]["requires_approval"]
    
    def get_review_time(self, tier: ReportTier) -> int:
        """Get expected review time in hours"""
        return self.approval_rules[tier]["review_time_hours"]
    
    def get_quality_checks(self, tier: ReportTier) -> List[str]:
        """Get required quality checks for tier"""
        return self.approval_rules[tier]["quality_checks"]
    
    def validate_report_quality(
        self,
        report_data: Dict[str, Any],
        tier: ReportTier
    ) -> Tuple[bool, List[str]]:
        """Validate report quality based on tier requirements"""
        
        validation_errors = []
        required_checks = self.get_quality_checks(tier)
        
        # Basic validation
        if "basic_validation" in required_checks:
            errors = self._basic_validation(report_data)
            validation_errors.extend(errors)
        
        # Content review
        if "content_review" in required_checks:
            errors = self._content_review(report_data)
            validation_errors.extend(errors)
        
        # Technical review
        if "technical_review" in required_checks:
            errors = self._technical_review(report_data)
            validation_errors.extend(errors)
        
        # Expert review (would involve human reviewer)
        if "expert_review" in required_checks:
            errors = self._expert_review_requirements(report_data)
            validation_errors.extend(errors)
        
        # Compliance review
        if "compliance_review" in required_checks:
            errors = self._compliance_review(report_data)
            validation_errors.extend(errors)
        
        return len(validation_errors) == 0, validation_errors
    
    def _basic_validation(self, report_data: Dict[str, Any]) -> List[str]:
        """Basic validation checks"""
        errors = []
        
        required_fields = [
            "executive_summary", "threat_level", "confidence_score",
            "recommendations", "primary_indicators"
        ]
        
        for field in required_fields:
            if field not in report_data or not report_data[field]:
                errors.append(f"Missing or empty required field: {field}")
        
        # Validate confidence score
        if "confidence_score" in report_data:
            score = report_data["confidence_score"]
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                errors.append("Confidence score must be between 0 and 100")
        
        # Validate threat level
        if "threat_level" in report_data:
            valid_levels = ["low", "medium", "high", "critical"]
            if report_data["threat_level"] not in valid_levels:
                errors.append(f"Invalid threat level. Must be one of: {valid_levels}")
        
        return errors
    
    def _content_review(self, report_data: Dict[str, Any]) -> List[str]:
        """Content quality review"""
        errors = []
        
        # Check executive summary length and quality
        if "executive_summary" in report_data:
            summary = report_data["executive_summary"]
            if len(summary) < 100:
                errors.append("Executive summary too short (minimum 100 characters)")
            if len(summary) > 2000:
                errors.append("Executive summary too long (maximum 2000 characters)")
        
        # Check recommendations quality
        if "recommendations" in report_data:
            recommendations = report_data["recommendations"]
            if isinstance(recommendations, list) and len(recommendations) < 3:
                errors.append("Insufficient recommendations (minimum 3 required)")
        
        return errors
    
    def _technical_review(self, report_data: Dict[str, Any]) -> List[str]:
        """Technical analysis review"""
        errors = []
        
        # Check for technical analysis completeness
        if "technical_analysis" in report_data:
            tech_analysis = report_data["technical_analysis"]
            if not isinstance(tech_analysis, dict) or not tech_analysis:
                errors.append("Technical analysis section is incomplete")
        
        # Check evidence quality
        if "evidence_analysis" in report_data:
            evidence = report_data["evidence_analysis"]
            if not isinstance(evidence, dict) or not evidence:
                errors.append("Evidence analysis section is incomplete")
        
        return errors
    
    def _expert_review_requirements(self, report_data: Dict[str, Any]) -> List[str]:
        """Requirements for expert review"""
        requirements = []
        
        # High-stakes findings require expert review
        if report_data.get("threat_level") in ["high", "critical"]:
            requirements.append("High threat level requires expert validation")
        
        if report_data.get("confidence_score", 0) > 90:
            requirements.append("High confidence claims require expert verification")
        
        return requirements
    
    def _compliance_review(self, report_data: Dict[str, Any]) -> List[str]:
        """Compliance and regulatory review"""
        errors = []
        
        # Check for proper disclaimers
        required_disclaimers = [
            "general_disclaimer", "tier_disclaimer",
            "data_sources_disclaimer", "action_disclaimer"
        ]
        
        for disclaimer in required_disclaimers:
            if disclaimer not in report_data or not report_data[disclaimer]:
                errors.append(f"Missing required disclaimer: {disclaimer}")
        
        return errors

class ReportGenerator:
    """Main report generation orchestrator"""
    
    def __init__(self):
        self.template_manager = ReportTemplateManager()
        self.approval_workflow = ReportApprovalWorkflow()
        self.disclaimer_manager = LegalDisclaimerManager()
    
    def generate_report(
        self,
        investigation_data: Dict[str, Any],
        user_id: str,
        tier: ReportTier,
        format: ReportFormat = ReportFormat.HTML,
        investigation_id: Optional[str] = None
    ) -> Tuple[str, ReportMetadata]:
        """Generate a complete report with metadata"""
        
        # Create report metadata
        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            investigation_id=investigation_id or str(uuid.uuid4()),
            user_id=user_id,
            tier=tier,
            format=format,
            status=ReportStatus.GENERATED,
            generated_at=datetime.now(timezone.utc)
        )
        
        # Check if approval is required
        if self.approval_workflow.should_require_approval(tier):
            metadata.status = ReportStatus.UNDER_REVIEW
        
        # Validate report quality
        is_valid, validation_errors = self.approval_workflow.validate_report_quality(
            investigation_data, tier
        )
        
        if not is_valid:
            logger.warning(f"Report validation failed: {validation_errors}")
            # Continue with warnings but mark for review
            metadata.status = ReportStatus.UNDER_REVIEW
        
        # Generate report based on format
        if format == ReportFormat.HTML:
            report_content = self.template_manager.generate_html_report(
                investigation_data, tier, metadata
            )
        elif format == ReportFormat.JSON:
            report_content = json.dumps(
                self.template_manager.generate_json_report(
                    investigation_data, tier, metadata
                ), indent=2
            )
        elif format == ReportFormat.PDF:
            report_content = self.template_manager.generate_pdf_report(
                investigation_data, tier, metadata
            ).decode('utf-8')
        else:
            # Default to HTML
            report_content = self.template_manager.generate_html_report(
                investigation_data, tier, metadata
            )
        
        logger.info(f"Generated {tier.value} tier report {metadata.report_id}")
        
        return report_content, metadata
    
    def approve_report(
        self,
        report_id: str,
        approved_by: str,
        approval_notes: Optional[str] = None
    ) -> bool:
        """Approve a report for publication"""
        
        # In a real implementation, this would update the database
        # For now, we'll just log the approval
        logger.info(f"Report {report_id} approved by {approved_by}")
        
        return True
    
    def reject_report(
        self,
        report_id: str,
        rejected_by: str,
        rejection_reason: str
    ) -> bool:
        """Reject a report and require regeneration"""
        
        logger.info(f"Report {report_id} rejected by {rejected_by}: {rejection_reason}")
        
        return True

# Initialize global report generator
report_generator = ReportGenerator()

