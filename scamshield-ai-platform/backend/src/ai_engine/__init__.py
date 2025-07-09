"""
ScamShield AI Engine - Hybrid AI Architecture

This package implements a sophisticated hybrid AI architecture that combines
the most powerful open-source models with advanced proprietary models to
provide elite-level investigation capabilities.

Architecture Overview:
- Open Source Models: Llama 3.1, Mistral, CodeLlama, specialized fraud models
- Proprietary Models: GPT-4, Claude 3.5, Gemini Pro, specialized APIs
- Intelligent Routing: Automatic model selection based on investigation tier
- Model Ensemble: Combining multiple models for enhanced accuracy
"""

from .model_manager import ModelManager
from .investigation_engine import InvestigationEngine
from .intelligence_fusion import IntelligenceFusion
from .artifact_analyzer import ArtifactAnalyzer

__all__ = [
    'ModelManager',
    'InvestigationEngine', 
    'IntelligenceFusion',
    'ArtifactAnalyzer'
]

