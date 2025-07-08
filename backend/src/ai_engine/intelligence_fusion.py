"""
Intelligence Fusion System

Correlates and fuses intelligence from multiple sources to provide
comprehensive threat assessment and attribution analysis.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import hashlib
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ThreatIntelligence:
    """Threat intelligence data structure"""
    source: str
    threat_type: str
    indicators: List[str]
    confidence: float
    timestamp: datetime
    attribution: Optional[str] = None
    campaign_id: Optional[str] = None

class IntelligenceFusion:
    """
    Intelligence Fusion Engine
    
    Correlates threat intelligence from multiple sources:
    - Known scam databases
    - Threat intelligence feeds
    - Historical investigation data
    - Pattern recognition systems
    - Attribution analysis
    """
    
    def __init__(self):
        self.threat_database = {}
        self.campaign_tracker = {}
        self.pattern_cache = {}
        self.intelligence_sources = self._initialize_intelligence_sources()
    
    def _initialize_intelligence_sources(self) -> Dict[str, Any]:
        """Initialize intelligence source configurations"""
        return {
            "internal_database": {
                "enabled": True,
                "priority": 1,
                "confidence_weight": 0.9
            },
            "threat_feeds": {
                "enabled": True,
                "priority": 2,
                "confidence_weight": 0.8,
                "sources": ["misp", "otx", "threatfox"]
            },
            "reputation_services": {
                "enabled": True,
                "priority": 3,
                "confidence_weight": 0.7,
                "services": ["virustotal", "urlvoid", "abuseipdb"]
            },
            "community_reports": {
                "enabled": True,
                "priority": 4,
                "confidence_weight": 0.6
            }
        }
    
    async def correlate_intelligence(self, artifact_results: Dict[str, Any], 
                                   context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Correlate intelligence across multiple sources
        
        Args:
            artifact_results: Results from artifact analysis
            context: Additional context for correlation
            
        Returns:
            Fused intelligence assessment
        """
        
        correlation_results = {
            "correlation_id": self._generate_correlation_id(artifact_results),
            "timestamp": datetime.utcnow().isoformat(),
            "intelligence_sources": [],
            "threat_correlations": [],
            "campaign_attribution": {},
            "pattern_matches": [],
            "confidence_score": 0.0,
            "strategic_assessment": {}
        }
        
        try:
            # Extract indicators from artifacts
            indicators = self._extract_indicators(artifact_results)
            
            # Correlate against internal database
            internal_matches = await self._correlate_internal_database(indicators)
            if internal_matches:
                correlation_results["intelligence_sources"].append("internal_database")
                correlation_results["threat_correlations"].extend(internal_matches)
            
            # Correlate against threat feeds
            threat_feed_matches = await self._correlate_threat_feeds(indicators)
            if threat_feed_matches:
                correlation_results["intelligence_sources"].append("threat_feeds")
                correlation_results["threat_correlations"].extend(threat_feed_matches)
            
            # Pattern analysis
            pattern_matches = await self._analyze_patterns(indicators, artifact_results)
            correlation_results["pattern_matches"] = pattern_matches
            
            # Campaign attribution
            attribution = await self._perform_attribution_analysis(indicators, correlation_results)
            correlation_results["campaign_attribution"] = attribution
            
            # Strategic assessment
            strategic_assessment = await self._generate_strategic_assessment(correlation_results)
            correlation_results["strategic_assessment"] = strategic_assessment
            
            # Calculate overall confidence
            correlation_results["confidence_score"] = self._calculate_correlation_confidence(correlation_results)
            
        except Exception as e:
            logger.error(f"Intelligence correlation failed: {str(e)}")
            correlation_results["error"] = str(e)
        
        return correlation_results
    
    def _extract_indicators(self, artifact_results: Dict[str, Any]) -> Dict[str, List[str]]:
        """Extract threat indicators from artifact analysis"""
        indicators = {
            "domains": [],
            "urls": [],
            "ip_addresses": [],
            "email_addresses": [],
            "phone_numbers": [],
            "hashes": [],
            "patterns": []
        }
        
        analyzed_artifacts = artifact_results.get("analyzed_artifacts", [])
        
        for artifact in analyzed_artifacts:
            artifact_type = artifact.get("type", "")
            
            if artifact_type == "url":
                technical_analysis = artifact.get("technical_analysis", {})
                if "domain" in technical_analysis:
                    indicators["domains"].append(technical_analysis["domain"])
                indicators["urls"].append(artifact.get("artifact_id", ""))
            
            elif artifact_type == "domain":
                indicators["domains"].append(artifact.get("technical_analysis", {}).get("domain", ""))
            
            elif artifact_type == "ip_address":
                indicators["ip_addresses"].append(artifact.get("technical_analysis", {}).get("ip_address", ""))
            
            elif artifact_type == "email":
                content_analysis = artifact.get("content_analysis", {})
                if "sender" in content_analysis:
                    indicators["email_addresses"].append(content_analysis["sender"])
            
            elif artifact_type == "phone":
                indicators["phone_numbers"].append(artifact.get("technical_analysis", {}).get("formatted_number", ""))
            
            # Extract risk indicators as patterns
            risk_indicators = artifact.get("risk_indicators", [])
            indicators["patterns"].extend(risk_indicators)
        
        return indicators
    
    async def _correlate_internal_database(self, indicators: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Correlate against internal threat database"""
        matches = []
        
        # Check against known scam database (Apps Curb example)
        known_threats = {
            "appscurb.com": {
                "threat_type": "advance_fee_fraud",
                "confidence": 0.99,
                "first_seen": "2024-12-01",
                "last_seen": "2025-01-07",
                "campaign": "apps_curb_scam",
                "indicators": ["testimonial_theft", "fake_business", "new_domain"],
                "attribution": "unknown_threat_actor"
            }
        }
        
        # Check domains
        for domain in indicators.get("domains", []):
            if domain in known_threats:
                threat_data = known_threats[domain]
                matches.append({
                    "source": "internal_database",
                    "indicator": domain,
                    "indicator_type": "domain",
                    "threat_type": threat_data["threat_type"],
                    "confidence": threat_data["confidence"],
                    "campaign": threat_data.get("campaign"),
                    "attribution": threat_data.get("attribution"),
                    "details": threat_data
                })
        
        # Check patterns against known fraud patterns
        fraud_patterns = {
            "testimonial_theft": {
                "threat_type": "business_impersonation",
                "confidence": 0.95,
                "description": "Systematic theft of client testimonials"
            },
            "new_domain": {
                "threat_type": "domain_squatting",
                "confidence": 0.7,
                "description": "Recently registered domain for fraudulent purposes"
            }
        }
        
        for pattern in indicators.get("patterns", []):
            pattern_lower = pattern.lower()
            for fraud_pattern, data in fraud_patterns.items():
                if fraud_pattern in pattern_lower:
                    matches.append({
                        "source": "internal_database",
                        "indicator": pattern,
                        "indicator_type": "pattern",
                        "threat_type": data["threat_type"],
                        "confidence": data["confidence"],
                        "description": data["description"]
                    })
        
        return matches
    
    async def _correlate_threat_feeds(self, indicators: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Correlate against external threat intelligence feeds"""
        matches = []
        
        # Simulate threat feed correlation
        # In production, this would query actual threat intelligence APIs
        
        threat_feed_data = {
            "malicious_domains": ["scam-example.com", "fraud-site.net"],
            "suspicious_ips": ["192.168.1.100", "10.0.0.1"],
            "known_campaigns": {
                "advance_fee_fraud_2024": {
                    "indicators": ["urgent payment", "wire transfer", "inheritance"],
                    "confidence": 0.85
                }
            }
        }
        
        # Check domains against threat feeds
        for domain in indicators.get("domains", []):
            if domain in threat_feed_data["malicious_domains"]:
                matches.append({
                    "source": "threat_feeds",
                    "indicator": domain,
                    "indicator_type": "domain",
                    "threat_type": "malicious_domain",
                    "confidence": 0.8,
                    "feed_source": "simulated_feed"
                })
        
        # Check IPs against threat feeds
        for ip in indicators.get("ip_addresses", []):
            if ip in threat_feed_data["suspicious_ips"]:
                matches.append({
                    "source": "threat_feeds",
                    "indicator": ip,
                    "indicator_type": "ip_address",
                    "threat_type": "suspicious_ip",
                    "confidence": 0.75,
                    "feed_source": "simulated_feed"
                })
        
        return matches
    
    async def _analyze_patterns(self, indicators: Dict[str, List[str]], 
                              artifact_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze patterns across indicators and artifacts"""
        pattern_matches = []
        
        # Temporal pattern analysis
        temporal_patterns = self._analyze_temporal_patterns(artifact_results)
        if temporal_patterns:
            pattern_matches.extend(temporal_patterns)
        
        # Infrastructure pattern analysis
        infrastructure_patterns = self._analyze_infrastructure_patterns(indicators)
        if infrastructure_patterns:
            pattern_matches.extend(infrastructure_patterns)
        
        # Behavioral pattern analysis
        behavioral_patterns = self._analyze_behavioral_patterns(artifact_results)
        if behavioral_patterns:
            pattern_matches.extend(behavioral_patterns)
        
        return pattern_matches
    
    def _analyze_temporal_patterns(self, artifact_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze temporal patterns in threat activity"""
        patterns = []
        
        # Check for rapid domain registration and use
        analyzed_artifacts = artifact_results.get("analyzed_artifacts", [])
        
        for artifact in analyzed_artifacts:
            if artifact.get("type") == "domain":
                whois_data = artifact.get("technical_analysis", {}).get("whois_data", {})
                creation_date = whois_data.get("creation_date")
                
                if creation_date and "2024-12" in str(creation_date):
                    patterns.append({
                        "pattern_type": "temporal",
                        "pattern_name": "rapid_deployment",
                        "description": "Domain registered and immediately used for fraudulent activity",
                        "confidence": 0.8,
                        "indicators": [artifact.get("artifact_id")]
                    })
        
        return patterns
    
    def _analyze_infrastructure_patterns(self, indicators: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Analyze infrastructure patterns"""
        patterns = []
        
        # Check for shared infrastructure
        domains = indicators.get("domains", [])
        if len(domains) > 1:
            patterns.append({
                "pattern_type": "infrastructure",
                "pattern_name": "shared_infrastructure",
                "description": "Multiple domains potentially sharing infrastructure",
                "confidence": 0.6,
                "indicators": domains
            })
        
        # Check for suspicious TLDs
        suspicious_tlds = [".tk", ".ml", ".ga", ".cf"]
        for domain in domains:
            for tld in suspicious_tlds:
                if domain.endswith(tld):
                    patterns.append({
                        "pattern_type": "infrastructure",
                        "pattern_name": "suspicious_tld",
                        "description": f"Use of suspicious TLD: {tld}",
                        "confidence": 0.7,
                        "indicators": [domain]
                    })
        
        return patterns
    
    def _analyze_behavioral_patterns(self, artifact_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Analyze behavioral patterns in threat activity"""
        patterns = []
        
        # Check for social engineering patterns
        social_engineering_count = 0
        urgency_count = 0
        
        analyzed_artifacts = artifact_results.get("analyzed_artifacts", [])
        
        for artifact in analyzed_artifacts:
            risk_indicators = artifact.get("risk_indicators", [])
            
            for indicator in risk_indicators:
                indicator_lower = indicator.lower()
                if "social engineering" in indicator_lower:
                    social_engineering_count += 1
                if "urgency" in indicator_lower or "pressure" in indicator_lower:
                    urgency_count += 1
        
        if social_engineering_count >= 2:
            patterns.append({
                "pattern_type": "behavioral",
                "pattern_name": "social_engineering_campaign",
                "description": "Coordinated social engineering tactics detected",
                "confidence": 0.85,
                "indicators": [f"{social_engineering_count} social engineering indicators"]
            })
        
        if urgency_count >= 2:
            patterns.append({
                "pattern_type": "behavioral",
                "pattern_name": "urgency_manipulation",
                "description": "High-pressure urgency tactics employed",
                "confidence": 0.8,
                "indicators": [f"{urgency_count} urgency indicators"]
            })
        
        return patterns
    
    async def _perform_attribution_analysis(self, indicators: Dict[str, List[str]], 
                                          correlation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform threat attribution analysis"""
        attribution = {
            "threat_actor": "unknown",
            "campaign_name": "",
            "confidence": 0.0,
            "attribution_factors": [],
            "related_campaigns": []
        }
        
        # Check for known campaign indicators
        threat_correlations = correlation_results.get("threat_correlations", [])
        
        campaigns_found = set()
        for correlation in threat_correlations:
            if "campaign" in correlation:
                campaigns_found.add(correlation["campaign"])
        
        if campaigns_found:
            # Use the most confident campaign attribution
            primary_campaign = list(campaigns_found)[0]  # Simplified selection
            attribution.update({
                "campaign_name": primary_campaign,
                "confidence": 0.8,
                "attribution_factors": ["Known campaign indicators", "Infrastructure overlap"],
                "related_campaigns": list(campaigns_found)
            })
            
            # Specific attribution for Apps Curb campaign
            if primary_campaign == "apps_curb_scam":
                attribution.update({
                    "threat_actor": "unknown_fraudster",
                    "campaign_name": "Apps Curb Advance Fee Fraud",
                    "confidence": 0.95,
                    "attribution_factors": [
                        "Testimonial theft from Goji Labs",
                        "Fake business registration",
                        "Advance fee fraud methodology",
                        "Domain registration patterns"
                    ],
                    "tactics": ["Business impersonation", "Testimonial theft", "Social engineering"],
                    "target_profile": "Small business owners seeking app development services"
                })
        
        return attribution
    
    async def _generate_strategic_assessment(self, correlation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate strategic threat assessment"""
        assessment = {
            "threat_landscape": "evolving",
            "campaign_maturity": "unknown",
            "threat_persistence": "unknown",
            "geographic_scope": "unknown",
            "target_sectors": [],
            "recommended_actions": [],
            "monitoring_priorities": []
        }
        
        # Analyze threat correlations for strategic insights
        threat_correlations = correlation_results.get("threat_correlations", [])
        campaign_attribution = correlation_results.get("campaign_attribution", {})
        
        if threat_correlations:
            assessment["threat_landscape"] = "active"
            
            # Determine campaign maturity
            confidence_scores = [tc.get("confidence", 0) for tc in threat_correlations]
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
            
            if avg_confidence > 0.8:
                assessment["campaign_maturity"] = "established"
            elif avg_confidence > 0.6:
                assessment["campaign_maturity"] = "developing"
            else:
                assessment["campaign_maturity"] = "emerging"
        
        # Strategic recommendations based on attribution
        if campaign_attribution.get("campaign_name") == "Apps Curb Advance Fee Fraud":
            assessment.update({
                "target_sectors": ["Small business", "App development", "Technology services"],
                "geographic_scope": "Global (English-speaking)",
                "threat_persistence": "ongoing",
                "recommended_actions": [
                    "Alert small business communities",
                    "Share intelligence with app development platforms",
                    "Monitor for similar testimonial theft patterns",
                    "Track domain registration patterns"
                ],
                "monitoring_priorities": [
                    "New domains with similar patterns",
                    "Testimonial theft from legitimate companies",
                    "Advance fee fraud targeting app developers"
                ]
            })
        
        return assessment
    
    def _calculate_correlation_confidence(self, correlation_results: Dict[str, Any]) -> float:
        """Calculate overall correlation confidence score"""
        confidence_factors = []
        
        # Intelligence source confidence
        intelligence_sources = correlation_results.get("intelligence_sources", [])
        source_weights = {
            "internal_database": 0.9,
            "threat_feeds": 0.8,
            "reputation_services": 0.7,
            "community_reports": 0.6
        }
        
        for source in intelligence_sources:
            confidence_factors.append(source_weights.get(source, 0.5))
        
        # Threat correlation confidence
        threat_correlations = correlation_results.get("threat_correlations", [])
        if threat_correlations:
            correlation_confidences = [tc.get("confidence", 0) for tc in threat_correlations]
            avg_correlation_confidence = sum(correlation_confidences) / len(correlation_confidences)
            confidence_factors.append(avg_correlation_confidence)
        
        # Pattern match confidence
        pattern_matches = correlation_results.get("pattern_matches", [])
        if pattern_matches:
            pattern_confidences = [pm.get("confidence", 0) for pm in pattern_matches]
            avg_pattern_confidence = sum(pattern_confidences) / len(pattern_confidences)
            confidence_factors.append(avg_pattern_confidence)
        
        # Attribution confidence
        attribution = correlation_results.get("campaign_attribution", {})
        if attribution.get("confidence", 0) > 0:
            confidence_factors.append(attribution["confidence"])
        
        # Calculate weighted average
        if confidence_factors:
            return sum(confidence_factors) / len(confidence_factors)
        else:
            return 0.0
    
    def _generate_correlation_id(self, artifact_results: Dict[str, Any]) -> str:
        """Generate unique correlation ID"""
        content = json.dumps(artifact_results, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    async def add_threat_intelligence(self, intelligence: ThreatIntelligence) -> bool:
        """Add new threat intelligence to the database"""
        try:
            threat_id = hashlib.sha256(f"{intelligence.source}_{intelligence.threat_type}_{intelligence.timestamp}".encode()).hexdigest()[:16]
            
            self.threat_database[threat_id] = {
                "source": intelligence.source,
                "threat_type": intelligence.threat_type,
                "indicators": intelligence.indicators,
                "confidence": intelligence.confidence,
                "timestamp": intelligence.timestamp.isoformat(),
                "attribution": intelligence.attribution,
                "campaign_id": intelligence.campaign_id
            }
            
            logger.info(f"Added threat intelligence: {threat_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to add threat intelligence: {str(e)}")
            return False
    
    async def query_threat_intelligence(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Query threat intelligence database"""
        results = []
        
        query_type = query.get("type", "")
        query_value = query.get("value", "")
        
        for threat_id, threat_data in self.threat_database.items():
            # Simple matching logic
            if query_type == "indicator" and query_value in threat_data.get("indicators", []):
                results.append(threat_data)
            elif query_type == "threat_type" and query_value == threat_data.get("threat_type"):
                results.append(threat_data)
            elif query_type == "campaign" and query_value == threat_data.get("campaign_id"):
                results.append(threat_data)
        
        return results
    
    def get_threat_statistics(self) -> Dict[str, Any]:
        """Get threat intelligence statistics"""
        stats = {
            "total_threats": len(self.threat_database),
            "threat_types": {},
            "sources": {},
            "campaigns": {},
            "recent_activity": 0
        }
        
        recent_threshold = datetime.utcnow() - timedelta(days=7)
        
        for threat_data in self.threat_database.values():
            # Count threat types
            threat_type = threat_data.get("threat_type", "unknown")
            stats["threat_types"][threat_type] = stats["threat_types"].get(threat_type, 0) + 1
            
            # Count sources
            source = threat_data.get("source", "unknown")
            stats["sources"][source] = stats["sources"].get(source, 0) + 1
            
            # Count campaigns
            campaign = threat_data.get("campaign_id")
            if campaign:
                stats["campaigns"][campaign] = stats["campaigns"].get(campaign, 0) + 1
            
            # Count recent activity
            timestamp_str = threat_data.get("timestamp", "")
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                if timestamp > recent_threshold:
                    stats["recent_activity"] += 1
            except:
                pass
        
        return stats

