"""
ScamShield AI - Public Data APIs and Verification Sources

Comprehensive list of public APIs and data sources for fraud investigation and verification
"""

from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass

class APICategory(Enum):
    """Categories of public APIs"""
    DOMAIN_INTELLIGENCE = "domain_intelligence"
    BUSINESS_RECORDS = "business_records"
    FRAUD_DATABASES = "fraud_databases"
    FINANCIAL_DATA = "financial_data"
    SOCIAL_MEDIA = "social_media"
    TECHNICAL_ANALYSIS = "technical_analysis"
    GOVERNMENT_DATA = "government_data"
    THREAT_INTELLIGENCE = "threat_intelligence"
    REPUTATION_SERVICES = "reputation_services"
    BLOCKCHAIN_ANALYSIS = "blockchain_analysis"

@dataclass
class PublicAPI:
    """Structure for public API information"""
    name: str
    category: APICategory
    description: str
    base_url: str
    documentation_url: str
    authentication_required: bool
    rate_limits: str
    cost: str
    reliability_score: float  # 0.0 to 1.0
    data_types: List[str]
    use_cases: List[str]
    legal_considerations: str

class PublicDataAPIs:
    """Comprehensive collection of public data APIs for fraud investigation"""
    
    def __init__(self):
        self.apis = self._initialize_public_apis()
    
    def _initialize_public_apis(self) -> Dict[str, PublicAPI]:
        """Initialize comprehensive list of public APIs"""
        return {
            # DOMAIN INTELLIGENCE APIs
            "whois_api": PublicAPI(
                name="WHOIS API",
                category=APICategory.DOMAIN_INTELLIGENCE,
                description="Domain registration information and ownership details",
                base_url="https://www.whoisxmlapi.com/",
                documentation_url="https://www.whoisxmlapi.com/documentation/",
                authentication_required=True,
                rate_limits="1000 requests/month (free tier)",
                cost="Free tier available, paid plans from $99/month",
                reliability_score=0.95,
                data_types=["domain_registration", "registrant_info", "nameservers", "creation_date"],
                use_cases=["Domain age verification", "Registrant identification", "Infrastructure analysis"],
                legal_considerations="Public WHOIS data, privacy laws may apply to personal information"
            ),
            
            "virustotal_api": PublicAPI(
                name="VirusTotal API",
                category=APICategory.THREAT_INTELLIGENCE,
                description="URL and domain reputation analysis from multiple security vendors",
                base_url="https://www.virustotal.com/vtapi/v2/",
                documentation_url="https://developers.virustotal.com/reference",
                authentication_required=True,
                rate_limits="4 requests/minute (free), 1000/minute (premium)",
                cost="Free tier available, premium from $180/month",
                reliability_score=0.90,
                data_types=["malware_detection", "url_analysis", "domain_reputation", "file_analysis"],
                use_cases=["Malware detection", "URL safety analysis", "Domain reputation check"],
                legal_considerations="Terms of service restrict commercial use of free tier"
            ),
            
            "urlvoid_api": PublicAPI(
                name="URLVoid API",
                category=APICategory.REPUTATION_SERVICES,
                description="Website reputation and safety analysis",
                base_url="https://www.urlvoid.com/api1000/",
                documentation_url="https://www.urlvoid.com/api/",
                authentication_required=True,
                rate_limits="1000 requests/month (free)",
                cost="Free tier available, paid plans from $9.95/month",
                reliability_score=0.85,
                data_types=["website_reputation", "blacklist_status", "safety_analysis"],
                use_cases=["Website safety verification", "Blacklist checking", "Reputation analysis"],
                legal_considerations="Standard API terms, no special restrictions"
            ),
            
            # BUSINESS RECORDS APIs
            "opencorporates_api": PublicAPI(
                name="OpenCorporates API",
                category=APICategory.BUSINESS_RECORDS,
                description="Global company database with business registration information",
                base_url="https://api.opencorporates.com/",
                documentation_url="https://api.opencorporates.com/documentation/",
                authentication_required=True,
                rate_limits="500 requests/month (free), higher limits for paid",
                cost="Free tier available, paid plans from $99/month",
                reliability_score=0.90,
                data_types=["company_registration", "officer_information", "filing_history", "addresses"],
                use_cases=["Business verification", "Corporate structure analysis", "Officer identification"],
                legal_considerations="Public record data, some jurisdictions may have restrictions"
            ),
            
            "sec_edgar_api": PublicAPI(
                name="SEC EDGAR API",
                category=APICategory.BUSINESS_RECORDS,
                description="US Securities and Exchange Commission filings database",
                base_url="https://www.sec.gov/edgar/",
                documentation_url="https://www.sec.gov/edgar/sec-api-documentation",
                authentication_required=False,
                rate_limits="10 requests/second",
                cost="Free",
                reliability_score=0.95,
                data_types=["sec_filings", "financial_statements", "insider_trading", "company_facts"],
                use_cases=["Public company verification", "Financial analysis", "Regulatory compliance"],
                legal_considerations="Public domain data, must comply with SEC fair access rules"
            ),
            
            # FRAUD DATABASES APIs
            "scamadviser_api": PublicAPI(
                name="ScamAdviser API",
                category=APICategory.FRAUD_DATABASES,
                description="Website trustworthiness and scam detection database",
                base_url="https://www.scamadviser.com/api/",
                documentation_url="https://www.scamadviser.com/api-documentation",
                authentication_required=True,
                rate_limits="1000 requests/month (free)",
                cost="Free tier available, enterprise plans available",
                reliability_score=0.80,
                data_types=["trust_score", "scam_reports", "website_analysis", "risk_factors"],
                use_cases=["Scam detection", "Website trustworthiness", "Risk assessment"],
                legal_considerations="Proprietary database, terms of service apply"
            ),
            
            "better_business_bureau_api": PublicAPI(
                name="Better Business Bureau API",
                category=APICategory.BUSINESS_RECORDS,
                description="Business accreditation and complaint information",
                base_url="https://www.bbb.org/",
                documentation_url="https://www.bbb.org/api/",
                authentication_required=True,
                rate_limits="Varies by plan",
                cost="Contact for pricing",
                reliability_score=0.85,
                data_types=["business_rating", "complaints", "accreditation_status", "reviews"],
                use_cases=["Business reputation verification", "Complaint analysis", "Accreditation status"],
                legal_considerations="BBB terms of service, may require business relationship"
            ),
            
            # TECHNICAL ANALYSIS APIs
            "shodan_api": PublicAPI(
                name="Shodan API",
                category=APICategory.TECHNICAL_ANALYSIS,
                description="Internet-connected device and service discovery",
                base_url="https://api.shodan.io/",
                documentation_url="https://developer.shodan.io/api",
                authentication_required=True,
                rate_limits="100 results/month (free), unlimited for paid",
                cost="Free tier available, paid plans from $59/month",
                reliability_score=0.90,
                data_types=["open_ports", "services", "vulnerabilities", "geolocation", "ssl_certificates"],
                use_cases=["Infrastructure analysis", "Security assessment", "Service identification"],
                legal_considerations="Must comply with terms of service, no unauthorized access"
            ),
            
            "censys_api": PublicAPI(
                name="Censys API",
                category=APICategory.TECHNICAL_ANALYSIS,
                description="Internet-wide scanning and certificate transparency data",
                base_url="https://search.censys.io/api/",
                documentation_url="https://search.censys.io/api",
                authentication_required=True,
                rate_limits="1000 requests/month (free)",
                cost="Free tier available, paid plans from $99/month",
                reliability_score=0.90,
                data_types=["ssl_certificates", "host_information", "protocol_analysis", "certificate_transparency"],
                use_cases=["Certificate analysis", "Infrastructure mapping", "Security research"],
                legal_considerations="Academic and research use encouraged, commercial terms available"
            ),
            
            # FINANCIAL DATA APIs
            "alpha_vantage_api": PublicAPI(
                name="Alpha Vantage API",
                category=APICategory.FINANCIAL_DATA,
                description="Stock market and financial data",
                base_url="https://www.alphavantage.co/",
                documentation_url="https://www.alphavantage.co/documentation/",
                authentication_required=True,
                rate_limits="5 requests/minute (free), 75/minute (premium)",
                cost="Free tier available, premium from $49.99/month",
                reliability_score=0.85,
                data_types=["stock_prices", "financial_indicators", "company_overview", "earnings"],
                use_cases=["Public company verification", "Financial analysis", "Market data"],
                legal_considerations="Standard financial data terms, not for high-frequency trading"
            ),
            
            # SOCIAL MEDIA APIs
            "twitter_api": PublicAPI(
                name="Twitter API v2",
                category=APICategory.SOCIAL_MEDIA,
                description="Twitter social media data and analytics",
                base_url="https://api.twitter.com/2/",
                documentation_url="https://developer.twitter.com/en/docs/twitter-api",
                authentication_required=True,
                rate_limits="Varies by endpoint and plan",
                cost="Free tier available, paid plans from $100/month",
                reliability_score=0.85,
                data_types=["tweets", "user_profiles", "engagement_metrics", "trends"],
                use_cases=["Social media verification", "Sentiment analysis", "Account authenticity"],
                legal_considerations="Strict terms of service, privacy considerations for user data"
            ),
            
            # GOVERNMENT DATA APIs
            "usa_gov_api": PublicAPI(
                name="USA.gov APIs",
                category=APICategory.GOVERNMENT_DATA,
                description="US government data and services",
                base_url="https://api.usa.gov/",
                documentation_url="https://api.usa.gov/docs/",
                authentication_required=True,
                rate_limits="1000 requests/hour (free)",
                cost="Free",
                reliability_score=0.95,
                data_types=["government_data", "agency_information", "regulations", "statistics"],
                use_cases=["Government verification", "Regulatory compliance", "Public records"],
                legal_considerations="Public domain data, must comply with government API terms"
            ),
            
            "uk_companies_house_api": PublicAPI(
                name="UK Companies House API",
                category=APICategory.BUSINESS_RECORDS,
                description="UK company registration and filing information",
                base_url="https://api.company-information.service.gov.uk/",
                documentation_url="https://developer-specs.company-information.service.gov.uk/",
                authentication_required=True,
                rate_limits="600 requests/5 minutes",
                cost="Free",
                reliability_score=0.95,
                data_types=["company_profile", "filing_history", "officers", "charges"],
                use_cases=["UK business verification", "Corporate structure analysis", "Compliance checking"],
                legal_considerations="Public record data, UK data protection laws apply"
            ),
            
            # BLOCKCHAIN ANALYSIS APIs
            "blockchain_info_api": PublicAPI(
                name="Blockchain.info API",
                category=APICategory.BLOCKCHAIN_ANALYSIS,
                description="Bitcoin blockchain data and analytics",
                base_url="https://blockchain.info/api/",
                documentation_url="https://www.blockchain.com/api",
                authentication_required=False,
                rate_limits="No official limits, fair use policy",
                cost="Free",
                reliability_score=0.85,
                data_types=["bitcoin_transactions", "addresses", "blocks", "statistics"],
                use_cases=["Cryptocurrency investigation", "Transaction analysis", "Address verification"],
                legal_considerations="Public blockchain data, privacy considerations for analysis"
            ),
            
            "etherscan_api": PublicAPI(
                name="Etherscan API",
                category=APICategory.BLOCKCHAIN_ANALYSIS,
                description="Ethereum blockchain explorer and analytics",
                base_url="https://api.etherscan.io/api/",
                documentation_url="https://docs.etherscan.io/",
                authentication_required=True,
                rate_limits="5 requests/second (free), 100/second (premium)",
                cost="Free tier available, premium plans available",
                reliability_score=0.90,
                data_types=["ethereum_transactions", "smart_contracts", "token_transfers", "gas_prices"],
                use_cases=["Ethereum investigation", "Smart contract analysis", "Token tracking"],
                legal_considerations="Public blockchain data, terms of service for API usage"
            ),
            
            # ADDITIONAL VERIFICATION APIs
            "have_i_been_pwned_api": PublicAPI(
                name="Have I Been Pwned API",
                category=APICategory.THREAT_INTELLIGENCE,
                description="Data breach and password exposure database",
                base_url="https://haveibeenpwned.com/api/v3/",
                documentation_url="https://haveibeenpwned.com/API/v3",
                authentication_required=True,
                rate_limits="1 request/1.5 seconds (free)",
                cost="Free for non-commercial use, $3.50/month for commercial",
                reliability_score=0.95,
                data_types=["data_breaches", "password_exposure", "email_verification"],
                use_cases=["Email verification", "Security assessment", "Breach analysis"],
                legal_considerations="Non-commercial use free, commercial license required"
            ),
            
            "google_safe_browsing_api": PublicAPI(
                name="Google Safe Browsing API",
                category=APICategory.REPUTATION_SERVICES,
                description="Google's database of unsafe web resources",
                base_url="https://safebrowsing.googleapis.com/",
                documentation_url="https://developers.google.com/safe-browsing/",
                authentication_required=True,
                rate_limits="10,000 requests/day (free)",
                cost="Free",
                reliability_score=0.95,
                data_types=["malware_detection", "phishing_detection", "unwanted_software"],
                use_cases=["URL safety verification", "Malware detection", "Phishing identification"],
                legal_considerations="Google API terms of service, privacy policy compliance"
            ),
            
            "ipqualityscore_api": PublicAPI(
                name="IPQualityScore API",
                category=APICategory.REPUTATION_SERVICES,
                description="IP address, email, and phone number fraud detection",
                base_url="https://ipqualityscore.com/api/",
                documentation_url="https://www.ipqualityscore.com/documentation/",
                authentication_required=True,
                rate_limits="5,000 requests/month (free)",
                cost="Free tier available, paid plans from $25/month",
                reliability_score=0.85,
                data_types=["ip_reputation", "email_validation", "phone_validation", "fraud_scoring"],
                use_cases=["Contact verification", "Fraud detection", "Risk assessment"],
                legal_considerations="Standard API terms, privacy compliance required"
            ),
            
            "clearbit_api": PublicAPI(
                name="Clearbit API",
                category=APICategory.BUSINESS_RECORDS,
                description="Company and person data enrichment",
                base_url="https://person.clearbit.com/",
                documentation_url="https://clearbit.com/docs",
                authentication_required=True,
                rate_limits="Varies by plan",
                cost="Contact for pricing, free tier limited",
                reliability_score=0.80,
                data_types=["company_data", "person_data", "technology_stack", "social_profiles"],
                use_cases=["Business verification", "Contact enrichment", "Technology analysis"],
                legal_considerations="Privacy laws apply, terms of service restrictions"
            )
        }
    
    def get_apis_by_category(self, category: APICategory) -> List[PublicAPI]:
        """Get APIs filtered by category"""
        return [api for api in self.apis.values() if api.category == category]
    
    def get_free_apis(self) -> List[PublicAPI]:
        """Get APIs that offer free tiers"""
        return [api for api in self.apis.values() if "free" in api.cost.lower()]
    
    def get_high_reliability_apis(self, min_score: float = 0.85) -> List[PublicAPI]:
        """Get APIs with high reliability scores"""
        return [api for api in self.apis.values() if api.reliability_score >= min_score]
    
    def get_verification_workflow(self, investigation_type: str) -> List[str]:
        """Get recommended API workflow for different investigation types"""
        workflows = {
            "domain_investigation": [
                "whois_api",
                "virustotal_api",
                "urlvoid_api",
                "google_safe_browsing_api",
                "shodan_api"
            ],
            "business_verification": [
                "opencorporates_api",
                "sec_edgar_api",
                "better_business_bureau_api",
                "uk_companies_house_api",
                "clearbit_api"
            ],
            "fraud_detection": [
                "scamadviser_api",
                "virustotal_api",
                "ipqualityscore_api",
                "have_i_been_pwned_api",
                "google_safe_browsing_api"
            ],
            "technical_analysis": [
                "shodan_api",
                "censys_api",
                "virustotal_api",
                "whois_api"
            ],
            "financial_verification": [
                "sec_edgar_api",
                "alpha_vantage_api",
                "opencorporates_api"
            ],
            "cryptocurrency_investigation": [
                "blockchain_info_api",
                "etherscan_api"
            ]
        }
        
        return workflows.get(investigation_type, [])
    
    def get_legal_considerations_summary(self) -> Dict[str, List[str]]:
        """Get summary of legal considerations for API usage"""
        return {
            "data_protection": [
                "Comply with GDPR for EU data subjects",
                "Follow CCPA requirements for California residents",
                "Respect privacy laws in relevant jurisdictions",
                "Obtain consent when required for personal data"
            ],
            "terms_of_service": [
                "Review and comply with each API's terms of service",
                "Respect rate limits and usage restrictions",
                "Understand commercial vs non-commercial use limitations",
                "Maintain proper attribution when required"
            ],
            "data_accuracy": [
                "Verify information from multiple sources when possible",
                "Understand limitations and potential inaccuracies",
                "Document sources and methodologies used",
                "Provide appropriate disclaimers in reports"
            ],
            "ethical_use": [
                "Use APIs only for legitimate fraud prevention purposes",
                "Avoid harassment or stalking behaviors",
                "Respect individual privacy and reputation",
                "Consider potential harm from investigations"
            ]
        }

# Initialize global instance
public_data_apis = PublicDataAPIs()

# Export commonly used API lists
DOMAIN_INTELLIGENCE_APIS = public_data_apis.get_apis_by_category(APICategory.DOMAIN_INTELLIGENCE)
BUSINESS_VERIFICATION_APIS = public_data_apis.get_apis_by_category(APICategory.BUSINESS_RECORDS)
FRAUD_DETECTION_APIS = public_data_apis.get_apis_by_category(APICategory.FRAUD_DATABASES)
FREE_TIER_APIS = public_data_apis.get_free_apis()
HIGH_RELIABILITY_APIS = public_data_apis.get_high_reliability_apis()

# Verification workflows
VERIFICATION_WORKFLOWS = {
    "standard_domain_check": public_data_apis.get_verification_workflow("domain_investigation"),
    "business_verification": public_data_apis.get_verification_workflow("business_verification"),
    "fraud_detection": public_data_apis.get_verification_workflow("fraud_detection"),
    "technical_analysis": public_data_apis.get_verification_workflow("technical_analysis")
}

