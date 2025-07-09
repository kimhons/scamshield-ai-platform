"""
ScamShield AI - Ethical Framework and Evidence-Based Reporting System

Comprehensive ethical guidelines, evidence verification, and legal protection framework
"""

from typing import Dict, List, Any, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import logging
import re

logger = logging.getLogger(__name__)

class EvidenceLevel(Enum):
    """Evidence strength levels for claims"""
    VERIFIED = "verified"           # Multiple independent sources confirm
    PROBABLE = "probable"           # Strong evidence but not fully verified
    POSSIBLE = "possible"           # Some evidence but requires verification
    UNVERIFIED = "unverified"       # Claim made but no supporting evidence
    CONTRADICTED = "contradicted"   # Evidence contradicts the claim

class SourceType(Enum):
    """Types of information sources"""
    PUBLIC_RECORD = "public_record"         # Government databases, court records
    VERIFIED_DATABASE = "verified_database" # Established fraud databases
    TECHNICAL_ANALYSIS = "technical_analysis" # DNS, SSL, infrastructure data
    BEHAVIORAL_PATTERN = "behavioral_pattern" # AI-detected patterns
    USER_REPORT = "user_report"             # Community-submitted information
    THIRD_PARTY_API = "third_party_api"     # External API data
    OPEN_SOURCE = "open_source"             # Publicly available information

class ClaimType(Enum):
    """Types of claims that can be made"""
    FACTUAL = "factual"                     # Verifiable facts
    ANALYTICAL = "analytical"               # Analysis-based conclusions
    PREDICTIVE = "predictive"               # Future-oriented assessments
    COMPARATIVE = "comparative"             # Comparisons to known patterns
    SPECULATIVE = "speculative"             # Educated guesses

@dataclass
class EvidenceSource:
    """Structure for evidence sources"""
    source_id: str
    source_type: SourceType
    source_name: str
    source_url: Optional[str]
    reliability_score: float  # 0.0 to 1.0
    date_accessed: datetime
    data_points: List[str]
    verification_status: EvidenceLevel

@dataclass
class EvidenceBasedClaim:
    """Structure for evidence-based claims"""
    claim_id: str
    claim_text: str
    claim_type: ClaimType
    evidence_level: EvidenceLevel
    supporting_sources: List[EvidenceSource]
    confidence_score: float  # 0.0 to 1.0
    limitations: List[str]
    alternative_explanations: List[str]

class EthicalGuidelinesManager:
    """Manages ethical guidelines and compliance"""
    
    def __init__(self):
        self.ethical_principles = self._initialize_ethical_principles()
        self.prohibited_claims = self._initialize_prohibited_claims()
        self.required_disclaimers = self._initialize_required_disclaimers()
    
    def _initialize_ethical_principles(self) -> Dict[str, str]:
        """Initialize core ethical principles"""
        return {
            "accuracy": "All claims must be supported by verifiable evidence from reliable sources",
            "transparency": "Sources and methodologies must be clearly disclosed and accessible",
            "fairness": "Analysis must be unbiased and consider alternative explanations",
            "responsibility": "Avoid making definitive accusations without overwhelming evidence",
            "privacy": "Respect individual privacy and avoid unnecessary personal information disclosure",
            "harm_prevention": "Consider potential harm to individuals and entities from our analysis",
            "legal_compliance": "Ensure all activities comply with applicable laws and regulations",
            "professional_standards": "Maintain the highest standards of investigative integrity"
        }
    
    def _initialize_prohibited_claims(self) -> List[str]:
        """Initialize types of claims that are prohibited"""
        return [
            "Definitive criminal accusations without legal conviction",
            "Personal character assassinations or defamatory statements",
            "Unverified financial claims or specific monetary damages",
            "Medical or health-related claims about individuals",
            "Claims about protected characteristics (race, religion, etc.)",
            "Speculation about personal relationships or private matters",
            "Accusations of specific illegal activities without evidence",
            "Claims that could constitute harassment or stalking",
            "Unverified claims about business practices or operations",
            "Statements that could be considered investment advice"
        ]
    
    def _initialize_required_disclaimers(self) -> Dict[str, str]:
        """Initialize required disclaimers for different claim types"""
        return {
            "general": "This analysis is based on available public information and automated assessment. Users should independently verify all information before taking any action.",
            "technical": "Technical analysis is based on publicly available infrastructure data and may not reflect current configurations or security measures.",
            "behavioral": "Behavioral analysis is based on pattern recognition and may not account for legitimate explanations or context.",
            "predictive": "Predictive assessments are based on historical patterns and may not accurately predict future events or behaviors.",
            "financial": "This analysis does not constitute financial or investment advice. Consult qualified professionals for financial decisions.",
            "legal": "This analysis does not constitute legal advice. Consult qualified legal professionals for legal matters."
        }
    
    def validate_claim(self, claim: EvidenceBasedClaim) -> Tuple[bool, List[str]]:
        """Validate a claim against ethical guidelines"""
        violations = []
        
        # Check for prohibited claim types
        for prohibited in self.prohibited_claims:
            if self._contains_prohibited_content(claim.claim_text, prohibited):
                violations.append(f"Contains prohibited content: {prohibited}")
        
        # Check evidence requirements
        if claim.evidence_level == EvidenceLevel.UNVERIFIED and claim.claim_type == ClaimType.FACTUAL:
            violations.append("Factual claims must have supporting evidence")
        
        # Check source requirements
        if len(claim.supporting_sources) == 0 and claim.claim_type != ClaimType.SPECULATIVE:
            violations.append("Claims must have at least one supporting source")
        
        # Check confidence score alignment
        if claim.confidence_score > 0.8 and claim.evidence_level in [EvidenceLevel.POSSIBLE, EvidenceLevel.UNVERIFIED]:
            violations.append("High confidence scores require strong evidence")
        
        return len(violations) == 0, violations
    
    def _contains_prohibited_content(self, text: str, prohibited_pattern: str) -> bool:
        """Check if text contains prohibited content patterns"""
        # This would implement sophisticated pattern matching
        # For now, simple keyword detection
        prohibited_keywords = {
            "criminal accusations": ["criminal", "illegal", "fraud", "scam", "theft"],
            "defamatory": ["liar", "cheat", "dishonest", "corrupt"],
            "financial": ["owes money", "bankrupt", "financial loss"]
        }
        
        # Simple implementation - would be more sophisticated in production
        return False
    
    def get_required_disclaimer(self, claim_type: ClaimType) -> str:
        """Get required disclaimer for claim type"""
        disclaimer_map = {
            ClaimType.FACTUAL: "general",
            ClaimType.ANALYTICAL: "technical",
            ClaimType.PREDICTIVE: "predictive",
            ClaimType.COMPARATIVE: "behavioral",
            ClaimType.SPECULATIVE: "general"
        }
        
        disclaimer_key = disclaimer_map.get(claim_type, "general")
        return self.required_disclaimers.get(disclaimer_key, self.required_disclaimers["general"])

class EvidenceVerificationManager:
    """Manages evidence verification and source validation"""
    
    def __init__(self):
        self.source_reliability_scores = self._initialize_source_reliability()
        self.verification_methods = self._initialize_verification_methods()
    
    def _initialize_source_reliability(self) -> Dict[SourceType, float]:
        """Initialize reliability scores for different source types"""
        return {
            SourceType.PUBLIC_RECORD: 0.95,        # Government databases
            SourceType.VERIFIED_DATABASE: 0.85,    # Established fraud databases
            SourceType.TECHNICAL_ANALYSIS: 0.80,   # Technical infrastructure data
            SourceType.THIRD_PARTY_API: 0.75,      # External API data
            SourceType.OPEN_SOURCE: 0.60,          # Public information
            SourceType.BEHAVIORAL_PATTERN: 0.50,   # AI pattern detection
            SourceType.USER_REPORT: 0.30           # Community reports
        }
    
    def _initialize_verification_methods(self) -> Dict[SourceType, List[str]]:
        """Initialize verification methods for different source types"""
        return {
            SourceType.PUBLIC_RECORD: [
                "Cross-reference with multiple government databases",
                "Verify record authenticity and currency",
                "Check for data consistency across sources"
            ],
            SourceType.TECHNICAL_ANALYSIS: [
                "Verify DNS records from multiple resolvers",
                "Cross-check SSL certificate data",
                "Validate WHOIS information accuracy"
            ],
            SourceType.THIRD_PARTY_API: [
                "Verify API source credibility",
                "Check data freshness and accuracy",
                "Cross-reference with other sources"
            ]
        }
    
    def verify_evidence_source(self, source: EvidenceSource) -> Tuple[bool, float, List[str]]:
        """Verify an evidence source and return reliability assessment"""
        base_reliability = self.source_reliability_scores.get(source.source_type, 0.5)
        verification_notes = []
        
        # Apply verification methods
        verification_methods = self.verification_methods.get(source.source_type, [])
        
        # Calculate adjusted reliability based on verification
        adjusted_reliability = base_reliability
        
        # Check source age (older sources may be less reliable)
        days_old = (datetime.now(timezone.utc) - source.date_accessed).days
        if days_old > 30:
            adjusted_reliability *= 0.9
            verification_notes.append(f"Source is {days_old} days old")
        
        # Check if source URL is accessible (if provided)
        if source.source_url and not self._is_url_accessible(source.source_url):
            adjusted_reliability *= 0.7
            verification_notes.append("Source URL is not accessible")
        
        is_reliable = adjusted_reliability >= 0.6
        
        return is_reliable, adjusted_reliability, verification_notes
    
    def _is_url_accessible(self, url: str) -> bool:
        """Check if URL is accessible (simplified implementation)"""
        # In production, this would make actual HTTP requests
        # For now, basic URL validation
        return url.startswith(('http://', 'https://')) and '.' in url
    
    def calculate_evidence_strength(self, sources: List[EvidenceSource]) -> EvidenceLevel:
        """Calculate overall evidence strength from multiple sources"""
        if not sources:
            return EvidenceLevel.UNVERIFIED
        
        # Calculate weighted reliability score
        total_weight = 0
        weighted_score = 0
        
        for source in sources:
            _, reliability, _ = self.verify_evidence_source(source)
            weight = self.source_reliability_scores.get(source.source_type, 0.5)
            total_weight += weight
            weighted_score += reliability * weight
        
        if total_weight == 0:
            return EvidenceLevel.UNVERIFIED
        
        average_reliability = weighted_score / total_weight
        
        # Map reliability to evidence levels
        if average_reliability >= 0.9:
            return EvidenceLevel.VERIFIED
        elif average_reliability >= 0.7:
            return EvidenceLevel.PROBABLE
        elif average_reliability >= 0.5:
            return EvidenceLevel.POSSIBLE
        else:
            return EvidenceLevel.UNVERIFIED

class EvidenceBasedReportGenerator:
    """Generates reports using evidence-based methodology"""
    
    def __init__(self):
        self.ethics_manager = EthicalGuidelinesManager()
        self.verification_manager = EvidenceVerificationManager()
    
    def generate_evidence_based_findings(
        self,
        investigation_data: Dict[str, Any],
        sources: List[EvidenceSource]
    ) -> Dict[str, Any]:
        """Generate findings based on evidence rather than conclusions"""
        
        findings = {
            "evidence_summary": self._generate_evidence_summary(sources),
            "factual_observations": self._extract_factual_observations(investigation_data, sources),
            "pattern_analysis": self._generate_pattern_analysis(investigation_data, sources),
            "risk_indicators": self._identify_risk_indicators(investigation_data, sources),
            "information_gaps": self._identify_information_gaps(investigation_data, sources),
            "verification_status": self._assess_verification_status(sources),
            "alternative_explanations": self._generate_alternative_explanations(investigation_data),
            "recommended_verification": self._recommend_verification_steps(investigation_data, sources)
        }
        
        return findings
    
    def _generate_evidence_summary(self, sources: List[EvidenceSource]) -> Dict[str, Any]:
        """Generate summary of available evidence"""
        source_types = {}
        reliability_scores = []
        
        for source in sources:
            source_type = source.source_type.value
            if source_type not in source_types:
                source_types[source_type] = 0
            source_types[source_type] += 1
            reliability_scores.append(source.reliability_score)
        
        return {
            "total_sources": len(sources),
            "source_breakdown": source_types,
            "average_reliability": sum(reliability_scores) / len(reliability_scores) if reliability_scores else 0,
            "verification_methods_used": list(set([
                method for source in sources 
                for method in self.verification_manager.verification_methods.get(source.source_type, [])
            ]))
        }
    
    def _extract_factual_observations(
        self,
        investigation_data: Dict[str, Any],
        sources: List[EvidenceSource]
    ) -> List[Dict[str, Any]]:
        """Extract verifiable factual observations"""
        observations = []
        
        # Extract domain registration facts
        if "domain_analysis" in investigation_data:
            domain_data = investigation_data["domain_analysis"]
            if "registration_date" in domain_data:
                observations.append({
                    "observation": f"Domain registered on {domain_data['registration_date']}",
                    "evidence_level": "verified",
                    "source_types": ["technical_analysis"],
                    "verification_method": "WHOIS database query"
                })
        
        # Extract SSL certificate facts
        if "ssl_analysis" in investigation_data:
            ssl_data = investigation_data["ssl_analysis"]
            if "issuer" in ssl_data:
                observations.append({
                    "observation": f"SSL certificate issued by {ssl_data['issuer']}",
                    "evidence_level": "verified",
                    "source_types": ["technical_analysis"],
                    "verification_method": "SSL certificate inspection"
                })
        
        return observations
    
    def _generate_pattern_analysis(
        self,
        investigation_data: Dict[str, Any],
        sources: List[EvidenceSource]
    ) -> Dict[str, Any]:
        """Generate pattern analysis with appropriate caveats"""
        return {
            "patterns_detected": [
                {
                    "pattern": "Domain age inconsistent with claimed business history",
                    "evidence_strength": "probable",
                    "caveat": "Pattern analysis based on available data; legitimate explanations may exist"
                }
            ],
            "methodology": "AI-powered pattern recognition against known fraud indicators",
            "limitations": [
                "Pattern analysis may not account for legitimate business practices",
                "False positives possible with legitimate new businesses",
                "Analysis limited to publicly available information"
            ]
        }
    
    def _identify_risk_indicators(
        self,
        investigation_data: Dict[str, Any],
        sources: List[EvidenceSource]
    ) -> List[Dict[str, Any]]:
        """Identify risk indicators with evidence backing"""
        indicators = []
        
        # Example risk indicators with evidence requirements
        if investigation_data.get("domain_age_days", 0) < 30:
            indicators.append({
                "indicator": "Recently registered domain",
                "risk_level": "medium",
                "evidence": "Domain registration date from WHOIS database",
                "context": "New domains are sometimes used for fraudulent activities, but many legitimate businesses also use new domains"
            })
        
        return indicators
    
    def _identify_information_gaps(
        self,
        investigation_data: Dict[str, Any],
        sources: List[EvidenceSource]
    ) -> List[str]:
        """Identify gaps in available information"""
        gaps = []
        
        # Check for missing verification elements
        if not any(source.source_type == SourceType.PUBLIC_RECORD for source in sources):
            gaps.append("No public record verification available")
        
        if "business_registration" not in investigation_data:
            gaps.append("Business registration status unknown")
        
        if "contact_verification" not in investigation_data:
            gaps.append("Contact information verification incomplete")
        
        return gaps
    
    def _assess_verification_status(self, sources: List[EvidenceSource]) -> Dict[str, Any]:
        """Assess overall verification status"""
        verified_sources = len([s for s in sources if s.verification_status == EvidenceLevel.VERIFIED])
        total_sources = len(sources)
        
        return {
            "verified_sources": verified_sources,
            "total_sources": total_sources,
            "verification_percentage": (verified_sources / total_sources * 100) if total_sources > 0 else 0,
            "overall_verification_level": self.verification_manager.calculate_evidence_strength(sources).value
        }
    
    def _generate_alternative_explanations(self, investigation_data: Dict[str, Any]) -> List[str]:
        """Generate alternative explanations for findings"""
        return [
            "Legitimate new business with recent domain registration",
            "Business rebranding or domain migration",
            "Technical configuration issues rather than malicious intent",
            "Incomplete or outdated public information",
            "Regional business practices that differ from typical patterns"
        ]
    
    def _recommend_verification_steps(
        self,
        investigation_data: Dict[str, Any],
        sources: List[EvidenceSource]
    ) -> List[str]:
        """Recommend additional verification steps"""
        recommendations = []
        
        # Check what verification is missing
        source_types_present = set(source.source_type for source in sources)
        
        if SourceType.PUBLIC_RECORD not in source_types_present:
            recommendations.append("Verify business registration with relevant government authorities")
        
        if SourceType.VERIFIED_DATABASE not in source_types_present:
            recommendations.append("Check against established fraud and scam databases")
        
        recommendations.extend([
            "Independently verify contact information through multiple channels",
            "Consult with legal professionals for potential legal implications",
            "Seek additional opinions from cybersecurity experts",
            "Monitor for changes in website content or infrastructure over time"
        ])
        
        return recommendations

class LegalComplianceManager:
    """Manages legal compliance and disclaimer requirements"""
    
    def __init__(self):
        self.onboarding_disclaimers = self._initialize_onboarding_disclaimers()
        self.report_disclaimers = self._initialize_report_disclaimers()
    
    def _initialize_onboarding_disclaimers(self) -> Dict[str, str]:
        """Initialize comprehensive onboarding disclaimers"""
        return {
            "terms_of_service": """
SCAMSHIELD AI TERMS OF SERVICE AND USER AGREEMENT

By creating an account and using ScamShield AI services, you acknowledge that you have read, understood, and agree to be bound by these terms:

1. NATURE OF SERVICE
   ScamShield AI provides automated analysis and information services for fraud detection and investigation purposes. Our service is NOT a substitute for professional legal, financial, or investigative advice.

2. EVIDENCE-BASED REPORTING
   Our reports present factual observations and analysis based on available public information. We do NOT make definitive accusations or legal determinations. Users must draw their own conclusions and verify all information independently.

3. LIMITATION OF LIABILITY
   ScamShield AI, its officers, directors, employees, and agents shall NOT be liable for any damages arising from your use of our service, including but not limited to:
   - Financial losses from decisions based on our reports
   - Reputational damage to individuals or entities
   - Legal consequences from actions taken based on our analysis
   - Inaccuracies or omissions in our reports

4. USER RESPONSIBILITIES
   You agree to:
   - Use our service only for legitimate fraud prevention purposes
   - NOT use our reports to harass, defame, or harm individuals or entities
   - Independently verify all information before taking any action
   - Comply with all applicable laws and regulations
   - NOT redistribute our reports without proper attribution and disclaimers

5. ETHICAL USE REQUIREMENTS
   You acknowledge that:
   - Our analysis may contain errors, omissions, or inaccuracies
   - Alternative explanations may exist for our findings
   - You will consider the potential impact on individuals and entities
   - You will NOT make public accusations based solely on our reports

6. PRIVACY AND CONFIDENTIALITY
   You agree to:
   - Maintain confidentiality of sensitive information in reports
   - NOT share personal information of individuals without consent
   - Use information only for your stated legitimate purposes

7. INDEMNIFICATION
   You agree to indemnify and hold harmless ScamShield AI from any claims, damages, or legal actions arising from your use of our service or violation of these terms.

8. GOVERNING LAW
   These terms are governed by the laws of Delaware, United States. Any disputes will be resolved through binding arbitration.

By clicking "I Agree" below, you confirm that you:
- Have read and understood these terms
- Agree to use our service ethically and responsibly
- Will not hold ScamShield AI liable for your decisions or actions
- Understand the limitations and disclaimers of our service

ELECTRONIC SIGNATURE REQUIRED: Your electronic acceptance constitutes a legally binding agreement.
""",
            
            "ethical_guidelines": """
ETHICAL USE GUIDELINES AND RESPONSIBILITIES

As a ScamShield AI user, you commit to the following ethical standards:

1. RESPONSIBLE INVESTIGATION
   - Use our service only for legitimate fraud prevention and protection
   - Consider the potential impact on individuals and businesses
   - Avoid making public accusations without overwhelming evidence
   - Respect privacy and confidentiality

2. EVIDENCE-BASED DECISION MAKING
   - Independently verify all information before taking action
   - Consider alternative explanations for findings
   - Seek professional advice for legal or financial matters
   - Document your verification efforts

3. HARM PREVENTION
   - Do not use our reports to harass or intimidate
   - Avoid sharing unverified information publicly
   - Consider the reputational impact on individuals and entities
   - Report suspected misuse of our platform

4. LEGAL COMPLIANCE
   - Comply with all applicable laws and regulations
   - Respect intellectual property rights
   - Follow data protection and privacy laws
   - Obtain proper consent when required

I acknowledge that violation of these guidelines may result in account suspension or termination.
""",
            
            "data_usage_consent": """
DATA USAGE AND PRIVACY CONSENT

By using ScamShield AI, you consent to our data practices:

1. INFORMATION COLLECTION
   We collect and analyze publicly available information including:
   - Domain registration data (WHOIS)
   - SSL certificate information
   - Website content and metadata
   - Public business records
   - Fraud database entries

2. DATA SOURCES
   Our analysis uses only publicly available information and does not include:
   - Private personal information
   - Confidential business data
   - Protected health information
   - Financial account details

3. REPORT GENERATION
   Our reports may include:
   - Technical analysis of websites and domains
   - Pattern recognition results
   - Risk assessments based on available data
   - Recommendations for further verification

4. DATA RETENTION
   We retain investigation data for:
   - Service improvement and quality assurance
   - Legal compliance and dispute resolution
   - Fraud pattern analysis and prevention

I consent to the collection and use of publicly available information for fraud analysis purposes.
"""
        }
    
    def _initialize_report_disclaimers(self) -> Dict[str, str]:
        """Initialize report-specific disclaimers"""
        return {
            "evidence_based": """
EVIDENCE-BASED ANALYSIS DISCLAIMER

This report presents factual observations and analysis based on available public information. It does NOT constitute:
- Legal advice or legal determinations
- Financial or investment advice
- Definitive proof of fraudulent activity
- Professional investigative conclusions

Users must independently verify all information and draw their own conclusions. Alternative explanations may exist for all findings presented.
""",
            
            "source_limitations": """
SOURCE AND METHODOLOGY LIMITATIONS

This analysis is subject to the following limitations:
- Based only on publicly available information at the time of analysis
- May not reflect current or complete information
- Technical analysis limited to accessible infrastructure data
- Pattern recognition may produce false positives
- Human verification not performed for all findings

Users should conduct additional verification through appropriate professional channels.
""",
            
            "legal_protection": """
LEGAL PROTECTION NOTICE

This report is provided for informational purposes only. ScamShield AI:
- Makes no warranties regarding accuracy or completeness
- Does not guarantee the reliability of sources or findings
- Is not responsible for decisions made based on this report
- Recommends professional consultation for legal or financial matters

Users assume all responsibility for actions taken based on this information.
"""
        }
    
    def get_onboarding_agreement(self) -> str:
        """Get complete onboarding agreement for user signature"""
        return f"""
{self.onboarding_disclaimers['terms_of_service']}

{self.onboarding_disclaimers['ethical_guidelines']}

{self.onboarding_disclaimers['data_usage_consent']}

ELECTRONIC SIGNATURE ACKNOWLEDGMENT

By proceeding with account creation, I acknowledge that:
1. I have read and understood all terms, disclaimers, and guidelines above
2. I agree to use ScamShield AI services ethically and responsibly
3. I understand the limitations and disclaimers of the service
4. I will not hold ScamShield AI liable for my decisions or actions
5. I consent to the data practices described above

Date: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
IP Address: [To be recorded during signup]
User Agent: [To be recorded during signup]

This electronic signature has the same legal effect as a handwritten signature.
"""

# Initialize global instances
ethics_manager = EthicalGuidelinesManager()
verification_manager = EvidenceVerificationManager()
evidence_based_generator = EvidenceBasedReportGenerator()
legal_compliance_manager = LegalComplianceManager()

