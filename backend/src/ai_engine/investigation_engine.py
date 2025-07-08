"""
ScamShield AI Investigation Engine

Orchestrates comprehensive fraud investigations using multiple AI models,
intelligence sources, and analysis techniques to provide elite-level
investigation capabilities.
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json
import hashlib
from datetime import datetime, timezone
import uuid

from .model_manager_v2 import EnhancedModelManager, ModelTier
from .artifact_analyzer import ArtifactAnalyzer
from .intelligence_fusion import IntelligenceFusion

logger = logging.getLogger(__name__)

class InvestigationType(Enum):
    """Types of investigations"""
    QUICK_SCAN = "quick_scan"
    DEEP_ANALYSIS = "deep_analysis"
    COMPREHENSIVE = "comprehensive"
    ELITE_INTELLIGENCE = "elite_intelligence"

class ThreatLevel(Enum):
    """Threat assessment levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class InvestigationRequest:
    """Investigation request structure"""
    investigation_id: str
    user_id: str
    tier: ModelTier
    investigation_type: InvestigationType
    artifacts: List[Dict[str, Any]]
    context: Optional[Dict[str, Any]] = None
    priority: str = "normal"
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now(timezone.utc)

@dataclass
class InvestigationResult:
    """Investigation result structure"""
    investigation_id: str
    tier: ModelTier
    threat_level: ThreatLevel
    confidence_score: float
    executive_summary: str
    detailed_findings: Dict[str, Any]
    evidence_analysis: Dict[str, Any]
    recommendations: List[str]
    models_used: List[str]
    processing_time: float
    cost: float
    timestamp: datetime
    
    def to_dict(self):
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        result['tier'] = self.tier.value
        result['threat_level'] = self.threat_level.value
        return result

class InvestigationEngine:
    """
    Elite Investigation Engine
    
    Orchestrates comprehensive fraud investigations using:
    - Multi-modal artifact analysis
    - Advanced AI model ensemble
    - Intelligence fusion and correlation
    - Behavioral and technical analysis
    - Strategic threat assessment
    """
    
    def __init__(self):
        self.model_manager = EnhancedModelManager()
        self.artifact_analyzer = ArtifactAnalyzer()
        self.intelligence_fusion = IntelligenceFusion()
        self.active_investigations = {}
        
    async def conduct_investigation(self, request: InvestigationRequest) -> InvestigationResult:
        """
        Conduct comprehensive investigation based on tier and artifacts
        
        Args:
            request: Investigation request with artifacts and parameters
            
        Returns:
            Comprehensive investigation result with findings and recommendations
        """
        start_time = datetime.now(timezone.utc)
        investigation_id = request.investigation_id
        
        logger.info(f"Starting {request.tier.value} investigation {investigation_id}")
        
        try:
            # Store active investigation
            self.active_investigations[investigation_id] = {
                "status": "processing",
                "start_time": start_time,
                "tier": request.tier,
                "artifacts_count": len(request.artifacts)
            }
            
            # Phase 1: Artifact Analysis
            artifact_results = await self._analyze_artifacts(request.artifacts, request.tier)
            
            # Phase 2: Intelligence Fusion
            intelligence_results = await self._fuse_intelligence(artifact_results, request.context)
            
            # Phase 3: AI Model Analysis
            ai_analysis = await self._conduct_ai_analysis(request, artifact_results, intelligence_results)
            
            # Phase 4: Threat Assessment
            threat_assessment = await self._assess_threat_level(ai_analysis, artifact_results)
            
            # Phase 5: Generate Recommendations
            recommendations = await self._generate_recommendations(
                threat_assessment, ai_analysis, request.tier
            )
            
            # Phase 6: Compile Final Report
            final_result = await self._compile_investigation_result(
                request, ai_analysis, threat_assessment, recommendations, start_time
            )
            
            # Update investigation status
            self.active_investigations[investigation_id]["status"] = "completed"
            
            logger.info(f"Completed investigation {investigation_id} in {final_result.processing_time:.2f}s")
            
            return final_result
            
        except Exception as e:
            logger.error(f"Investigation {investigation_id} failed: {str(e)}")
            self.active_investigations[investigation_id]["status"] = "failed"
            
            # Return error result
            return InvestigationResult(
                investigation_id=investigation_id,
                tier=request.tier,
                threat_level=ThreatLevel.MEDIUM,
                confidence_score=0.0,
                executive_summary=f"Investigation failed: {str(e)}",
                detailed_findings={"error": str(e)},
                evidence_analysis={},
                recommendations=["Contact support for assistance"],
                models_used=[],
                processing_time=(datetime.now(timezone.utc) - start_time).total_seconds(),
                cost=0.0,
                timestamp=datetime.now(timezone.utc)
            )
    
    async def _analyze_artifacts(self, artifacts: List[Dict[str, Any]], tier: ModelTier) -> Dict[str, Any]:
        """Analyze submitted artifacts using appropriate techniques"""
        
        artifact_results = {
            "total_artifacts": len(artifacts),
            "analyzed_artifacts": [],
            "artifact_types": {},
            "risk_indicators": [],
            "technical_findings": {}
        }
        
        for artifact in artifacts:
            try:
                # Analyze each artifact
                analysis = await self.artifact_analyzer.analyze_artifact(artifact, tier)
                artifact_results["analyzed_artifacts"].append(analysis)
                
                # Track artifact types
                artifact_type = analysis.get("type", "unknown")
                artifact_results["artifact_types"][artifact_type] = \
                    artifact_results["artifact_types"].get(artifact_type, 0) + 1
                
                # Collect risk indicators
                if "risk_indicators" in analysis:
                    artifact_results["risk_indicators"].extend(analysis["risk_indicators"])
                
                # Collect technical findings
                if "technical_analysis" in analysis:
                    artifact_results["technical_findings"][artifact_type] = analysis["technical_analysis"]
                    
            except Exception as e:
                logger.error(f"Failed to analyze artifact: {str(e)}")
                artifact_results["analyzed_artifacts"].append({
                    "error": str(e),
                    "artifact": artifact
                })
        
        return artifact_results
    
    async def _fuse_intelligence(self, artifact_results: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Fuse intelligence from multiple sources"""
        
        intelligence_results = await self.intelligence_fusion.correlate_intelligence(
            artifact_results, context
        )
        
        return intelligence_results
    
    async def _conduct_ai_analysis(self, request: InvestigationRequest, artifact_results: Dict[str, Any], 
                                 intelligence_results: Dict[str, Any]) -> Dict[str, Any]:
        """Conduct AI analysis using appropriate models for the tier"""
        
        # Prepare comprehensive analysis prompt
        analysis_prompt = self._prepare_analysis_prompt(
            request, artifact_results, intelligence_results
        )
        
        # Prepare analysis context
        analysis_context = {
            "investigation_id": request.investigation_id,
            "tier": request.tier.value,
            "artifacts": artifact_results,
            "intelligence": intelligence_results,
            "user_context": request.context
        }
        
        # Conduct ensemble analysis
        ai_analysis = await self.model_manager.elite_ensemble_analysis(
            tier=request.tier,
            prompt=analysis_prompt,
            context=analysis_context
        )
        
        return ai_analysis
    
    def _prepare_analysis_prompt(self, request: InvestigationRequest, 
                               artifact_results: Dict[str, Any], 
                               intelligence_results: Dict[str, Any]) -> str:
        """Prepare comprehensive analysis prompt for AI models"""
        
        prompt = f"""
ELITE FRAUD INVESTIGATION ANALYSIS

INVESTIGATION PARAMETERS:
- Investigation ID: {request.investigation_id}
- Tier Level: {request.tier.value.upper()}
- Investigation Type: {request.investigation_type.value}
- Priority: {request.priority}

ARTIFACT ANALYSIS SUMMARY:
- Total Artifacts: {artifact_results.get('total_artifacts', 0)}
- Artifact Types: {json.dumps(artifact_results.get('artifact_types', {}), indent=2)}
- Risk Indicators Found: {len(artifact_results.get('risk_indicators', []))}

INTELLIGENCE CORRELATION:
{json.dumps(intelligence_results, indent=2)}

REQUIRED ANALYSIS COMPONENTS:

1. THREAT ASSESSMENT
   - Overall threat level (LOW/MEDIUM/HIGH/CRITICAL)
   - Specific threat indicators identified
   - Threat actor attribution (if applicable)
   - Attack vector analysis

2. EVIDENCE ANALYSIS
   - Artifact authenticity assessment
   - Pattern recognition across artifacts
   - Temporal analysis of threat evolution
   - Technical infrastructure analysis

3. BEHAVIORAL ANALYSIS
   - Social engineering indicators
   - Psychological manipulation techniques
   - Communication pattern analysis
   - Victim targeting methodology

4. STRATEGIC INTELLIGENCE
   - Campaign attribution and tracking
   - Related threat activity correlation
   - Predictive threat modeling
   - Strategic threat landscape assessment

5. ACTIONABLE RECOMMENDATIONS
   - Immediate protective actions
   - Long-term security improvements
   - Monitoring and detection strategies
   - Incident response procedures

6. CONFIDENCE ASSESSMENT
   - Analysis reliability score
   - Evidence quality evaluation
   - Uncertainty factors
   - Additional investigation needs

Provide detailed, actionable intelligence suitable for {request.tier.value} level decision-making.
Focus on specific, evidence-based findings with clear confidence indicators.
"""
        
        return prompt
    
    async def _assess_threat_level(self, ai_analysis: Dict[str, Any], 
                                 artifact_results: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall threat level based on analysis results"""
        
        # Extract threat indicators
        risk_indicators = artifact_results.get("risk_indicators", [])
        ai_threat_assessment = ai_analysis.get("ensemble_summary", {}).get("threat_assessment", "MEDIUM")
        confidence_score = ai_analysis.get("confidence_score", 0.5)
        
        # Calculate threat score
        threat_score = 0.0
        
        # Risk indicator scoring
        critical_indicators = ["confirmed_fraud", "active_scam", "malware_detected"]
        high_indicators = ["suspicious_domain", "fake_profile", "phishing_attempt"]
        medium_indicators = ["unusual_pattern", "potential_risk", "requires_verification"]
        
        for indicator in risk_indicators:
            indicator_lower = indicator.lower()
            if any(ci in indicator_lower for ci in critical_indicators):
                threat_score += 0.3
            elif any(hi in indicator_lower for hi in high_indicators):
                threat_score += 0.2
            elif any(mi in indicator_lower for mi in medium_indicators):
                threat_score += 0.1
        
        # AI assessment scoring
        ai_threat_mapping = {
            "CRITICAL": 0.4,
            "HIGH": 0.3,
            "MEDIUM": 0.2,
            "LOW": 0.1
        }
        threat_score += ai_threat_mapping.get(ai_threat_assessment, 0.2)
        
        # Confidence adjustment
        threat_score *= confidence_score
        
        # Determine final threat level
        if threat_score >= 0.7:
            threat_level = ThreatLevel.CRITICAL
        elif threat_score >= 0.5:
            threat_level = ThreatLevel.HIGH
        elif threat_score >= 0.3:
            threat_level = ThreatLevel.MEDIUM
        else:
            threat_level = ThreatLevel.LOW
        
        return {
            "threat_level": threat_level,
            "threat_score": threat_score,
            "confidence_score": confidence_score,
            "contributing_factors": {
                "risk_indicators": len(risk_indicators),
                "ai_assessment": ai_threat_assessment,
                "technical_findings": len(artifact_results.get("technical_findings", {}))
            }
        }
    
    async def _generate_recommendations(self, threat_assessment: Dict[str, Any], 
                                      ai_analysis: Dict[str, Any], 
                                      tier: ModelTier) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        
        recommendations = []
        threat_level = threat_assessment["threat_level"]
        confidence_score = threat_assessment["confidence_score"]
        
        # Immediate actions based on threat level
        if threat_level == ThreatLevel.CRITICAL:
            recommendations.extend([
                "🚨 IMMEDIATE ACTION REQUIRED: Do not engage with this entity under any circumstances",
                "🚨 STOP all financial transactions and communications immediately",
                "🚨 Report to law enforcement and relevant authorities immediately",
                "🚨 Secure all accounts and change passwords for any potentially compromised systems",
                "🚨 Monitor financial accounts for unauthorized activity"
            ])
        elif threat_level == ThreatLevel.HIGH:
            recommendations.extend([
                "⚠️ HIGH RISK: Avoid engagement and proceed with extreme caution",
                "⚠️ Verify through independent, trusted channels before any action",
                "⚠️ Report to appropriate authorities for investigation",
                "⚠️ Implement additional security measures and monitoring"
            ])
        elif threat_level == ThreatLevel.MEDIUM:
            recommendations.extend([
                "⚡ MEDIUM RISK: Exercise caution and verify independently",
                "⚡ Seek additional verification through trusted sources",
                "⚡ Monitor for additional suspicious activity",
                "⚡ Consider professional consultation if concerns persist"
            ])
        else:  # LOW
            recommendations.extend([
                "✅ LOW RISK: Appears legitimate but maintain standard security practices",
                "✅ Continue normal verification procedures",
                "✅ Monitor for any changes in behavior or patterns"
            ])
        
        # Tier-specific recommendations
        if tier in [ModelTier.ENTERPRISE, ModelTier.INTELLIGENCE]:
            recommendations.extend([
                "📊 Implement organizational threat monitoring for similar patterns",
                "📊 Update security policies based on identified threat vectors",
                "📊 Consider threat intelligence sharing with industry partners",
                "📊 Develop incident response procedures for similar threats"
            ])
        
        # Confidence-based recommendations
        if confidence_score < 0.7:
            recommendations.append(
                f"🔍 Consider upgrading to higher tier analysis for increased confidence (current: {confidence_score:.1%})"
            )
        
        # Extract AI-generated recommendations
        ai_recommendations = ai_analysis.get("ensemble_summary", {}).get("strategic_recommendations", [])
        recommendations.extend([f"🤖 AI Recommendation: {rec}" for rec in ai_recommendations])
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    async def _compile_investigation_result(self, request: InvestigationRequest,
                                          ai_analysis: Dict[str, Any],
                                          threat_assessment: Dict[str, Any],
                                          recommendations: List[str],
                                          start_time: datetime) -> InvestigationResult:
        """Compile final investigation result"""
        
        processing_time = (datetime.now(timezone.utc) - start_time).total_seconds()
        
        # Generate executive summary
        executive_summary = self._generate_executive_summary(
            request.tier, threat_assessment, ai_analysis
        )
        
        # Compile detailed findings
        detailed_findings = {
            "investigation_metadata": {
                "tier": request.tier.value,
                "investigation_type": request.investigation_type.value,
                "artifacts_analyzed": len(request.artifacts),
                "models_used": ai_analysis.get("models_used", []),
                "processing_time_seconds": processing_time
            },
            "threat_analysis": threat_assessment,
            "ai_analysis_summary": ai_analysis.get("ensemble_summary", {}),
            "model_consensus": ai_analysis.get("model_consensus", {}),
            "confidence_metrics": ai_analysis.get("confidence_metrics", {})
        }
        
        # Compile evidence analysis
        evidence_analysis = {
            "artifacts_processed": len(request.artifacts),
            "risk_indicators_found": threat_assessment.get("contributing_factors", {}).get("risk_indicators", 0),
            "technical_findings": threat_assessment.get("contributing_factors", {}).get("technical_findings", 0),
            "analysis_depth": request.tier.value,
            "evidence_quality": "High" if threat_assessment["confidence_score"] > 0.8 else "Medium"
        }
        
        return InvestigationResult(
            investigation_id=request.investigation_id,
            tier=request.tier,
            threat_level=threat_assessment["threat_level"],
            confidence_score=threat_assessment["confidence_score"],
            executive_summary=executive_summary,
            detailed_findings=detailed_findings,
            evidence_analysis=evidence_analysis,
            recommendations=recommendations,
            models_used=ai_analysis.get("models_used", []),
            processing_time=processing_time,
            cost=ai_analysis.get("total_cost", 0.0),
            timestamp=datetime.now(timezone.utc)
        )
    
    def _generate_executive_summary(self, tier: ModelTier, 
                                  threat_assessment: Dict[str, Any],
                                  ai_analysis: Dict[str, Any]) -> str:
        """Generate executive summary of investigation"""
        
        threat_level = threat_assessment["threat_level"].value.upper()
        confidence = threat_assessment["confidence_score"]
        models_count = len(ai_analysis.get("models_used", []))
        
        summary = f"""
EXECUTIVE SUMMARY - {tier.value.upper()} TIER INVESTIGATION

THREAT ASSESSMENT: {threat_level} RISK
CONFIDENCE LEVEL: {confidence:.1%}
ANALYSIS DEPTH: {models_count} AI models employed

"""
        
        if threat_level == "CRITICAL":
            summary += "🚨 CRITICAL THREAT IDENTIFIED: Immediate action required to prevent potential fraud or security breach. "
        elif threat_level == "HIGH":
            summary += "⚠️ HIGH RISK DETECTED: Significant threat indicators present requiring immediate attention. "
        elif threat_level == "MEDIUM":
            summary += "⚡ MEDIUM RISK IDENTIFIED: Suspicious patterns detected requiring verification and caution. "
        else:
            summary += "✅ LOW RISK ASSESSMENT: Entity appears legitimate with standard security practices recommended. "
        
        summary += f"Analysis conducted using {tier.value} tier capabilities with {confidence:.1%} confidence based on comprehensive evidence evaluation."
        
        return summary.strip()
    
    def get_investigation_status(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        """Get status of active investigation"""
        return self.active_investigations.get(investigation_id)
    
    def list_active_investigations(self) -> Dict[str, Any]:
        """List all active investigations"""
        return self.active_investigations
    
    async def cancel_investigation(self, investigation_id: str) -> bool:
        """Cancel an active investigation"""
        if investigation_id in self.active_investigations:
            self.active_investigations[investigation_id]["status"] = "cancelled"
            return True
        return False

