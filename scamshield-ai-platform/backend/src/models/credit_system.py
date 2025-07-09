"""
ScamShield AI - Credit System Models

Database models for credit management, subscriptions, and billing.
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List
import uuid
from enum import Enum
from decimal import Decimal

from .user import db

class SubscriptionTier(Enum):
    """Subscription tier enumeration"""
    FREE = "free"
    BASIC = "basic"
    PLUS = "plus"
    PRO = "pro"
    ENTERPRISE = "enterprise"

class SubscriptionStatus(Enum):
    """Subscription status enumeration"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    SUSPENDED = "suspended"

class CreditTransactionType(Enum):
    """Credit transaction type enumeration"""
    PURCHASE = "purchase"
    CONSUMPTION = "consumption"
    REFUND = "refund"
    BONUS = "bonus"
    ROLLOVER = "rollover"
    EXPIRATION = "expiration"

class InvestigationComplexity(Enum):
    """Investigation complexity enumeration"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ELITE = "elite"

class ProcessingPriority(Enum):
    """Processing priority enumeration"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class SubscriptionPlan(db.Model):
    """Subscription plan model defining available tiers"""
    
    __tablename__ = 'subscription_plans'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Plan details
    tier = db.Column(db.Enum(SubscriptionTier), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Pricing
    monthly_price = db.Column(db.Float, nullable=False)
    annual_price = db.Column(db.Float, nullable=True)
    monthly_credits = db.Column(db.Integer, nullable=False)
    
    # Features
    max_investigations_per_day = db.Column(db.Integer, nullable=True)
    max_investigations_per_month = db.Column(db.Integer, nullable=True)
    allowed_models = db.Column(db.JSON, nullable=True)  # List of allowed AI models
    priority_processing = db.Column(db.Boolean, default=False, nullable=False)
    api_access = db.Column(db.Boolean, default=False, nullable=False)
    
    # Configuration
    credit_rollover_enabled = db.Column(db.Boolean, default=False, nullable=False)
    max_rollover_credits = db.Column(db.Integer, nullable=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert subscription plan to dictionary representation"""
        return {
            'id': self.id,
            'tier': self.tier.value,
            'name': self.name,
            'description': self.description,
            'monthly_price': self.monthly_price,
            'annual_price': self.annual_price,
            'monthly_credits': self.monthly_credits,
            'max_investigations_per_day': self.max_investigations_per_day,
            'max_investigations_per_month': self.max_investigations_per_month,
            'allowed_models': self.allowed_models,
            'priority_processing': self.priority_processing,
            'api_access': self.api_access,
            'credit_rollover_enabled': self.credit_rollover_enabled,
            'max_rollover_credits': self.max_rollover_credits,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self) -> str:
        return f'<SubscriptionPlan {self.tier.value}: {self.name}>'

class Subscription(db.Model):
    """Subscription model for user subscriptions"""
    
    __tablename__ = 'subscriptions'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    plan_id = db.Column(db.String(36), db.ForeignKey('subscription_plans.id'), nullable=False, index=True)
    
    # Subscription details
    tier = db.Column(db.Enum(SubscriptionTier), nullable=False, index=True)
    status = db.Column(db.Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE, nullable=False, index=True)
    
    # Credits
    monthly_credits = db.Column(db.Integer, nullable=False)
    current_credits = db.Column(db.Integer, default=0, nullable=False)
    rollover_credits = db.Column(db.Integer, default=0, nullable=False)
    bonus_credits = db.Column(db.Integer, default=0, nullable=False)
    
    # Billing
    billing_cycle = db.Column(db.String(20), default='monthly', nullable=False)  # monthly, annual
    next_billing_date = db.Column(db.Date, nullable=True)
    amount = db.Column(db.Float, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    started_at = db.Column(db.DateTime(timezone=True), nullable=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=True)
    cancelled_at = db.Column(db.DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = db.relationship('User', back_populates='subscriptions')
    plan = db.relationship('SubscriptionPlan')
    
    @property
    def total_credits(self) -> int:
        """Calculate total available credits"""
        return self.current_credits + self.rollover_credits + self.bonus_credits
    
    def consume_credits(self, amount: int) -> bool:
        """Consume credits from subscription"""
        if self.total_credits < amount:
            return False
        
        remaining = amount
        
        # Consume bonus credits first
        if self.bonus_credits > 0:
            consume_bonus = min(remaining, self.bonus_credits)
            self.bonus_credits -= consume_bonus
            remaining -= consume_bonus
        
        # Then rollover credits
        if remaining > 0 and self.rollover_credits > 0:
            consume_rollover = min(remaining, self.rollover_credits)
            self.rollover_credits -= consume_rollover
            remaining -= consume_rollover
        
        # Finally current credits
        if remaining > 0:
            self.current_credits -= remaining
        
        return True
    
    def add_credits(self, amount: int, credit_type: str = 'current') -> None:
        """Add credits to subscription"""
        if credit_type == 'bonus':
            self.bonus_credits += amount
        elif credit_type == 'rollover':
            self.rollover_credits += amount
        else:
            self.current_credits += amount
    
    def reset_monthly_credits(self) -> None:
        """Reset monthly credits and handle rollover"""
        if self.plan and self.plan.credit_rollover_enabled:
            # Calculate rollover amount
            rollover_amount = min(self.current_credits, self.plan.max_rollover_credits or 0)
            self.rollover_credits += rollover_amount
        
        # Reset current credits to monthly allowance
        self.current_credits = self.monthly_credits
        
        # Update next billing date
        if self.billing_cycle == 'monthly':
            self.next_billing_date = (datetime.now().date() + timedelta(days=30))
        elif self.billing_cycle == 'annual':
            self.next_billing_date = (datetime.now().date() + timedelta(days=365))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert subscription to dictionary representation"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'plan_id': self.plan_id,
            'tier': self.tier.value,
            'status': self.status.value,
            'monthly_credits': self.monthly_credits,
            'current_credits': self.current_credits,
            'rollover_credits': self.rollover_credits,
            'bonus_credits': self.bonus_credits,
            'total_credits': self.total_credits,
            'billing_cycle': self.billing_cycle,
            'next_billing_date': self.next_billing_date.isoformat() if self.next_billing_date else None,
            'amount': self.amount,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
        }
    
    def __repr__(self) -> str:
        return f'<Subscription {self.user_id}: {self.tier.value}>'

class CreditTransaction(db.Model):
    """Credit transaction model for tracking credit usage"""
    
    __tablename__ = 'credit_transactions'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign keys
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    subscription_id = db.Column(db.String(36), db.ForeignKey('subscriptions.id'), nullable=False, index=True)
    investigation_id = db.Column(db.String(36), db.ForeignKey('investigations.id'), nullable=True, index=True)
    
    # Transaction details
    transaction_type = db.Column(db.Enum(CreditTransactionType), nullable=False, index=True)
    amount = db.Column(db.Integer, nullable=False)  # Positive for additions, negative for consumption
    description = db.Column(db.String(255), nullable=True)
    
    # Metadata
    complexity = db.Column(db.Enum(InvestigationComplexity), nullable=True)
    priority = db.Column(db.Enum(ProcessingPriority), nullable=True)
    model_used = db.Column(db.String(100), nullable=True)
    processing_time = db.Column(db.Float, nullable=True)
    
    # Balance tracking
    balance_before = db.Column(db.Integer, nullable=False)
    balance_after = db.Column(db.Integer, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='credit_transactions')
    subscription = db.relationship('Subscription')
    investigation = db.relationship('Investigation')
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert credit transaction to dictionary representation"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'subscription_id': self.subscription_id,
            'investigation_id': self.investigation_id,
            'transaction_type': self.transaction_type.value,
            'amount': self.amount,
            'description': self.description,
            'complexity': self.complexity.value if self.complexity else None,
            'priority': self.priority.value if self.priority else None,
            'model_used': self.model_used,
            'processing_time': self.processing_time,
            'balance_before': self.balance_before,
            'balance_after': self.balance_after,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self) -> str:
        return f'<CreditTransaction {self.transaction_type.value}: {self.amount}>'

class CreditConsumptionRule(db.Model):
    """Credit consumption rules for different operations"""
    
    __tablename__ = 'credit_consumption_rules'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Rule details
    operation_type = db.Column(db.String(100), nullable=False, index=True)  # investigation_type
    complexity = db.Column(db.Enum(InvestigationComplexity), nullable=False, index=True)
    priority = db.Column(db.Enum(ProcessingPriority), nullable=False, index=True)
    tier = db.Column(db.Enum(SubscriptionTier), nullable=False, index=True)
    
    # Credit cost
    base_credits = db.Column(db.Integer, nullable=False)
    per_artifact_credits = db.Column(db.Integer, default=0, nullable=False)
    model_multiplier = db.Column(db.Float, default=1.0, nullable=False)
    priority_multiplier = db.Column(db.Float, default=1.0, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
    
    def calculate_credits(self, artifact_count: int = 1, model_tier_multiplier: float = 1.0) -> int:
        """Calculate credit cost for an operation"""
        base_cost = self.base_credits + (self.per_artifact_credits * artifact_count)
        total_cost = base_cost * self.model_multiplier * self.priority_multiplier * model_tier_multiplier
        return max(1, int(total_cost))  # Minimum 1 credit
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert credit consumption rule to dictionary representation"""
        return {
            'id': self.id,
            'operation_type': self.operation_type,
            'complexity': self.complexity.value,
            'priority': self.priority.value,
            'tier': self.tier.value,
            'base_credits': self.base_credits,
            'per_artifact_credits': self.per_artifact_credits,
            'model_multiplier': self.model_multiplier,
            'priority_multiplier': self.priority_multiplier,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self) -> str:
        return f'<CreditConsumptionRule {self.operation_type}: {self.base_credits} credits>'

class CreditUsageAnalytics(db.Model):
    """Credit usage analytics for reporting and optimization"""
    
    __tablename__ = 'credit_usage_analytics'
    
    # Primary key
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Analytics period
    period_start = db.Column(db.Date, nullable=False, index=True)
    period_end = db.Column(db.Date, nullable=False, index=True)
    period_type = db.Column(db.String(20), nullable=False)  # daily, weekly, monthly
    
    # User/subscription info
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)
    subscription_tier = db.Column(db.Enum(SubscriptionTier), nullable=False, index=True)
    
    # Usage statistics
    total_credits_consumed = db.Column(db.Integer, default=0, nullable=False)
    total_investigations = db.Column(db.Integer, default=0, nullable=False)
    avg_credits_per_investigation = db.Column(db.Float, default=0.0, nullable=False)
    
    # Operation breakdown
    quick_scan_count = db.Column(db.Integer, default=0, nullable=False)
    deep_analysis_count = db.Column(db.Integer, default=0, nullable=False)
    comprehensive_count = db.Column(db.Integer, default=0, nullable=False)
    elite_intelligence_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Model usage
    model_usage_breakdown = db.Column(db.JSON, nullable=True)  # Model name -> usage count
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert credit usage analytics to dictionary representation"""
        return {
            'id': self.id,
            'period_start': self.period_start.isoformat() if self.period_start else None,
            'period_end': self.period_end.isoformat() if self.period_end else None,
            'period_type': self.period_type,
            'user_id': self.user_id,
            'subscription_tier': self.subscription_tier.value,
            'total_credits_consumed': self.total_credits_consumed,
            'total_investigations': self.total_investigations,
            'avg_credits_per_investigation': self.avg_credits_per_investigation,
            'quick_scan_count': self.quick_scan_count,
            'deep_analysis_count': self.deep_analysis_count,
            'comprehensive_count': self.comprehensive_count,
            'elite_intelligence_count': self.elite_intelligence_count,
            'model_usage_breakdown': self.model_usage_breakdown,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
    
    def __repr__(self) -> str:
        return f'<CreditUsageAnalytics {self.period_type}: {self.total_credits_consumed} credits>'

class CreditCalculator:
    """Utility class for credit calculations"""
    
    @staticmethod
    def calculate_investigation_cost(
        investigation_type: str,
        complexity: InvestigationComplexity,
        priority: ProcessingPriority,
        tier: SubscriptionTier,
        artifact_count: int = 1,
        model_tier_multiplier: float = 1.0
    ) -> int:
        """Calculate credit cost for an investigation"""
        # Get consumption rule
        rule = CreditConsumptionRule.query.filter_by(
            operation_type=investigation_type,
            complexity=complexity,
            priority=priority,
            tier=tier
        ).first()
        
        if not rule:
            # Default fallback calculation
            base_costs = {
                InvestigationComplexity.SIMPLE: 1,
                InvestigationComplexity.MODERATE: 3,
                InvestigationComplexity.COMPLEX: 7,
                InvestigationComplexity.ELITE: 15
            }
            priority_multipliers = {
                ProcessingPriority.LOW: 0.8,
                ProcessingPriority.NORMAL: 1.0,
                ProcessingPriority.HIGH: 1.5,
                ProcessingPriority.URGENT: 2.0
            }
            tier_multipliers = {
                SubscriptionTier.FREE: 1.0,
                SubscriptionTier.BASIC: 0.9,
                SubscriptionTier.PLUS: 0.8,
                SubscriptionTier.PRO: 0.7,
                SubscriptionTier.ENTERPRISE: 0.6
            }
            
            base_cost = base_costs.get(complexity, 5)
            priority_mult = priority_multipliers.get(priority, 1.0)
            tier_mult = tier_multipliers.get(tier, 1.0)
            
            total_cost = base_cost * priority_mult * tier_mult * model_tier_multiplier * artifact_count
            return max(1, int(total_cost))
        
        return rule.calculate_credits(artifact_count, model_tier_multiplier)

# Default subscription plans data
DEFAULT_SUBSCRIPTION_PLANS = [
    {
        'tier': SubscriptionTier.FREE,
        'name': 'Free Tier',
        'description': 'Basic scam detection for personal use',
        'monthly_price': 0.0,
        'annual_price': 0.0,
        'monthly_credits': 3,
        'max_investigations_per_day': 1,
        'max_investigations_per_month': 3,
        'allowed_models': ['basic'],
        'priority_processing': False,
        'api_access': False,
        'credit_rollover_enabled': False,
        'max_rollover_credits': 0,
    },
    {
        'tier': SubscriptionTier.BASIC,
        'name': 'Basic Plan',
        'description': 'Enhanced protection for individuals',
        'monthly_price': 19.99,
        'annual_price': 199.99,
        'monthly_credits': 10,
        'max_investigations_per_day': 3,
        'max_investigations_per_month': 10,
        'allowed_models': ['basic', 'standard'],
        'priority_processing': False,
        'api_access': False,
        'credit_rollover_enabled': True,
        'max_rollover_credits': 5,
    },
    {
        'tier': SubscriptionTier.PLUS,
        'name': 'Plus Plan',
        'description': 'Advanced protection for power users',
        'monthly_price': 89.99,
        'annual_price': 899.99,
        'monthly_credits': 25,
        'max_investigations_per_day': 8,
        'max_investigations_per_month': 25,
        'allowed_models': ['basic', 'standard', 'advanced'],
        'priority_processing': True,
        'api_access': True,
        'credit_rollover_enabled': True,
        'max_rollover_credits': 15,
    },
    {
        'tier': SubscriptionTier.PRO,
        'name': 'Professional Plan',
        'description': 'Elite protection for businesses',
        'monthly_price': 399.99,
        'annual_price': 3999.99,
        'monthly_credits': 100,
        'max_investigations_per_day': 33,
        'max_investigations_per_month': 100,
        'allowed_models': ['basic', 'standard', 'advanced', 'premium'],
        'priority_processing': True,
        'api_access': True,
        'credit_rollover_enabled': True,
        'max_rollover_credits': 50,
    },
    {
        'tier': SubscriptionTier.ENTERPRISE,
        'name': 'Enterprise Plan',
        'description': 'Custom enterprise solutions',
        'monthly_price': 999.99,
        'annual_price': 9999.99,
        'monthly_credits': 500,
        'max_investigations_per_day': None,
        'max_investigations_per_month': None,
        'allowed_models': ['basic', 'standard', 'advanced', 'premium', 'elite'],
        'priority_processing': True,
        'api_access': True,
        'credit_rollover_enabled': True,
        'max_rollover_credits': 200,
    }
]
