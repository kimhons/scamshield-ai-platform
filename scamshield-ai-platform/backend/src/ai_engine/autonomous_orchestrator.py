"""
ScamShield AI - Autonomous Orchestrator

Intelligent AI orchestration system that autonomously coordinates multiple AI models,
makes decisions, and adapts investigation strategies based on evidence and context.
"""

import asyncio
import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import openai
import anthropic
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import networkx as nx
import uuid

from ..utils.error_handler import ErrorContext, APIError
from ..utils.logging_config import get_logger
from .model_manager_v2 import ModelTier, AIModelManager
from .web_intelligence_engine import WebIntelligenceEngine, investigate_website
from .ocr_engine import AdvancedOCREngine, extract_text_from_image
from ..models.investigation import Investigation, Evidence, EvidenceType

logger = get_logger(__name__)


class AutonomyLevel(Enum):
    """Levels of autonomous operation"""
    MANUAL = "manual"              # Human-guided
    ASSISTED = "assisted"          # AI-assisted with human oversight
    SEMI_AUTONOMOUS = "semi_autonomous"  # Autonomous with human approval
    FULLY_AUTONOMOUS = "fully_autonomous"  # Complete autonomy


class DecisionType(Enum):
    """Types of decisions the orchestrator can make"""
    INVESTIGATION_STRATEGY = "investigation_strategy"
    MODEL_SELECTION = "model_selection"
    EVIDENCE_ANALYSIS = "evidence_analysis"
    RISK_ASSESSMENT = "risk_assessment"
    NEXT_ACTION = "next_action"
    RESOURCE_ALLOCATION = "resource_allocation"


class ConfidenceLevel(Enum):
    """Confidence levels for AI decisions"""
    VERY_LOW = "very_low"      # 0-20%
    LOW = "low"                # 20-40%
    MODERATE = "moderate"      # 40-60%
    HIGH = "high"              # 60-80%
    VERY_HIGH = "very_high"    # 80-100%


@dataclass
class AIDecision:
    """Represents an AI decision with context and confidence"""
    decision_id: str
    decision_type: DecisionType
    decision: str
    reasoning: str
    confidence: float
    evidence_used: List[str]
    models_consulted: List[str]
    alternatives_considered: List[Dict[str, Any]]
    timestamp: datetime
    context: Dict[str, Any]


@dataclass
class InvestigationPlan:
    """Dynamic investigation plan that adapts based on findings"""
    investigation_id: str
    current_phase: str
    planned_actions: List[Dict[str, Any]]
    completed_actions: List[Dict[str, Any]]
    evidence_graph: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    resource_allocation: Dict[str, Any]
    adaptation_history: List[Dict[str, Any]]
    estimated_completion: datetime
    confidence_score: float


@dataclass
class ModelConsensus:
    """Consensus result from multiple AI models"""
    consensus_decision: str
    individual_responses: List[Dict[str, Any]]
    agreement_score: float
    confidence_weighted_result: str
    dissenting_opinions: List[Dict[str, Any]]
    final_confidence: float


class IntelligentPromptEngine:
    """Advanced prompt engineering with context awareness"""
    
    def __init__(self):
        self.prompt_templates = {
            "fraud_analysis": {
                "system": """You are an elite fraud investigation AI with decades of expertise in financial crimes, cybersecurity, and behavioral analysis. Analyze the provided evidence with the methodical precision of a forensic investigator.""",
                "user": """Analyze this evidence for fraud indicators:

EVIDENCE TYPE: {evidence_type}
CONTENT: {content}

INVESTIGATION CONTEXT:
- Previous findings: {previous_findings}
- Risk level: {risk_level}
- Investigation phase: {phase}

Provide:
1. Fraud likelihood (0-100%)
2. Key fraud indicators
3. Recommended next steps
4. Confidence level
5. Alternative explanations

Be specific, actionable, and cite evidence for each conclusion."""
            },
            "risk_assessment": {
                "system": """You are a risk assessment specialist with expertise in cybersecurity threats, financial fraud, and social engineering attacks. Evaluate threats with the precision of a security analyst.""",
                "user": """Assess the risk level of this situation:

CURRENT EVIDENCE:
{evidence_summary}

CONTEXT:
- Investigation type: {investigation_type}
- Stakeholder impact: {stakeholder_impact}
- Time sensitivity: {time_sensitivity}

Provide a comprehensive risk assessment including:
1. Overall risk score (0-100)
2. Risk categories and severity
3. Potential impact scenarios
4. Mitigation strategies
5. Monitoring recommendations"""
            },
            "strategy_planning": {
                "system": """You are a strategic investigation planner with expertise in evidence collection, forensic analysis, and case management. Design investigation strategies with the thoroughness of a detective.""",
                "user": """Plan the next phase of this investigation:

CURRENT STATUS:
- Completed actions: {completed_actions}
- Available evidence: {available_evidence}
- Resource constraints: {resource_constraints}
- Time constraints: {time_constraints}

OBJECTIVES:
{investigation_objectives}

Create a detailed investigation plan including:
1. Prioritized action items
2. Resource allocation
3. Timeline estimates
4. Success metrics
5. Contingency plans
6. Risk mitigation strategies"""
            },
            "evidence_correlation": {
                "system": """You are a forensic analyst specializing in evidence correlation and pattern recognition. Identify connections with the analytical precision of a data scientist.""",
                "user": """Analyze correlations between these evidence items:

EVIDENCE SET:
{evidence_items}

KNOWN PATTERNS:
{known_patterns}

Identify:
1. Strong correlations and connections
2. Timeline reconstruction
3. Actor identification and relationships
4. Missing evidence gaps
5. Verification requirements
6. Pattern significance
7. Investigation implications"""
            }
        }
    
    def generate_prompt(
        self, 
        prompt_type: str, 
        context: Dict[str, Any],
        model_specific: bool = True,
        model_name: str = "gpt-4"
    ) -> Dict[str, str]:
        """Generate contextually aware prompts"""
        
        if prompt_type not in self.prompt_templates:
            raise APIError(f"Unknown prompt type: {prompt_type}")
        
        template = self.prompt_templates[prompt_type]
        
        # Format prompts with context
        try:
            system_prompt = template["system"]
            user_prompt = template["user"].format(**context)
            
            # Add model-specific optimizations
            if model_specific:
                system_prompt, user_prompt = self._optimize_for_model(
                    system_prompt, user_prompt, model_name
                )
            
            return {
                "system": system_prompt,
                "user": user_prompt
            }
        
        except KeyError as e:
            raise APIError(f"Missing context variable for prompt: {e}")
    
    def _optimize_for_model(self, system_prompt: str, user_prompt: str, model_name: str) -> Tuple[str, str]:
        """Optimize prompts for specific models"""
        
        if "gpt" in model_name.lower():
            # GPT optimizations
            system_prompt += "\n\nProvide structured, detailed responses with clear reasoning chains."
            
        elif "claude" in model_name.lower():
            # Claude optimizations  
            system_prompt += "\n\nThink step-by-step and provide comprehensive analysis with nuanced insights."
            
        elif "gemini" in model_name.lower():
            # Gemini optimizations
            system_prompt += "\n\nProvide creative yet analytical responses with multiple perspectives."
        
        return system_prompt, user_prompt


class EvidenceGraph:
    """Graph-based evidence relationship modeling"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.evidence_nodes = {}
        self.relationship_types = [
            "contains", "references", "connects_to", "contradicts",
            "supports", "originated_from", "leads_to", "similar_to"
        ]
    
    def add_evidence(self, evidence_id: str, evidence_data: Dict[str, Any]):
        """Add evidence node to graph"""
        self.graph.add_node(evidence_id, **evidence_data)
        self.evidence_nodes[evidence_id] = evidence_data
    
    def add_relationship(
        self, 
        source_id: str, 
        target_id: str, 
        relationship_type: str, 
        confidence: float,
        metadata: Dict[str, Any] = None
    ):
        """Add relationship between evidence items"""
        if relationship_type not in self.relationship_types:
            logger.warning(f"Unknown relationship type: {relationship_type}")
        
        self.graph.add_edge(
            source_id, 
            target_id, 
            relationship_type=relationship_type,
            confidence=confidence,
            metadata=metadata or {}
        )
    
    def find_evidence_clusters(self) -> List[List[str]]:
        """Find clusters of related evidence"""
        return list(nx.weakly_connected_components(self.graph))
    
    def get_evidence_importance(self) -> Dict[str, float]:
        """Calculate importance scores for evidence items"""
        # Use PageRank algorithm to determine importance
        importance_scores = nx.pagerank(self.graph)
        
        # Adjust for evidence quality and confidence
        adjusted_scores = {}
        for evidence_id, score in importance_scores.items():
            evidence_data = self.evidence_nodes.get(evidence_id, {})
            quality_factor = evidence_data.get('quality_score', 0.5)
            confidence_factor = evidence_data.get('confidence', 0.5)
            
            adjusted_scores[evidence_id] = score * quality_factor * confidence_factor
        
        return adjusted_scores
    
    def get_investigation_paths(self, start_evidence: str, max_depth: int = 5) -> List[List[str]]:
        """Find investigation paths from starting evidence"""
        paths = []
        
        def dfs_paths(current, target_depth, current_path):
            if target_depth == 0:
                paths.append(current_path.copy())
                return
            
            for neighbor in self.graph.neighbors(current):
                if neighbor not in current_path:  # Avoid cycles
                    current_path.append(neighbor)
                    dfs_paths(neighbor, target_depth - 1, current_path)
                    current_path.pop()
        
        dfs_paths(start_evidence, max_depth, [start_evidence])
        return paths
    
    def detect_inconsistencies(self) -> List[Dict[str, Any]]:
        """Detect contradictions and inconsistencies in evidence"""
        inconsistencies = []
        
        # Find contradictory relationships
        for source, target, data in self.graph.edges(data=True):
            if data.get('relationship_type') == 'contradicts':
                inconsistencies.append({
                    'type': 'contradiction',
                    'evidence_ids': [source, target],
                    'confidence': data.get('confidence', 0.0),
                    'description': f"Evidence {source} contradicts {target}"
                })
        
        # Find temporal inconsistencies
        # (Implementation would analyze timestamps and causality)
        
        return inconsistencies
    
    def export_graph_data(self) -> Dict[str, Any]:
        """Export graph for visualization and analysis"""
        return {
            'nodes': [
                {
                    'id': node_id,
                    **node_data
                }
                for node_id, node_data in self.graph.nodes(data=True)
            ],
            'edges': [
                {
                    'source': source,
                    'target': target,
                    **edge_data
                }
                for source, target, edge_data in self.graph.edges(data=True)
            ],
            'metrics': {
                'node_count': self.graph.number_of_nodes(),
                'edge_count': self.graph.number_of_edges(),
                'density': nx.density(self.graph),
                'clusters': len(self.find_evidence_clusters())
            }
        }


class AutonomousOrchestrator:
    """Main autonomous orchestration engine"""
    
    def __init__(self, autonomy_level: AutonomyLevel = AutonomyLevel.SEMI_AUTONOMOUS):
        self.autonomy_level = autonomy_level
        self.ai_manager = AIModelManager()
        self.prompt_engine = IntelligentPromptEngine()
        self.web_intelligence = WebIntelligenceEngine()
        self.ocr_engine = AdvancedOCREngine()
        
        # Decision making components
        self.decision_history = []
        self.active_investigations = {}
        self.model_performance_tracker = {}
        
        # Autonomous learning components
        self.pattern_recognizer = None
        self.decision_optimizer = None
        
        # Performance metrics
        self.metrics = {
            'decisions_made': 0,
            'successful_investigations': 0,
            'average_confidence': 0.0,
            'model_usage': {},
            'processing_time': []
        }
    
    async def initialize(self):
        """Initialize the orchestrator and all components"""
        with ErrorContext("orchestrator_initialization"):
            await self.web_intelligence.initialize()
            await self.ai_manager.initialize()
            
            # Load or train decision models
            await self._initialize_decision_models()
            
            logger.info("Autonomous orchestrator initialized", 
                       autonomy_level=self.autonomy_level.value)
    
    async def _initialize_decision_models(self):
        """Initialize ML models for autonomous decision making"""
        try:
            # Try to load existing models
            self.pattern_recognizer = joblib.load('models/pattern_recognizer.pkl')
            self.decision_optimizer = joblib.load('models/decision_optimizer.pkl')
            logger.info("Loaded existing decision models")
        except:
            # Initialize new models
            self.pattern_recognizer = RandomForestClassifier(n_estimators=100, random_state=42)
            self.decision_optimizer = RandomForestClassifier(n_estimators=100, random_state=42)
            logger.info("Initialized new decision models")
    
    async def start_investigation(
        self, 
        investigation_id: str, 
        evidence_items: List[Dict[str, Any]],
        investigation_type: str,
        priority: str = "normal"
    ) -> InvestigationPlan:
        """Start an autonomous investigation"""
        
        with ErrorContext("start_investigation", investigation_id=investigation_id):
            logger.info("Starting autonomous investigation", 
                       investigation_id=investigation_id,
                       evidence_count=len(evidence_items),
                       type=investigation_type)
            
            # Create evidence graph
            evidence_graph = EvidenceGraph()
            
            # Add evidence to graph
            for i, evidence in enumerate(evidence_items):
                evidence_id = f"evidence_{i}"
                evidence_graph.add_evidence(evidence_id, evidence)
            
            # Create initial investigation plan
            plan = await self._create_investigation_plan(
                investigation_id, evidence_items, investigation_type, priority, evidence_graph
            )
            
            # Store active investigation
            self.active_investigations[investigation_id] = {
                'plan': plan,
                'evidence_graph': evidence_graph,
                'start_time': datetime.now(timezone.utc)
            }
            
            # Start autonomous execution if appropriate
            if self.autonomy_level in [AutonomyLevel.SEMI_AUTONOMOUS, AutonomyLevel.FULLY_AUTONOMOUS]:
                asyncio.create_task(self._execute_investigation_autonomously(investigation_id))
            
            return plan
    
    async def _create_investigation_plan(
        self, 
        investigation_id: str,
        evidence_items: List[Dict[str, Any]],
        investigation_type: str,
        priority: str,
        evidence_graph: EvidenceGraph
    ) -> InvestigationPlan:
        """Create dynamic investigation plan using AI"""
        
        # Analyze evidence for initial strategy
        initial_analysis = await self._analyze_evidence_batch(evidence_items)
        
        # Generate investigation strategy using AI
        strategy_context = {
            'investigation_type': investigation_type,
            'evidence_summary': self._summarize_evidence(evidence_items),
            'priority': priority,
            'available_evidence': len(evidence_items),
            'resource_constraints': 'standard',
            'time_constraints': 'standard',
            'investigation_objectives': f"Comprehensive {investigation_type} investigation",
            'completed_actions': []
        }
        
        strategy_prompt = self.prompt_engine.generate_prompt("strategy_planning", strategy_context)
        strategy_response = await self._get_ai_consensus([
            {"model": "gpt-4", "prompt": strategy_prompt},
            {"model": "claude-3", "prompt": strategy_prompt}
        ])
        
        # Parse strategy response into actionable plan
        planned_actions = self._parse_strategy_to_actions(strategy_response.consensus_decision)
        
        # Create risk assessment
        risk_assessment = await self._assess_initial_risk(evidence_items, investigation_type)
        
        # Estimate completion time and resource allocation
        resource_allocation = self._allocate_resources(planned_actions, priority)
        estimated_completion = self._estimate_completion_time(planned_actions, resource_allocation)
        
        return InvestigationPlan(
            investigation_id=investigation_id,
            current_phase="initial_analysis",
            planned_actions=planned_actions,
            completed_actions=[],
            evidence_graph=evidence_graph.export_graph_data(),
            risk_assessment=risk_assessment,
            resource_allocation=resource_allocation,
            adaptation_history=[],
            estimated_completion=estimated_completion,
            confidence_score=strategy_response.final_confidence
        )
    
    async def _execute_investigation_autonomously(self, investigation_id: str):
        """Execute investigation plan autonomously"""
        
        with ErrorContext("autonomous_execution", investigation_id=investigation_id):
            investigation_data = self.active_investigations.get(investigation_id)
            if not investigation_data:
                logger.error("Investigation not found", investigation_id=investigation_id)
                return
            
            plan = investigation_data['plan']
            evidence_graph = investigation_data['evidence_graph']
            
            logger.info("Starting autonomous execution", 
                       investigation_id=investigation_id,
                       planned_actions=len(plan.planned_actions))
            
            while plan.planned_actions:
                # Get next action
                next_action = plan.planned_actions[0]
                
                try:
                    # Execute action
                    action_result = await self._execute_action(next_action, evidence_graph)
                    
                    # Update plan based on results
                    await self._update_plan_with_results(plan, next_action, action_result, evidence_graph)
                    
                    # Move action to completed
                    plan.completed_actions.append({
                        **next_action,
                        'result': action_result,
                        'completed_at': datetime.now(timezone.utc).isoformat()
                    })
                    plan.planned_actions.pop(0)
                    
                    # Check if investigation should be adapted
                    if self._should_adapt_strategy(action_result, plan):
                        await self._adapt_investigation_strategy(plan, evidence_graph)
                    
                    # Autonomous decision on whether to continue
                    should_continue = await self._decide_whether_to_continue(plan, evidence_graph)
                    if not should_continue:
                        logger.info("Autonomous decision to pause investigation", 
                                   investigation_id=investigation_id)
                        break
                
                except Exception as e:
                    logger.error("Action execution failed", 
                               investigation_id=investigation_id,
                               action=next_action,
                               error=str(e))
                    
                    # Autonomous error recovery
                    recovery_strategy = await self._determine_error_recovery(next_action, str(e))
                    if recovery_strategy == "skip":
                        plan.planned_actions.pop(0)
                    elif recovery_strategy == "retry":
                        # Retry with modifications
                        pass
                    elif recovery_strategy == "abort":
                        logger.error("Investigation aborted due to critical error")
                        break
            
            # Generate final report
            final_report = await self._generate_autonomous_report(investigation_id, plan, evidence_graph)
            
            logger.info("Autonomous investigation completed", 
                       investigation_id=investigation_id,
                       actions_completed=len(plan.completed_actions))
    
    async def _execute_action(self, action: Dict[str, Any], evidence_graph: EvidenceGraph) -> Dict[str, Any]:
        """Execute a single investigation action"""
        
        action_type = action.get('type')
        action_params = action.get('parameters', {})
        
        if action_type == "url_investigation":
            result = await investigate_website(action_params['url'])
            
            # Add results to evidence graph
            evidence_id = f"web_evidence_{uuid.uuid4().hex[:8]}"
            evidence_graph.add_evidence(evidence_id, {
                'type': 'web_investigation',
                'url': action_params['url'],
                'result': result,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            
            return {
                'status': 'completed',
                'evidence_id': evidence_id,
                'findings': result,
                'confidence': result.get('risk_assessment', {}).get('confidence', 0.5)
            }
        
        elif action_type == "image_analysis":
            image_data = action_params['image_data']
            ocr_result = await self.ocr_engine.extract_text(image_data)
            
            # Analyze extracted text for fraud indicators
            fraud_analysis = self.ocr_engine.extract_specific_patterns(ocr_result.text)
            
            evidence_id = f"image_evidence_{uuid.uuid4().hex[:8]}"
            evidence_graph.add_evidence(evidence_id, {
                'type': 'image_analysis',
                'ocr_result': asdict(ocr_result),
                'fraud_analysis': fraud_analysis,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            
            return {
                'status': 'completed',
                'evidence_id': evidence_id,
                'text_extracted': ocr_result.text,
                'fraud_indicators': fraud_analysis,
                'confidence': ocr_result.confidence
            }
        
        elif action_type == "ai_analysis":
            # Perform AI analysis on specific evidence
            evidence_id = action_params['evidence_id']
            analysis_type = action_params['analysis_type']
            
            evidence_data = evidence_graph.evidence_nodes.get(evidence_id)
            if not evidence_data:
                raise APIError(f"Evidence {evidence_id} not found")
            
            # Generate appropriate prompt
            if analysis_type == "fraud_analysis":
                context = {
                    'evidence_type': evidence_data.get('type'),
                    'content': str(evidence_data),
                    'previous_findings': self._get_previous_findings(evidence_graph),
                    'risk_level': 'medium',
                    'phase': 'detailed_analysis'
                }
                prompt = self.prompt_engine.generate_prompt("fraud_analysis", context)
            else:
                raise APIError(f"Unknown analysis type: {analysis_type}")
            
            # Get AI consensus
            consensus = await self._get_ai_consensus([
                {"model": "gpt-4", "prompt": prompt},
                {"model": "claude-3", "prompt": prompt}
            ])
            
            analysis_evidence_id = f"ai_analysis_{uuid.uuid4().hex[:8]}"
            evidence_graph.add_evidence(analysis_evidence_id, {
                'type': 'ai_analysis',
                'target_evidence': evidence_id,
                'analysis_type': analysis_type,
                'result': consensus.consensus_decision,
                'confidence': consensus.final_confidence,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            
            return {
                'status': 'completed',
                'evidence_id': analysis_evidence_id,
                'analysis_result': consensus.consensus_decision,
                'confidence': consensus.final_confidence
            }
        
        else:
            raise APIError(f"Unknown action type: {action_type}")
    
    async def _get_ai_consensus(self, model_requests: List[Dict[str, Any]]) -> ModelConsensus:
        """Get consensus from multiple AI models"""
        
        responses = []
        
        # Execute requests in parallel
        tasks = []
        for request in model_requests:
            model_name = request['model']
            prompt = request['prompt']
            
            if model_name.startswith('gpt'):
                task = self._query_openai(prompt)
            elif model_name.startswith('claude'):
                task = self._query_anthropic(prompt)
            elif model_name.startswith('gemini'):
                task = self._query_gemini(prompt)
            else:
                continue
            
            tasks.append(asyncio.create_task(task))
        
        # Wait for all responses
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process responses
        for i, result in enumerate(results):
            if not isinstance(result, Exception):
                responses.append({
                    'model': model_requests[i]['model'],
                    'response': result,
                    'confidence': self._extract_confidence(result)
                })
        
        if not responses:
            raise APIError("No valid AI responses received")
        
        # Calculate consensus
        consensus_decision = self._calculate_consensus(responses)
        agreement_score = self._calculate_agreement_score(responses)
        confidence_weighted_result = self._calculate_confidence_weighted_result(responses)
        final_confidence = self._calculate_final_confidence(responses, agreement_score)
        
        return ModelConsensus(
            consensus_decision=consensus_decision,
            individual_responses=responses,
            agreement_score=agreement_score,
            confidence_weighted_result=confidence_weighted_result,
            dissenting_opinions=self._find_dissenting_opinions(responses),
            final_confidence=final_confidence
        )
    
    async def _query_openai(self, prompt: Dict[str, str]) -> str:
        """Query OpenAI model"""
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user"]}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI query failed: {str(e)}")
            raise
    
    async def _query_anthropic(self, prompt: Dict[str, str]) -> str:
        """Query Anthropic model"""
        try:
            client = anthropic.Anthropic()
            response = await client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=2000,
                system=prompt["system"],
                messages=[{"role": "user", "content": prompt["user"]}]
            )
            return response.content[0].text
        except Exception as e:
            logger.error(f"Anthropic query failed: {str(e)}")
            raise
    
    async def _query_gemini(self, prompt: Dict[str, str]) -> str:
        """Query Google Gemini model"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            full_prompt = f"{prompt['system']}\n\n{prompt['user']}"
            response = await model.generate_content_async(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini query failed: {str(e)}")
            raise
    
    def _extract_confidence(self, response: str) -> float:
        """Extract confidence score from AI response"""
        # Simple pattern matching for confidence indicators
        import re
        
        confidence_patterns = [
            r'confidence:?\s*(\d+(?:\.\d+)?)[%]?',
            r'(\d+(?:\.\d+)?)[%]?\s*confident',
            r'likelihood:?\s*(\d+(?:\.\d+)?)[%]?'
        ]
        
        for pattern in confidence_patterns:
            match = re.search(pattern, response.lower())
            if match:
                confidence = float(match.group(1))
                return confidence / 100.0 if confidence > 1.0 else confidence
        
        # Default confidence based on response characteristics
        if "very confident" in response.lower() or "certain" in response.lower():
            return 0.9
        elif "confident" in response.lower() or "likely" in response.lower():
            return 0.7
        elif "possible" in response.lower() or "might" in response.lower():
            return 0.5
        elif "uncertain" in response.lower() or "unclear" in response.lower():
            return 0.3
        else:
            return 0.6  # Default moderate confidence
    
    def _calculate_consensus(self, responses: List[Dict[str, Any]]) -> str:
        """Calculate consensus decision from multiple responses"""
        # Simple majority-based consensus for now
        # Could be enhanced with semantic similarity analysis
        
        response_texts = [r['response'] for r in responses]
        
        # For now, return the response with highest confidence
        best_response = max(responses, key=lambda r: r['confidence'])
        return best_response['response']
    
    def _calculate_agreement_score(self, responses: List[Dict[str, Any]]) -> float:
        """Calculate how much the responses agree"""
        # Simplified agreement calculation
        # Could be enhanced with semantic similarity
        
        if len(responses) < 2:
            return 1.0
        
        # Calculate based on confidence variance
        confidences = [r['confidence'] for r in responses]
        confidence_variance = np.var(confidences)
        
        # Lower variance = higher agreement
        agreement_score = max(0.0, 1.0 - confidence_variance)
        
        return agreement_score
    
    def _calculate_confidence_weighted_result(self, responses: List[Dict[str, Any]]) -> str:
        """Calculate result weighted by confidence scores"""
        # Return the response with highest confidence
        best_response = max(responses, key=lambda r: r['confidence'])
        return best_response['response']
    
    def _calculate_final_confidence(self, responses: List[Dict[str, Any]], agreement_score: float) -> float:
        """Calculate final confidence score"""
        # Combine individual confidences with agreement score
        avg_confidence = np.mean([r['confidence'] for r in responses])
        final_confidence = avg_confidence * agreement_score
        
        return min(1.0, final_confidence)
    
    def _find_dissenting_opinions(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find responses that significantly differ from consensus"""
        if len(responses) < 2:
            return []
        
        avg_confidence = np.mean([r['confidence'] for r in responses])
        dissenting = []
        
        for response in responses:
            if abs(response['confidence'] - avg_confidence) > 0.3:
                dissenting.append(response)
        
        return dissenting
    
    # Additional helper methods would continue here...
    
    async def make_autonomous_decision(
        self, 
        decision_type: DecisionType, 
        context: Dict[str, Any]
    ) -> AIDecision:
        """Make an autonomous decision based on context"""
        
        with ErrorContext("autonomous_decision", decision_type=decision_type.value):
            decision_id = str(uuid.uuid4())
            
            # Check autonomy level permissions
            if not self._can_make_decision(decision_type):
                raise APIError(f"Autonomy level {self.autonomy_level.value} cannot make {decision_type.value} decisions")
            
            # Generate decision using AI consensus
            decision_prompt = self._generate_decision_prompt(decision_type, context)
            consensus = await self._get_ai_consensus([
                {"model": "gpt-4", "prompt": decision_prompt},
                {"model": "claude-3", "prompt": decision_prompt}
            ])
            
            # Create decision record
            decision = AIDecision(
                decision_id=decision_id,
                decision_type=decision_type,
                decision=consensus.consensus_decision,
                reasoning=f"AI consensus with {consensus.agreement_score:.2f} agreement",
                confidence=consensus.final_confidence,
                evidence_used=context.get('evidence_ids', []),
                models_consulted=[r['model'] for r in consensus.individual_responses],
                alternatives_considered=consensus.dissenting_opinions,
                timestamp=datetime.now(timezone.utc),
                context=context
            )
            
            # Store decision
            self.decision_history.append(decision)
            
            # Update metrics
            self.metrics['decisions_made'] += 1
            self.metrics['average_confidence'] = (
                (self.metrics['average_confidence'] * (self.metrics['decisions_made'] - 1) + 
                 consensus.final_confidence) / self.metrics['decisions_made']
            )
            
            logger.info("Autonomous decision made",
                       decision_id=decision_id,
                       decision_type=decision_type.value,
                       confidence=consensus.final_confidence)
            
            return decision
    
    def _can_make_decision(self, decision_type: DecisionType) -> bool:
        """Check if current autonomy level allows this decision type"""
        
        if self.autonomy_level == AutonomyLevel.MANUAL:
            return False
        elif self.autonomy_level == AutonomyLevel.ASSISTED:
            return decision_type in [DecisionType.MODEL_SELECTION]
        elif self.autonomy_level == AutonomyLevel.SEMI_AUTONOMOUS:
            return decision_type not in [DecisionType.RESOURCE_ALLOCATION]
        else:  # FULLY_AUTONOMOUS
            return True
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.web_intelligence:
            await self.web_intelligence.cleanup()


# Convenience functions
async def create_autonomous_investigator(
    autonomy_level: AutonomyLevel = AutonomyLevel.SEMI_AUTONOMOUS
) -> AutonomousOrchestrator:
    """
    Create and initialize autonomous investigator
    
    Args:
        autonomy_level: Level of autonomy for the investigator
        
    Returns:
        Initialized autonomous orchestrator
    """
    orchestrator = AutonomousOrchestrator(autonomy_level)
    await orchestrator.initialize()
    return orchestrator


async def run_autonomous_investigation(
    evidence_items: List[Dict[str, Any]],
    investigation_type: str,
    autonomy_level: AutonomyLevel = AutonomyLevel.SEMI_AUTONOMOUS
) -> Dict[str, Any]:
    """
    Run a complete autonomous investigation
    
    Args:
        evidence_items: Initial evidence to analyze
        investigation_type: Type of investigation
        autonomy_level: Level of autonomy
        
    Returns:
        Investigation results
    """
    orchestrator = await create_autonomous_investigator(autonomy_level)
    
    try:
        investigation_id = str(uuid.uuid4())
        plan = await orchestrator.start_investigation(
            investigation_id, evidence_items, investigation_type
        )
        
        # Wait for completion if fully autonomous
        if autonomy_level == AutonomyLevel.FULLY_AUTONOMOUS:
            # Would implement waiting logic here
            pass
        
        return {
            'investigation_id': investigation_id,
            'plan': asdict(plan),
            'status': 'started' if autonomy_level != AutonomyLevel.FULLY_AUTONOMOUS else 'completed'
        }
    
    finally:
        await orchestrator.cleanup()
