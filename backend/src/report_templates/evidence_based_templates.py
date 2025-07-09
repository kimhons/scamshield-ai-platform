"""
ScamShield AI - Evidence-Based Report Templates

Professional report templates that present facts and evidence rather than conclusions,
with comprehensive legal disclaimers and ethical compliance
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
import json

from ..ethical_framework.ethics_manager import (
    EvidenceBasedClaim, EvidenceLevel, SourceType, ClaimType,
    ethics_manager, evidence_based_generator, legal_compliance_manager
)
from ..data_sources.public_apis import public_data_apis

class EvidenceBasedReportTemplates:
    """Evidence-based report templates with ethical compliance"""
    
    def __init__(self):
        self.ethics_manager = ethics_manager
        self.evidence_generator = evidence_based_generator
        self.legal_manager = legal_compliance_manager
    
    def generate_evidence_based_html_report(
        self,
        investigation_data: Dict[str, Any],
        evidence_sources: List[Any],
        tier: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Generate evidence-based HTML report"""
        
        # Generate evidence-based findings
        findings = self.evidence_generator.generate_evidence_based_findings(
            investigation_data, evidence_sources
        )
        
        # Get appropriate template based on tier
        if tier.lower() in ['pro', 'enterprise']:
            template = self._get_professional_evidence_template()
        else:
            template = self._get_standard_evidence_template()
        
        # Prepare template data
        template_data = self._prepare_evidence_template_data(
            investigation_data, findings, evidence_sources, tier, metadata
        )
        
        # Format template
        return template.format(**template_data)
    
    def _get_professional_evidence_template(self) -> str:
        """Professional evidence-based report template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScamShield AI - Evidence-Based Investigation Report</title>
    <style>
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            line-height: 1.6; 
            margin: 0; 
            padding: 20px; 
            background-color: #f8f9fa; 
            color: #333;
        }}
        .container {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background-color: white; 
            padding: 40px; 
            border-radius: 12px; 
            box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
        }}
        .header {{ 
            text-align: center; 
            border-bottom: 3px solid #2c3e50; 
            padding-bottom: 30px; 
            margin-bottom: 40px; 
        }}
        .logo {{ 
            font-size: 32px; 
            font-weight: bold; 
            color: #2c3e50; 
        }}
        .report-title {{ 
            font-size: 24px; 
            color: #34495e; 
            margin-top: 15px; 
        }}
        .classification {{ 
            background-color: #3498db; 
            color: white; 
            padding: 8px 16px; 
            border-radius: 20px; 
            display: inline-block; 
            margin-top: 10px; 
            font-weight: bold;
        }}
        .evidence-disclaimer {{ 
            background-color: #e8f4fd; 
            border-left: 4px solid #3498db; 
            padding: 20px; 
            margin: 30px 0; 
            border-radius: 5px;
        }}
        .evidence-disclaimer h3 {{ 
            color: #2980b9; 
            margin-top: 0; 
        }}
        .metadata-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }}
        .metadata-card {{ 
            background-color: #f8f9fa; 
            padding: 20px; 
            border-radius: 8px; 
            border-left: 4px solid #3498db; 
        }}
        .section {{ 
            margin: 30px 0; 
        }}
        .section h2 {{ 
            color: #2c3e50; 
            border-bottom: 2px solid #3498db; 
            padding-bottom: 10px; 
        }}
        .section h3 {{ 
            color: #34495e; 
            border-bottom: 1px solid #bdc3c7; 
            padding-bottom: 5px; 
        }}
        .evidence-item {{ 
            background-color: #f8f9fa; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 5px; 
            border-left: 3px solid #27ae60; 
        }}
        .evidence-level {{ 
            display: inline-block; 
            padding: 4px 8px; 
            border-radius: 12px; 
            font-size: 12px; 
            font-weight: bold; 
            text-transform: uppercase; 
        }}
        .evidence-verified {{ background-color: #d4edda; color: #155724; }}
        .evidence-probable {{ background-color: #fff3cd; color: #856404; }}
        .evidence-possible {{ background-color: #e2e3e5; color: #383d41; }}
        .evidence-unverified {{ background-color: #f8d7da; color: #721c24; }}
        .source-list {{ 
            background-color: #f8f9fa; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 10px 0; 
        }}
        .source-item {{ 
            margin: 5px 0; 
            padding: 8px; 
            background-color: white; 
            border-radius: 3px; 
            border-left: 2px solid #3498db; 
        }}
        .limitation-box {{ 
            background-color: #fff3cd; 
            border: 1px solid #ffeaa7; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 15px 0; 
        }}
        .alternative-explanation {{ 
            background-color: #e8f5e8; 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 3px; 
            border-left: 3px solid #27ae60; 
        }}
        .verification-recommendation {{ 
            background-color: #e3f2fd; 
            padding: 10px; 
            margin: 5px 0; 
            border-radius: 3px; 
            border-left: 3px solid #2196f3; 
        }}
        .legal-disclaimer {{ 
            background-color: #fff3cd; 
            border: 1px solid #ffeaa7; 
            padding: 20px; 
            border-radius: 8px; 
            margin: 30px 0; 
        }}
        .legal-disclaimer h4 {{ 
            color: #856404; 
            margin-top: 0; 
        }}
        .footer {{ 
            text-align: center; 
            margin-top: 40px; 
            padding-top: 30px; 
            border-top: 2px solid #ecf0f1; 
            color: #7f8c8d; 
        }}
        .api-sources {{ 
            background-color: #f8f9fa; 
            padding: 15px; 
            border-radius: 5px; 
            margin: 15px 0; 
        }}
        .confidence-indicator {{ 
            display: inline-block; 
            width: 100px; 
            height: 10px; 
            background-color: #ecf0f1; 
            border-radius: 5px; 
            overflow: hidden; 
            margin-left: 10px; 
        }}
        .confidence-fill {{ 
            height: 100%; 
            background-color: #3498db; 
            transition: width 0.3s ease; 
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🛡️ ScamShield AI</div>
            <div class="report-title">Evidence-Based Investigation Report</div>
            <div class="classification">EVIDENCE-BASED ANALYSIS</div>
        </div>
        
        <div class="evidence-disclaimer">
            <h3>📋 Evidence-Based Methodology Notice</h3>
            <p><strong>This report presents factual observations and evidence-based analysis rather than definitive conclusions.</strong> 
            All findings are supported by verifiable sources and documented evidence. Users must independently verify 
            information and draw their own conclusions. Alternative explanations may exist for all observations presented.</p>
        </div>
        
        <div class="metadata-grid">
            <div class="metadata-card">
                <h4>Report Information</h4>
                <strong>Report ID:</strong> {report_id}<br>
                <strong>Investigation ID:</strong> {investigation_id}<br>
                <strong>Generated:</strong> {generated_at}<br>
                <strong>Analysis Tier:</strong> {tier}
            </div>
            <div class="metadata-card">
                <h4>Evidence Summary</h4>
                <strong>Total Sources:</strong> {total_sources}<br>
                <strong>Verified Sources:</strong> {verified_sources}<br>
                <strong>Average Reliability:</strong> {average_reliability:.1%}<br>
                <strong>Verification Level:</strong> <span class="evidence-level evidence-{verification_level}">{verification_level}</span>
            </div>
        </div>
        
        <div class="section">
            <h2>🔍 Factual Observations</h2>
            <p>The following observations are based on verifiable data from reliable sources:</p>
            {factual_observations}
        </div>
        
        <div class="section">
            <h2>📊 Evidence Analysis</h2>
            <h3>Sources and Verification</h3>
            <div class="source-list">
                {evidence_sources_list}
            </div>
            
            <h3>Data Verification Methods</h3>
            <div class="api-sources">
                <strong>Public APIs and Databases Used:</strong>
                {verification_methods}
            </div>
        </div>
        
        <div class="section">
            <h2>🔬 Pattern Analysis</h2>
            <p><em>Note: Pattern analysis is based on algorithmic assessment and may not account for all legitimate explanations.</em></p>
            {pattern_analysis}
        </div>
        
        <div class="section">
            <h2>⚠️ Risk Indicators</h2>
            <p><em>Risk indicators are observations that may warrant further investigation. They do not constitute proof of fraudulent activity.</em></p>
            {risk_indicators}
        </div>
        
        <div class="section">
            <h2>❓ Information Gaps</h2>
            <p>The following information could not be verified or was not available during this analysis:</p>
            {information_gaps}
        </div>
        
        <div class="section">
            <h2>🔄 Alternative Explanations</h2>
            <p>Legitimate explanations that could account for the observations include:</p>
            {alternative_explanations}
        </div>
        
        <div class="section">
            <h2>✅ Recommended Verification Steps</h2>
            <p>To further verify the findings in this report, consider the following steps:</p>
            {verification_recommendations}
        </div>
        
        <div class="limitation-box">
            <h4>⚠️ Analysis Limitations</h4>
            <ul>
                <li>Analysis based only on publicly available information at time of investigation</li>
                <li>Technical analysis limited to accessible infrastructure data</li>
                <li>Pattern recognition may produce false positives or miss sophisticated techniques</li>
                <li>Information may be incomplete, outdated, or inaccurate</li>
                <li>Alternative explanations may exist for all observations</li>
            </ul>
        </div>
        
        <div class="legal-disclaimer">
            <h4>📋 Legal Disclaimer and User Responsibilities</h4>
            {legal_disclaimer}
        </div>
        
        <div class="legal-disclaimer">
            <h4>🔒 Evidence and Source Disclaimer</h4>
            {evidence_disclaimer}
        </div>
        
        <div class="legal-disclaimer">
            <h4>⚖️ Ethical Use Requirements</h4>
            {ethical_disclaimer}
        </div>
        
        <div class="footer">
            <p><strong>ScamShield AI Evidence-Based Investigation Platform</strong></p>
            <p>Generated using ethical AI methodology | Evidence-based analysis | Report Version {version}</p>
            <p>For support and verification assistance: support@scamshield.ai</p>
            <p>© 2025 ScamShield AI. All rights reserved. This report contains evidence-based analysis only.</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _get_standard_evidence_template(self) -> str:
        """Standard evidence-based report template"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScamShield AI - Evidence Summary Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 20px; margin-bottom: 30px; }}
        .logo {{ font-size: 24px; font-weight: bold; color: #3498db; }}
        .report-title {{ font-size: 20px; color: #333; margin-top: 10px; }}
        .evidence-notice {{ background-color: #e8f4fd; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .metadata {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .section {{ margin: 20px 0; }}
        .section h3 {{ color: #3498db; border-bottom: 1px solid #3498db; padding-bottom: 5px; }}
        .evidence-item {{ background-color: #f8f9fa; padding: 10px; margin: 8px 0; border-radius: 5px; border-left: 3px solid #27ae60; }}
        .limitation {{ background-color: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; margin: 15px 0; }}
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
            <div class="report-title">Evidence Summary Report</div>
        </div>
        
        <div class="evidence-notice">
            <strong>Evidence-Based Analysis:</strong> This report presents factual observations and documented evidence. 
            Users must independently verify information and draw their own conclusions.
        </div>
        
        <div class="metadata">
            <strong>Report ID:</strong> {report_id}<br>
            <strong>Generated:</strong> {generated_at}<br>
            <strong>Evidence Sources:</strong> {total_sources}<br>
            <strong>Verification Level:</strong> {verification_level}
        </div>
        
        <div class="section">
            <h3>Verified Observations</h3>
            {factual_observations}
        </div>
        
        <div class="section">
            <h3>Evidence Sources</h3>
            {evidence_sources_list}
        </div>
        
        <div class="section">
            <h3>Recommended Verification</h3>
            {verification_recommendations}
        </div>
        
        <div class="limitation">
            <h4>⚠️ Important Limitations</h4>
            <p>This analysis is based on publicly available information and automated assessment. 
            Alternative explanations may exist. Independent verification is strongly recommended.</p>
        </div>
        
        <div class="disclaimer">
            <h4>📋 Legal Disclaimer</h4>
            {legal_disclaimer}
        </div>
        
        <div class="footer">
            <p>Generated by ScamShield AI Evidence-Based Analysis | Report Version {version}</p>
            <p>For support: support@scamshield.ai</p>
        </div>
    </div>
</body>
</html>
"""
    
    def _prepare_evidence_template_data(
        self,
        investigation_data: Dict[str, Any],
        findings: Dict[str, Any],
        evidence_sources: List[Any],
        tier: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Prepare data for evidence-based template"""
        
        # Format factual observations
        factual_observations = self._format_factual_observations(findings.get("factual_observations", []))
        
        # Format evidence sources
        evidence_sources_list = self._format_evidence_sources(evidence_sources)
        
        # Format pattern analysis
        pattern_analysis = self._format_pattern_analysis(findings.get("pattern_analysis", {}))
        
        # Format risk indicators
        risk_indicators = self._format_risk_indicators(findings.get("risk_indicators", []))
        
        # Format information gaps
        information_gaps = self._format_information_gaps(findings.get("information_gaps", []))
        
        # Format alternative explanations
        alternative_explanations = self._format_alternative_explanations(findings.get("alternative_explanations", []))
        
        # Format verification recommendations
        verification_recommendations = self._format_verification_recommendations(findings.get("recommended_verification", []))
        
        # Format verification methods
        verification_methods = self._format_verification_methods()
        
        # Get evidence summary
        evidence_summary = findings.get("evidence_summary", {})
        
        return {
            "report_id": metadata.get("report_id", "N/A"),
            "investigation_id": metadata.get("investigation_id", "N/A"),
            "generated_at": datetime.now(timezone.utc).strftime("%B %d, %Y at %I:%M %p UTC"),
            "tier": tier.title(),
            "version": metadata.get("version", "1.0"),
            
            # Evidence summary data
            "total_sources": evidence_summary.get("total_sources", 0),
            "verified_sources": len([s for s in evidence_sources if hasattr(s, 'verification_status') and s.verification_status.value == 'verified']),
            "average_reliability": evidence_summary.get("average_reliability", 0),
            "verification_level": findings.get("verification_status", {}).get("overall_verification_level", "unverified"),
            
            # Formatted content
            "factual_observations": factual_observations,
            "evidence_sources_list": evidence_sources_list,
            "pattern_analysis": pattern_analysis,
            "risk_indicators": risk_indicators,
            "information_gaps": information_gaps,
            "alternative_explanations": alternative_explanations,
            "verification_recommendations": verification_recommendations,
            "verification_methods": verification_methods,
            
            # Legal disclaimers
            "legal_disclaimer": self.legal_manager.report_disclaimers["evidence_based"],
            "evidence_disclaimer": self.legal_manager.report_disclaimers["source_limitations"],
            "ethical_disclaimer": self._get_ethical_use_disclaimer()
        }
    
    def _format_factual_observations(self, observations: List[Dict[str, Any]]) -> str:
        """Format factual observations for display"""
        if not observations:
            return "<p><em>No verifiable factual observations available from current data sources.</em></p>"
        
        formatted = []
        for obs in observations:
            evidence_level = obs.get("evidence_level", "unverified")
            formatted.append(f"""
            <div class="evidence-item">
                <strong>Observation:</strong> {obs.get('observation', 'N/A')}<br>
                <strong>Evidence Level:</strong> <span class="evidence-level evidence-{evidence_level}">{evidence_level}</span><br>
                <strong>Verification Method:</strong> {obs.get('verification_method', 'N/A')}<br>
                <strong>Source Types:</strong> {', '.join(obs.get('source_types', []))}
            </div>
            """)
        
        return ''.join(formatted)
    
    def _format_evidence_sources(self, sources: List[Any]) -> str:
        """Format evidence sources for display"""
        if not sources:
            return "<p><em>No evidence sources available.</em></p>"
        
        formatted = []
        for source in sources:
            if hasattr(source, 'source_name'):
                reliability = getattr(source, 'reliability_score', 0) * 100
                formatted.append(f"""
                <div class="source-item">
                    <strong>{source.source_name}</strong> ({source.source_type.value})<br>
                    Reliability: {reliability:.0f}% | 
                    Accessed: {source.date_accessed.strftime('%Y-%m-%d')}<br>
                    <small>Data Points: {len(source.data_points)} | Status: {source.verification_status.value}</small>
                </div>
                """)
        
        return ''.join(formatted) if formatted else "<p><em>Source details not available.</em></p>"
    
    def _format_pattern_analysis(self, pattern_data: Dict[str, Any]) -> str:
        """Format pattern analysis for display"""
        if not pattern_data:
            return "<p><em>No pattern analysis available.</em></p>"
        
        patterns = pattern_data.get("patterns_detected", [])
        limitations = pattern_data.get("limitations", [])
        
        formatted = []
        for pattern in patterns:
            formatted.append(f"""
            <div class="evidence-item">
                <strong>Pattern:</strong> {pattern.get('pattern', 'N/A')}<br>
                <strong>Evidence Strength:</strong> {pattern.get('evidence_strength', 'N/A')}<br>
                <strong>Caveat:</strong> <em>{pattern.get('caveat', 'N/A')}</em>
            </div>
            """)
        
        if limitations:
            formatted.append("<div class='limitation-box'><h4>Pattern Analysis Limitations:</h4><ul>")
            for limitation in limitations:
                formatted.append(f"<li>{limitation}</li>")
            formatted.append("</ul></div>")
        
        return ''.join(formatted)
    
    def _format_risk_indicators(self, indicators: List[Dict[str, Any]]) -> str:
        """Format risk indicators for display"""
        if not indicators:
            return "<p><em>No specific risk indicators identified in available data.</em></p>"
        
        formatted = []
        for indicator in indicators:
            risk_level = indicator.get('risk_level', 'unknown')
            formatted.append(f"""
            <div class="evidence-item">
                <strong>Indicator:</strong> {indicator.get('indicator', 'N/A')}<br>
                <strong>Risk Level:</strong> {risk_level.title()}<br>
                <strong>Evidence:</strong> {indicator.get('evidence', 'N/A')}<br>
                <strong>Context:</strong> <em>{indicator.get('context', 'N/A')}</em>
            </div>
            """)
        
        return ''.join(formatted)
    
    def _format_information_gaps(self, gaps: List[str]) -> str:
        """Format information gaps for display"""
        if not gaps:
            return "<p><em>No significant information gaps identified.</em></p>"
        
        formatted = ["<ul>"]
        for gap in gaps:
            formatted.append(f"<li>{gap}</li>")
        formatted.append("</ul>")
        
        return ''.join(formatted)
    
    def _format_alternative_explanations(self, explanations: List[str]) -> str:
        """Format alternative explanations for display"""
        if not explanations:
            return "<p><em>No alternative explanations provided.</em></p>"
        
        formatted = []
        for explanation in explanations:
            formatted.append(f'<div class="alternative-explanation">• {explanation}</div>')
        
        return ''.join(formatted)
    
    def _format_verification_recommendations(self, recommendations: List[str]) -> str:
        """Format verification recommendations for display"""
        if not recommendations:
            return "<p><em>No specific verification recommendations available.</em></p>"
        
        formatted = []
        for recommendation in recommendations:
            formatted.append(f'<div class="verification-recommendation">✓ {recommendation}</div>')
        
        return ''.join(formatted)
    
    def _format_verification_methods(self) -> str:
        """Format verification methods and APIs used"""
        apis_used = [
            "WHOIS Database Queries",
            "SSL Certificate Analysis",
            "Domain Reputation Services",
            "Public Business Records",
            "Fraud Database Checks",
            "Technical Infrastructure Analysis"
        ]
        
        formatted = ["<ul>"]
        for api in apis_used:
            formatted.append(f"<li>{api}</li>")
        formatted.append("</ul>")
        
        # Add API sources reference
        formatted.append("""
        <p><small><strong>Note:</strong> Analysis uses only publicly available APIs and databases. 
        See our <a href="/api/data-sources">Data Sources Documentation</a> for complete list of verification methods.</small></p>
        """)
        
        return ''.join(formatted)
    
    def _get_ethical_use_disclaimer(self) -> str:
        """Get ethical use disclaimer"""
        return """
<strong>Ethical Use Requirements:</strong>
<ul>
    <li>This report must be used only for legitimate fraud prevention and protection purposes</li>
    <li>Do not make public accusations or defamatory statements based solely on this analysis</li>
    <li>Consider the potential impact on individuals and businesses before taking action</li>
    <li>Independently verify all information through appropriate professional channels</li>
    <li>Respect privacy rights and avoid harassment or stalking behaviors</li>
    <li>Consult with legal professionals before taking any legal action</li>
    <li>Report suspected misuse of this platform to our ethics team</li>
</ul>
<p><strong>Remember:</strong> This analysis presents evidence and observations, not definitive proof. 
Alternative explanations may exist for all findings. Use this information responsibly and ethically.</p>
"""

# Initialize global instance
evidence_based_templates = EvidenceBasedReportTemplates()

