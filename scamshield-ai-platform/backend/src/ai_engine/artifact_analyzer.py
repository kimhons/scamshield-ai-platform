"""
Multi-Modal Artifact Analyzer

Analyzes various types of digital artifacts including URLs, images, documents,
emails, social media profiles, and other evidence using specialized techniques
for each artifact type.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
import re
import hashlib
import base64
from datetime import datetime
import json
import whois
import requests
from urllib.parse import urlparse, parse_qs
import dns.resolver
import ssl
import socket
from PIL import Image
import io
import cv2
import numpy as np

from .model_manager_v2 import ModelTier

logger = logging.getLogger(__name__)

class ArtifactType:
    """Supported artifact types"""
    URL = "url"
    EMAIL = "email"
    PHONE = "phone"
    IMAGE = "image"
    DOCUMENT = "document"
    TEXT = "text"
    SOCIAL_MEDIA = "social_media"
    IP_ADDRESS = "ip_address"
    DOMAIN = "domain"
    CRYPTOCURRENCY = "cryptocurrency"
    UNKNOWN = "unknown"

class ArtifactAnalyzer:
    """
    Multi-Modal Artifact Analyzer
    
    Provides comprehensive analysis of digital artifacts using:
    - Technical analysis (domains, IPs, certificates)
    - Content analysis (text, images, documents)
    - Pattern recognition (fraud indicators, behavioral patterns)
    - Intelligence correlation (threat databases, reputation systems)
    """
    
    def __init__(self):
        self.fraud_patterns = self._load_fraud_patterns()
        self.reputation_apis = self._setup_reputation_apis()
        
    def _load_fraud_patterns(self) -> Dict[str, List[str]]:
        """Load known fraud patterns and indicators"""
        return {
            "scam_keywords": [
                "urgent", "immediate action", "verify account", "suspended",
                "click here", "limited time", "act now", "congratulations",
                "winner", "lottery", "inheritance", "prince", "beneficiary",
                "wire transfer", "western union", "bitcoin", "cryptocurrency",
                "investment opportunity", "guaranteed returns", "risk-free"
            ],
            "suspicious_domains": [
                "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly",
                "short.link", "tiny.cc", "is.gd", "buff.ly"
            ],
            "phishing_indicators": [
                "paypal-security", "amazon-verification", "microsoft-support",
                "apple-id-locked", "google-security", "facebook-security",
                "bank-alert", "credit-card-suspended", "account-verification"
            ],
            "social_engineering": [
                "don't tell anyone", "keep this confidential", "secret",
                "exclusive offer", "selected customer", "special invitation",
                "time sensitive", "expires soon", "limited availability"
            ]
        }
    
    def _setup_reputation_apis(self) -> Dict[str, str]:
        """Setup reputation API endpoints"""
        return {
            "virustotal": "https://www.virustotal.com/vtapi/v2/",
            "urlvoid": "https://api.urlvoid.com/1000/",
            "abuseipdb": "https://api.abuseipdb.com/api/v2/",
            "shodan": "https://api.shodan.io/"
        }
    
    async def analyze_artifact(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """
        Analyze a single artifact using appropriate techniques
        
        Args:
            artifact: Artifact data with type and content
            tier: Investigation tier level
            
        Returns:
            Comprehensive analysis results
        """
        
        # Identify artifact type
        artifact_type = self._identify_artifact_type(artifact)
        
        # Base analysis structure
        analysis_result = {
            "artifact_id": self._generate_artifact_id(artifact),
            "type": artifact_type,
            "timestamp": datetime.utcnow().isoformat(),
            "tier": tier.value,
            "risk_score": 0.0,
            "risk_indicators": [],
            "technical_analysis": {},
            "content_analysis": {},
            "reputation_analysis": {},
            "confidence": 0.0
        }
        
        try:
            # Perform type-specific analysis
            if artifact_type == ArtifactType.URL:
                analysis_result.update(await self._analyze_url(artifact, tier))
            elif artifact_type == ArtifactType.EMAIL:
                analysis_result.update(await self._analyze_email(artifact, tier))
            elif artifact_type == ArtifactType.PHONE:
                analysis_result.update(await self._analyze_phone(artifact, tier))
            elif artifact_type == ArtifactType.IMAGE:
                analysis_result.update(await self._analyze_image(artifact, tier))
            elif artifact_type == ArtifactType.DOCUMENT:
                analysis_result.update(await self._analyze_document(artifact, tier))
            elif artifact_type == ArtifactType.TEXT:
                analysis_result.update(await self._analyze_text(artifact, tier))
            elif artifact_type == ArtifactType.SOCIAL_MEDIA:
                analysis_result.update(await self._analyze_social_media(artifact, tier))
            elif artifact_type == ArtifactType.IP_ADDRESS:
                analysis_result.update(await self._analyze_ip_address(artifact, tier))
            elif artifact_type == ArtifactType.DOMAIN:
                analysis_result.update(await self._analyze_domain(artifact, tier))
            elif artifact_type == ArtifactType.CRYPTOCURRENCY:
                analysis_result.update(await self._analyze_cryptocurrency(artifact, tier))
            else:
                analysis_result.update(await self._analyze_unknown(artifact, tier))
            
            # Calculate overall risk score
            analysis_result["risk_score"] = self._calculate_risk_score(analysis_result)
            
            # Set confidence based on analysis depth
            analysis_result["confidence"] = self._calculate_confidence(analysis_result, tier)
            
        except Exception as e:
            logger.error(f"Error analyzing artifact {artifact_type}: {str(e)}")
            analysis_result["error"] = str(e)
            analysis_result["confidence"] = 0.0
        
        return analysis_result
    
    def _identify_artifact_type(self, artifact: Dict[str, Any]) -> str:
        """Identify the type of artifact"""
        
        content = str(artifact.get("content", "")).strip()
        artifact_type = artifact.get("type", "").lower()
        
        # Explicit type provided
        if artifact_type in [t for t in dir(ArtifactType) if not t.startswith('_')]:
            return artifact_type
        
        # Pattern-based detection
        if re.match(r'^https?://', content):
            return ArtifactType.URL
        elif re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', content):
            return ArtifactType.EMAIL
        elif re.match(r'^\+?[\d\s\-\(\)]{7,15}$', content):
            return ArtifactType.PHONE
        elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', content):
            return ArtifactType.IP_ADDRESS
        elif re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', content):
            return ArtifactType.DOMAIN
        elif re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', content) or re.match(r'^0x[a-fA-F0-9]{40}$', content):
            return ArtifactType.CRYPTOCURRENCY
        elif artifact.get("file_type") in ["jpg", "jpeg", "png", "gif", "bmp"]:
            return ArtifactType.IMAGE
        elif artifact.get("file_type") in ["pdf", "doc", "docx", "txt"]:
            return ArtifactType.DOCUMENT
        elif "facebook.com" in content or "twitter.com" in content or "instagram.com" in content:
            return ArtifactType.SOCIAL_MEDIA
        else:
            return ArtifactType.TEXT if len(content) > 10 else ArtifactType.UNKNOWN
    
    def _generate_artifact_id(self, artifact: Dict[str, Any]) -> str:
        """Generate unique ID for artifact"""
        content = str(artifact.get("content", ""))
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    async def _analyze_url(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze URL artifacts"""
        url = artifact.get("content", "")
        parsed_url = urlparse(url)
        
        analysis = {
            "technical_analysis": {
                "domain": parsed_url.netloc,
                "path": parsed_url.path,
                "query_params": parse_qs(parsed_url.query),
                "scheme": parsed_url.scheme,
                "port": parsed_url.port
            },
            "risk_indicators": [],
            "reputation_analysis": {}
        }
        
        # Domain analysis
        if parsed_url.netloc:
            domain_analysis = await self._analyze_domain_technical(parsed_url.netloc)
            analysis["technical_analysis"].update(domain_analysis)
        
        # URL pattern analysis
        url_lower = url.lower()
        
        # Check for suspicious patterns
        if any(pattern in url_lower for pattern in self.fraud_patterns["phishing_indicators"]):
            analysis["risk_indicators"].append("Phishing indicator in URL")
        
        if any(domain in url_lower for domain in self.fraud_patterns["suspicious_domains"]):
            analysis["risk_indicators"].append("Suspicious URL shortener detected")
        
        # Check for suspicious parameters
        suspicious_params = ["verify", "confirm", "update", "secure", "login"]
        for param in parsed_url.query.split("&"):
            if any(sp in param.lower() for sp in suspicious_params):
                analysis["risk_indicators"].append(f"Suspicious parameter: {param}")
        
        # SSL/TLS analysis
        if parsed_url.scheme == "https":
            ssl_analysis = await self._analyze_ssl_certificate(parsed_url.netloc)
            analysis["technical_analysis"]["ssl"] = ssl_analysis
        else:
            analysis["risk_indicators"].append("No HTTPS encryption")
        
        # Reputation check (for higher tiers)
        if tier in [ModelTier.PROFESSIONAL, ModelTier.ENTERPRISE, ModelTier.INTELLIGENCE]:
            reputation = await self._check_url_reputation(url)
            analysis["reputation_analysis"] = reputation
        
        return analysis
    
    async def _analyze_email(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze email artifacts"""
        email_content = artifact.get("content", "")
        
        analysis = {
            "content_analysis": {
                "sender": artifact.get("sender", ""),
                "subject": artifact.get("subject", ""),
                "body_length": len(email_content),
                "links_found": [],
                "attachments": artifact.get("attachments", [])
            },
            "risk_indicators": [],
            "behavioral_analysis": {}
        }
        
        # Extract links from email
        links = re.findall(r'https?://[^\s<>"]+', email_content)
        analysis["content_analysis"]["links_found"] = links
        
        # Analyze email content for fraud patterns
        email_lower = email_content.lower()
        
        for keyword in self.fraud_patterns["scam_keywords"]:
            if keyword in email_lower:
                analysis["risk_indicators"].append(f"Scam keyword detected: {keyword}")
        
        for pattern in self.fraud_patterns["social_engineering"]:
            if pattern in email_lower:
                analysis["risk_indicators"].append(f"Social engineering indicator: {pattern}")
        
        # Urgency analysis
        urgency_indicators = ["urgent", "immediate", "expires", "deadline", "act now"]
        urgency_count = sum(1 for indicator in urgency_indicators if indicator in email_lower)
        if urgency_count >= 2:
            analysis["risk_indicators"].append("High urgency manipulation detected")
        
        # Sender analysis
        sender = artifact.get("sender", "")
        if sender:
            sender_analysis = await self._analyze_email_sender(sender)
            analysis["content_analysis"]["sender_analysis"] = sender_analysis
        
        # Link analysis (for higher tiers)
        if tier in [ModelTier.PROFESSIONAL, ModelTier.ENTERPRISE, ModelTier.INTELLIGENCE]:
            for link in links[:5]:  # Analyze first 5 links
                link_analysis = await self._analyze_url({"content": link}, tier)
                if link_analysis.get("risk_indicators"):
                    analysis["risk_indicators"].extend([f"Malicious link: {indicator}" for indicator in link_analysis["risk_indicators"]])
        
        return analysis
    
    async def _analyze_phone(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze phone number artifacts"""
        phone = artifact.get("content", "")
        
        analysis = {
            "technical_analysis": {
                "formatted_number": phone,
                "country_code": "",
                "area_code": "",
                "number_type": "unknown"
            },
            "risk_indicators": [],
            "reputation_analysis": {}
        }
        
        # Basic phone number parsing
        cleaned_phone = re.sub(r'[^\d+]', '', phone)
        
        # Country code detection
        if cleaned_phone.startswith('+1'):
            analysis["technical_analysis"]["country_code"] = "US/Canada"
            analysis["technical_analysis"]["area_code"] = cleaned_phone[2:5] if len(cleaned_phone) >= 5 else ""
        elif cleaned_phone.startswith('+'):
            analysis["technical_analysis"]["country_code"] = "International"
        
        # Check against known scam patterns
        scam_area_codes = ["473", "649", "876", "284", "268"]  # Known scam area codes
        area_code = analysis["technical_analysis"]["area_code"]
        if area_code in scam_area_codes:
            analysis["risk_indicators"].append(f"Known scam area code: {area_code}")
        
        # Premium rate number detection
        if cleaned_phone.startswith("1900") or cleaned_phone.startswith("1976"):
            analysis["risk_indicators"].append("Premium rate number detected")
        
        return analysis
    
    async def _analyze_image(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze image artifacts"""
        analysis = {
            "technical_analysis": {
                "file_size": artifact.get("file_size", 0),
                "dimensions": artifact.get("dimensions", {}),
                "format": artifact.get("format", "unknown"),
                "metadata": {}
            },
            "content_analysis": {},
            "risk_indicators": []
        }
        
        # Basic image analysis
        if "image_data" in artifact:
            try:
                # Load image for analysis
                image_data = base64.b64decode(artifact["image_data"])
                image = Image.open(io.BytesIO(image_data))
                
                analysis["technical_analysis"]["dimensions"] = {
                    "width": image.width,
                    "height": image.height
                }
                analysis["technical_analysis"]["format"] = image.format
                
                # Extract metadata
                if hasattr(image, '_getexif') and image._getexif():
                    analysis["technical_analysis"]["metadata"] = dict(image._getexif())
                
                # For higher tiers, perform advanced analysis
                if tier in [ModelTier.ENTERPRISE, ModelTier.INTELLIGENCE]:
                    # Deepfake detection (simplified)
                    deepfake_score = await self._detect_deepfake(image)
                    if deepfake_score > 0.7:
                        analysis["risk_indicators"].append("Potential deepfake detected")
                    
                    # Document authenticity check
                    if self._appears_to_be_document(image):
                        authenticity_score = await self._check_document_authenticity(image)
                        if authenticity_score < 0.5:
                            analysis["risk_indicators"].append("Document may be forged")
                
            except Exception as e:
                analysis["technical_analysis"]["error"] = str(e)
        
        return analysis
    
    async def _analyze_document(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze document artifacts"""
        analysis = {
            "technical_analysis": {
                "file_type": artifact.get("file_type", "unknown"),
                "file_size": artifact.get("file_size", 0),
                "page_count": artifact.get("page_count", 0)
            },
            "content_analysis": {
                "text_content": artifact.get("text_content", ""),
                "language": "unknown",
                "word_count": 0
            },
            "risk_indicators": []
        }
        
        text_content = artifact.get("text_content", "")
        if text_content:
            analysis["content_analysis"]["word_count"] = len(text_content.split())
            
            # Analyze text for fraud patterns
            text_lower = text_content.lower()
            
            for keyword in self.fraud_patterns["scam_keywords"]:
                if keyword in text_lower:
                    analysis["risk_indicators"].append(f"Fraud keyword detected: {keyword}")
            
            # Check for document authenticity indicators
            authenticity_indicators = ["copy", "duplicate", "sample", "template", "draft"]
            for indicator in authenticity_indicators:
                if indicator in text_lower:
                    analysis["risk_indicators"].append(f"Document authenticity concern: {indicator}")
        
        return analysis
    
    async def _analyze_text(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze text artifacts"""
        text = artifact.get("content", "")
        
        analysis = {
            "content_analysis": {
                "length": len(text),
                "word_count": len(text.split()),
                "language": "unknown",
                "sentiment": "neutral"
            },
            "risk_indicators": [],
            "behavioral_analysis": {}
        }
        
        text_lower = text.lower()
        
        # Fraud pattern detection
        for keyword in self.fraud_patterns["scam_keywords"]:
            if keyword in text_lower:
                analysis["risk_indicators"].append(f"Fraud keyword: {keyword}")
        
        for pattern in self.fraud_patterns["social_engineering"]:
            if pattern in text_lower:
                analysis["risk_indicators"].append(f"Social engineering: {pattern}")
        
        # Urgency and pressure tactics
        urgency_words = ["urgent", "immediate", "now", "quickly", "hurry", "deadline"]
        urgency_count = sum(1 for word in urgency_words if word in text_lower)
        if urgency_count >= 3:
            analysis["risk_indicators"].append("High pressure tactics detected")
        
        # Financial terms
        financial_terms = ["money", "payment", "transfer", "account", "bank", "credit", "bitcoin"]
        financial_count = sum(1 for term in financial_terms if term in text_lower)
        if financial_count >= 3:
            analysis["behavioral_analysis"]["financial_focus"] = True
        
        return analysis
    
    async def _analyze_social_media(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze social media profile artifacts"""
        profile_url = artifact.get("content", "")
        
        analysis = {
            "technical_analysis": {
                "platform": self._identify_social_platform(profile_url),
                "profile_url": profile_url,
                "username": self._extract_username(profile_url)
            },
            "content_analysis": {
                "profile_data": artifact.get("profile_data", {}),
                "post_count": artifact.get("post_count", 0),
                "follower_count": artifact.get("follower_count", 0),
                "following_count": artifact.get("following_count", 0)
            },
            "risk_indicators": [],
            "behavioral_analysis": {}
        }
        
        # Analyze profile characteristics
        profile_data = artifact.get("profile_data", {})
        
        # Check for fake profile indicators
        if profile_data.get("creation_date"):
            # Recent account creation
            creation_date = profile_data["creation_date"]
            # Simplified check - in production would parse actual date
            if "2024" in str(creation_date) or "2025" in str(creation_date):
                analysis["risk_indicators"].append("Recently created account")
        
        # Follower/following ratio analysis
        followers = analysis["content_analysis"]["follower_count"]
        following = analysis["content_analysis"]["following_count"]
        
        if followers > 0 and following > 0:
            ratio = following / followers
            if ratio > 10:  # Following many more than followers
                analysis["risk_indicators"].append("Suspicious follower/following ratio")
        
        # Profile completeness
        required_fields = ["bio", "profile_picture", "location"]
        missing_fields = [field for field in required_fields if not profile_data.get(field)]
        if len(missing_fields) >= 2:
            analysis["risk_indicators"].append("Incomplete profile information")
        
        return analysis
    
    async def _analyze_ip_address(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze IP address artifacts"""
        ip_address = artifact.get("content", "")
        
        analysis = {
            "technical_analysis": {
                "ip_address": ip_address,
                "ip_type": "unknown",
                "geolocation": {},
                "asn_info": {}
            },
            "reputation_analysis": {},
            "risk_indicators": []
        }
        
        # Basic IP validation
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip_address):
            analysis["risk_indicators"].append("Invalid IP address format")
            return analysis
        
        # Check for private/reserved IP ranges
        octets = [int(x) for x in ip_address.split('.')]
        
        if octets[0] == 10 or (octets[0] == 172 and 16 <= octets[1] <= 31) or (octets[0] == 192 and octets[1] == 168):
            analysis["technical_analysis"]["ip_type"] = "private"
        elif octets[0] == 127:
            analysis["technical_analysis"]["ip_type"] = "localhost"
        else:
            analysis["technical_analysis"]["ip_type"] = "public"
        
        # For public IPs, perform additional analysis
        if analysis["technical_analysis"]["ip_type"] == "public" and tier in [ModelTier.PROFESSIONAL, ModelTier.ENTERPRISE, ModelTier.INTELLIGENCE]:
            # Geolocation lookup (simplified)
            analysis["technical_analysis"]["geolocation"] = await self._geolocate_ip(ip_address)
            
            # Reputation check
            reputation = await self._check_ip_reputation(ip_address)
            analysis["reputation_analysis"] = reputation
        
        return analysis
    
    async def _analyze_domain(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze domain artifacts"""
        domain = artifact.get("content", "")
        
        analysis = await self._analyze_domain_technical(domain)
        
        # Add reputation analysis for higher tiers
        if tier in [ModelTier.PROFESSIONAL, ModelTier.ENTERPRISE, ModelTier.INTELLIGENCE]:
            reputation = await self._check_domain_reputation(domain)
            analysis["reputation_analysis"] = reputation
        
        return analysis
    
    async def _analyze_cryptocurrency(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze cryptocurrency address artifacts"""
        address = artifact.get("content", "")
        
        analysis = {
            "technical_analysis": {
                "address": address,
                "currency_type": "unknown",
                "address_format": "unknown"
            },
            "risk_indicators": [],
            "reputation_analysis": {}
        }
        
        # Identify cryptocurrency type
        if re.match(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$', address):
            analysis["technical_analysis"]["currency_type"] = "Bitcoin"
            analysis["technical_analysis"]["address_format"] = "Legacy/P2SH"
        elif re.match(r'^bc1[a-z0-9]{39,59}$', address):
            analysis["technical_analysis"]["currency_type"] = "Bitcoin"
            analysis["technical_analysis"]["address_format"] = "Bech32"
        elif re.match(r'^0x[a-fA-F0-9]{40}$', address):
            analysis["technical_analysis"]["currency_type"] = "Ethereum"
            analysis["technical_analysis"]["address_format"] = "ERC-20"
        
        # For higher tiers, check against known scam addresses
        if tier in [ModelTier.ENTERPRISE, ModelTier.INTELLIGENCE]:
            # This would integrate with blockchain analysis APIs
            analysis["reputation_analysis"]["scam_database_check"] = "Not implemented"
        
        return analysis
    
    async def _analyze_unknown(self, artifact: Dict[str, Any], tier: ModelTier) -> Dict[str, Any]:
        """Analyze unknown artifact types"""
        content = artifact.get("content", "")
        
        analysis = {
            "content_analysis": {
                "content_length": len(content),
                "content_type": "unknown"
            },
            "risk_indicators": [],
            "notes": ["Artifact type could not be determined automatically"]
        }
        
        # Basic pattern analysis
        if any(keyword in content.lower() for keyword in self.fraud_patterns["scam_keywords"]):
            analysis["risk_indicators"].append("Potential fraud keywords detected")
        
        return analysis
    
    # Helper methods for technical analysis
    
    async def _analyze_domain_technical(self, domain: str) -> Dict[str, Any]:
        """Perform technical analysis of a domain"""
        analysis = {
            "technical_analysis": {
                "domain": domain,
                "whois_data": {},
                "dns_records": {},
                "ssl_info": {}
            },
            "risk_indicators": []
        }
        
        try:
            # WHOIS lookup
            whois_data = whois.whois(domain)
            analysis["technical_analysis"]["whois_data"] = {
                "creation_date": str(whois_data.creation_date) if whois_data.creation_date else None,
                "expiration_date": str(whois_data.expiration_date) if whois_data.expiration_date else None,
                "registrar": whois_data.registrar,
                "name_servers": whois_data.name_servers
            }
            
            # Check domain age
            if whois_data.creation_date:
                creation_date = whois_data.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                
                domain_age = (datetime.now() - creation_date).days
                if domain_age < 30:
                    analysis["risk_indicators"].append("Very new domain (less than 30 days)")
                elif domain_age < 90:
                    analysis["risk_indicators"].append("Recently created domain (less than 90 days)")
            
        except Exception as e:
            analysis["technical_analysis"]["whois_error"] = str(e)
        
        try:
            # DNS lookup
            dns_records = {}
            for record_type in ['A', 'MX', 'NS', 'TXT']:
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    dns_records[record_type] = [str(answer) for answer in answers]
                except:
                    pass
            
            analysis["technical_analysis"]["dns_records"] = dns_records
            
        except Exception as e:
            analysis["technical_analysis"]["dns_error"] = str(e)
        
        return analysis
    
    async def _analyze_ssl_certificate(self, domain: str) -> Dict[str, Any]:
        """Analyze SSL certificate for a domain"""
        ssl_info = {
            "valid": False,
            "issuer": "",
            "expiration": "",
            "subject": ""
        }
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    ssl_info.update({
                        "valid": True,
                        "issuer": dict(x[0] for x in cert['issuer']).get('organizationName', ''),
                        "expiration": cert['notAfter'],
                        "subject": dict(x[0] for x in cert['subject']).get('commonName', '')
                    })
        except Exception as e:
            ssl_info["error"] = str(e)
        
        return ssl_info
    
    async def _check_url_reputation(self, url: str) -> Dict[str, Any]:
        """Check URL reputation using various services"""
        reputation = {
            "checked_services": [],
            "threat_detected": False,
            "reputation_score": 0.0
        }
        
        # This would integrate with actual reputation APIs
        # For demo purposes, simplified implementation
        reputation["checked_services"] = ["virustotal", "urlvoid"]
        reputation["reputation_score"] = 0.8  # Placeholder
        
        return reputation
    
    async def _check_ip_reputation(self, ip_address: str) -> Dict[str, Any]:
        """Check IP address reputation"""
        reputation = {
            "abuse_confidence": 0,
            "country": "unknown",
            "isp": "unknown",
            "threat_types": []
        }
        
        # This would integrate with AbuseIPDB, VirusTotal, etc.
        # Placeholder implementation
        return reputation
    
    async def _check_domain_reputation(self, domain: str) -> Dict[str, Any]:
        """Check domain reputation"""
        reputation = {
            "reputation_score": 0.0,
            "threat_categories": [],
            "last_seen": None
        }
        
        # This would integrate with domain reputation services
        # Placeholder implementation
        return reputation
    
    async def _geolocate_ip(self, ip_address: str) -> Dict[str, Any]:
        """Get geolocation information for IP address"""
        geolocation = {
            "country": "unknown",
            "city": "unknown",
            "latitude": 0.0,
            "longitude": 0.0
        }
        
        # This would integrate with IP geolocation services
        # Placeholder implementation
        return geolocation
    
    async def _analyze_email_sender(self, sender: str) -> Dict[str, Any]:
        """Analyze email sender information"""
        analysis = {
            "domain": "",
            "reputation": "unknown",
            "spf_record": False,
            "dmarc_record": False
        }
        
        if "@" in sender:
            domain = sender.split("@")[1]
            analysis["domain"] = domain
            
            # Check for common free email providers
            free_providers = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
            if domain in free_providers:
                analysis["provider_type"] = "free"
            else:
                analysis["provider_type"] = "custom"
        
        return analysis
    
    async def _detect_deepfake(self, image: Image.Image) -> float:
        """Detect potential deepfake in image (simplified)"""
        # This would use specialized deepfake detection models
        # Placeholder implementation
        return 0.1  # Low probability
    
    def _appears_to_be_document(self, image: Image.Image) -> bool:
        """Check if image appears to be a document"""
        # Simple heuristic based on aspect ratio and colors
        width, height = image.size
        aspect_ratio = width / height
        
        # Documents typically have certain aspect ratios
        return 0.7 <= aspect_ratio <= 1.5
    
    async def _check_document_authenticity(self, image: Image.Image) -> float:
        """Check document authenticity (simplified)"""
        # This would use document forensics techniques
        # Placeholder implementation
        return 0.8  # High authenticity score
    
    def _identify_social_platform(self, url: str) -> str:
        """Identify social media platform from URL"""
        if "facebook.com" in url:
            return "Facebook"
        elif "twitter.com" in url or "x.com" in url:
            return "Twitter/X"
        elif "instagram.com" in url:
            return "Instagram"
        elif "linkedin.com" in url:
            return "LinkedIn"
        elif "tiktok.com" in url:
            return "TikTok"
        else:
            return "Unknown"
    
    def _extract_username(self, url: str) -> str:
        """Extract username from social media URL"""
        # Simplified username extraction
        parts = url.split("/")
        for i, part in enumerate(parts):
            if part in ["facebook.com", "twitter.com", "instagram.com", "linkedin.com"]:
                if i + 1 < len(parts):
                    return parts[i + 1]
        return ""
    
    def _calculate_risk_score(self, analysis: Dict[str, Any]) -> float:
        """Calculate overall risk score for artifact"""
        risk_indicators = analysis.get("risk_indicators", [])
        
        # Base score calculation
        risk_score = len(risk_indicators) * 0.1
        
        # Weight by severity of indicators
        critical_keywords = ["confirmed", "detected", "malicious", "fraud"]
        for indicator in risk_indicators:
            if any(keyword in indicator.lower() for keyword in critical_keywords):
                risk_score += 0.2
        
        # Cap at 1.0
        return min(risk_score, 1.0)
    
    def _calculate_confidence(self, analysis: Dict[str, Any], tier: ModelTier) -> float:
        """Calculate confidence score based on analysis depth"""
        base_confidence = 0.5
        
        # Increase confidence based on tier
        tier_bonus = {
            ModelTier.BASIC: 0.1,
            ModelTier.PROFESSIONAL: 0.2,
            ModelTier.ENTERPRISE: 0.3,
            ModelTier.INTELLIGENCE: 0.4
        }
        
        confidence = base_confidence + tier_bonus.get(tier, 0.1)
        
        # Increase confidence if multiple analysis types completed
        analysis_types = ["technical_analysis", "content_analysis", "reputation_analysis"]
        completed_analyses = sum(1 for at in analysis_types if analysis.get(at))
        confidence += completed_analyses * 0.1
        
        # Decrease confidence if errors occurred
        if "error" in analysis:
            confidence -= 0.2
        
        return max(0.0, min(1.0, confidence))

