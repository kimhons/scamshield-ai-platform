"""
ScamShield AI - Data Models Package

This package contains all database models for the ScamShield AI platform.
"""

from .user import User, db
from .investigation import Investigation, Report, Evidence, ScamDatabase
from .credit_system import (
    Subscription, CreditTransaction, CreditConsumptionRule, SubscriptionPlan,
    CreditUsageAnalytics, SubscriptionTier, CreditTransactionType,
    InvestigationComplexity, ProcessingPriority, CreditCalculator
)

__all__ = [
    'User', 'db',
    'Investigation', 'Report', 'Evidence', 'ScamDatabase',
    'Subscription', 'CreditTransaction', 'CreditConsumptionRule', 'SubscriptionPlan',
    'CreditUsageAnalytics', 'SubscriptionTier', 'CreditTransactionType',
    'InvestigationComplexity', 'ProcessingPriority', 'CreditCalculator'
]
