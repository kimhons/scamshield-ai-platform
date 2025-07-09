"""
ScamShield AI - Credit System Model Tests

Comprehensive tests for credit system models including subscriptions, transactions, and analytics.
"""

import pytest
from datetime import datetime, timezone, timedelta, date
from decimal import Decimal

from models.credit_system import (
    SubscriptionPlan, Subscription, CreditTransaction, CreditConsumptionRule,
    CreditUsageAnalytics, CreditCalculator,
    SubscriptionTier, SubscriptionStatus, CreditTransactionType,
    InvestigationComplexity, ProcessingPriority
)


@pytest.mark.unit
class TestSubscriptionPlanModel:
    """Test cases for SubscriptionPlan model"""
    
    def test_subscription_plan_creation(self, db):
        """Test basic subscription plan creation"""
        plan = SubscriptionPlan(
            tier=SubscriptionTier.BASIC,
            name='Basic Plan',
            description='Basic fraud detection for individuals',
            monthly_price=19.99,
            annual_price=199.99,
            monthly_credits=10
        )
        db.session.add(plan)
        db.session.commit()
        
        assert plan.id is not None
        assert plan.tier == SubscriptionTier.BASIC
        assert plan.name == 'Basic Plan'
        assert plan.description == 'Basic fraud detection for individuals'
        assert plan.monthly_price == 19.99
        assert plan.annual_price == 199.99
        assert plan.monthly_credits == 10
        assert plan.is_active is True
        assert plan.priority_processing is False
        assert plan.api_access is False
        assert plan.credit_rollover_enabled is False
    
    def test_subscription_plan_with_features(self, db):
        """Test subscription plan with advanced features"""
        allowed_models = ['gpt-4', 'claude-3', 'gemini-pro']
        
        plan = SubscriptionPlan(
            tier=SubscriptionTier.PRO,
            name='Professional Plan',
            description='Advanced protection for businesses',
            monthly_price=399.99,
            monthly_credits=100,
            max_investigations_per_day=33,
            max_investigations_per_month=100,
            allowed_models=allowed_models,
            priority_processing=True,
            api_access=True,
            credit_rollover_enabled=True,
            max_rollover_credits=50
        )
        db.session.add(plan)
        db.session.commit()
        
        assert plan.max_investigations_per_day == 33
        assert plan.max_investigations_per_month == 100
        assert plan.allowed_models == allowed_models
        assert plan.priority_processing is True
        assert plan.api_access is True
        assert plan.credit_rollover_enabled is True
        assert plan.max_rollover_credits == 50
    
    def test_subscription_plan_to_dict(self, db):
        """Test subscription plan to_dict conversion"""
        plan = SubscriptionPlan(
            tier=SubscriptionTier.ENTERPRISE,
            name='Enterprise Plan',
            description='Custom enterprise solutions',
            monthly_price=999.99,
            annual_price=9999.99,
            monthly_credits=500,
            allowed_models=['all'],
            priority_processing=True,
            api_access=True
        )
        db.session.add(plan)
        db.session.commit()
        
        plan_dict = plan.to_dict()
        
        assert plan_dict['id'] == plan.id
        assert plan_dict['tier'] == 'enterprise'
        assert plan_dict['name'] == 'Enterprise Plan'
        assert plan_dict['monthly_price'] == 999.99
        assert plan_dict['annual_price'] == 9999.99
        assert plan_dict['monthly_credits'] == 500
        assert plan_dict['allowed_models'] == ['all']
        assert plan_dict['priority_processing'] is True
        assert plan_dict['api_access'] is True
    
    def test_subscription_plan_repr(self, db):
        """Test subscription plan string representation"""
        plan = SubscriptionPlan(
            tier=SubscriptionTier.FREE,
            name='Free Plan',
            monthly_price=0.0,
            monthly_credits=3
        )
        db.session.add(plan)
        db.session.commit()
        
        expected_repr = '<SubscriptionPlan free: Free Plan>'
        assert repr(plan) == expected_repr


@pytest.mark.unit
class TestSubscriptionModel:
    """Test cases for Subscription model"""
    
    def test_subscription_creation(self, db, user, subscription_plan):
        """Test basic subscription creation"""
        subscription = Subscription(
            user_id=user.id,
            plan_id=subscription_plan.id,
            tier=SubscriptionTier.BASIC,
            monthly_credits=10,
            current_credits=10,
            amount=19.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        assert subscription.id is not None
        assert subscription.user_id == user.id
        assert subscription.plan_id == subscription_plan.id
        assert subscription.tier == SubscriptionTier.BASIC
        assert subscription.status == SubscriptionStatus.ACTIVE
        assert subscription.monthly_credits == 10
        assert subscription.current_credits == 10
        assert subscription.rollover_credits == 0
        assert subscription.bonus_credits == 0
        assert subscription.billing_cycle == 'monthly'
        assert subscription.amount == 19.99
    
    def test_subscription_total_credits_property(self, db, user, subscription_plan):
        """Test total credits property calculation"""
        subscription = Subscription(
            user_id=user.id,
            plan_id=subscription_plan.id,
            tier=SubscriptionTier.BASIC,
            monthly_credits=10,
            current_credits=5,
            rollover_credits=3,
            bonus_credits=2,
            amount=19.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        assert subscription.total_credits == 10  # 5 + 3 + 2
    
    def test_subscription_consume_credits(self, db, user, subscription_plan):
        """Test credit consumption logic"""
        subscription = Subscription(
            user_id=user.id,
            plan_id=subscription_plan.id,
            tier=SubscriptionTier.BASIC,
            monthly_credits=10,
            current_credits=5,
            rollover_credits=3,
            bonus_credits=2,
            amount=19.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        # Test successful consumption
        result = subscription.consume_credits(4)
        assert result is True
        assert subscription.bonus_credits == 0  # Consumed first
        assert subscription.rollover_credits == 1  # 3 - 2 (remaining after bonus)
        assert subscription.current_credits == 5  # Untouched
        
        # Test insufficient credits
        result = subscription.consume_credits(10)
        assert result is False
        assert subscription.bonus_credits == 0
        assert subscription.rollover_credits == 1
        assert subscription.current_credits == 5  # Should be unchanged
        
        # Test exact consumption
        result = subscription.consume_credits(6)  # 1 rollover + 5 current
        assert result is True
        assert subscription.bonus_credits == 0
        assert subscription.rollover_credits == 0
        assert subscription.current_credits == 0
    
    def test_subscription_add_credits(self, db, user, subscription_plan):
        """Test adding credits to subscription"""
        subscription = Subscription(
            user_id=user.id,
            plan_id=subscription_plan.id,
            tier=SubscriptionTier.BASIC,
            monthly_credits=10,
            current_credits=5,
            amount=19.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        # Test adding current credits (default)
        subscription.add_credits(3)
        assert subscription.current_credits == 8
        assert subscription.rollover_credits == 0
        assert subscription.bonus_credits == 0
        
        # Test adding bonus credits
        subscription.add_credits(2, 'bonus')
        assert subscription.current_credits == 8
        assert subscription.rollover_credits == 0
        assert subscription.bonus_credits == 2
        
        # Test adding rollover credits
        subscription.add_credits(5, 'rollover')
        assert subscription.current_credits == 8
        assert subscription.rollover_credits == 5
        assert subscription.bonus_credits == 2
    
    def test_subscription_reset_monthly_credits(self, db, user):
        """Test monthly credit reset with rollover"""
        # Create plan with rollover enabled
        plan = SubscriptionPlan(
            tier=SubscriptionTier.PLUS,
            name='Plus Plan',
            monthly_price=89.99,
            monthly_credits=25,
            credit_rollover_enabled=True,
            max_rollover_credits=15
        )
        db.session.add(plan)
        db.session.commit()
        
        subscription = Subscription(
            user_id=user.id,
            plan_id=plan.id,
            tier=SubscriptionTier.PLUS,
            monthly_credits=25,
            current_credits=18,  # Has remaining credits
            rollover_credits=5,
            billing_cycle='monthly',
            amount=89.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        subscription.reset_monthly_credits()
        
        assert subscription.current_credits == 25  # Reset to monthly allowance
        assert subscription.rollover_credits == 20  # 5 + min(18, 15)
        assert subscription.next_billing_date is not None
    
    def test_subscription_reset_monthly_credits_no_rollover(self, db, user, subscription_plan):
        """Test monthly credit reset without rollover"""
        subscription = Subscription(
            user_id=user.id,
            plan_id=subscription_plan.id,
            tier=SubscriptionTier.BASIC,
            monthly_credits=10,
            current_credits=7,  # Has remaining credits
            amount=19.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        subscription.reset_monthly_credits()
        
        assert subscription.current_credits == 10  # Reset to monthly allowance
        assert subscription.rollover_credits == 0  # No rollover for basic plan
    
    def test_subscription_to_dict(self, db, user, subscription_plan):
        """Test subscription to_dict conversion"""
        subscription = Subscription(
            user_id=user.id,
            plan_id=subscription_plan.id,
            tier=SubscriptionTier.BASIC,
            monthly_credits=10,
            current_credits=8,
            rollover_credits=2,
            bonus_credits=1,
            billing_cycle='annual',
            amount=199.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        subscription_dict = subscription.to_dict()
        
        assert subscription_dict['id'] == subscription.id
        assert subscription_dict['user_id'] == user.id
        assert subscription_dict['plan_id'] == subscription_plan.id
        assert subscription_dict['tier'] == 'basic'
        assert subscription_dict['status'] == 'active'
        assert subscription_dict['monthly_credits'] == 10
        assert subscription_dict['current_credits'] == 8
        assert subscription_dict['rollover_credits'] == 2
        assert subscription_dict['bonus_credits'] == 1
        assert subscription_dict['total_credits'] == 11  # 8 + 2 + 1
        assert subscription_dict['billing_cycle'] == 'annual'
        assert subscription_dict['amount'] == 199.99


@pytest.mark.unit
class TestCreditTransactionModel:
    """Test cases for CreditTransaction model"""
    
    def test_credit_transaction_creation(self, db, user, subscription, investigation):
        """Test basic credit transaction creation"""
        transaction = CreditTransaction(
            user_id=user.id,
            subscription_id=subscription.id,
            investigation_id=investigation.id,
            transaction_type=CreditTransactionType.CONSUMPTION,
            amount=-5,
            description='Investigation processing',
            complexity=InvestigationComplexity.MODERATE,
            priority=ProcessingPriority.NORMAL,
            model_used='gpt-4',
            processing_time=12.5,
            balance_before=10,
            balance_after=5
        )
        db.session.add(transaction)
        db.session.commit()
        
        assert transaction.id is not None
        assert transaction.user_id == user.id
        assert transaction.subscription_id == subscription.id
        assert transaction.investigation_id == investigation.id
        assert transaction.transaction_type == CreditTransactionType.CONSUMPTION
        assert transaction.amount == -5
        assert transaction.description == 'Investigation processing'
        assert transaction.complexity == InvestigationComplexity.MODERATE
        assert transaction.priority == ProcessingPriority.NORMAL
        assert transaction.model_used == 'gpt-4'
        assert transaction.processing_time == 12.5
        assert transaction.balance_before == 10
        assert transaction.balance_after == 5
    
    def test_credit_transaction_purchase(self, db, user, subscription):
        """Test credit purchase transaction"""
        transaction = CreditTransaction(
            user_id=user.id,
            subscription_id=subscription.id,
            transaction_type=CreditTransactionType.PURCHASE,
            amount=50,
            description='Additional credit purchase',
            balance_before=5,
            balance_after=55
        )
        db.session.add(transaction)
        db.session.commit()
        
        assert transaction.transaction_type == CreditTransactionType.PURCHASE
        assert transaction.amount == 50
        assert transaction.investigation_id is None  # No investigation for purchase
        assert transaction.complexity is None
        assert transaction.priority is None
    
    def test_credit_transaction_to_dict(self, db, user, subscription, investigation):
        """Test credit transaction to_dict conversion"""
        transaction = CreditTransaction(
            user_id=user.id,
            subscription_id=subscription.id,
            investigation_id=investigation.id,
            transaction_type=CreditTransactionType.CONSUMPTION,
            amount=-7,
            description='Complex analysis',
            complexity=InvestigationComplexity.COMPLEX,
            priority=ProcessingPriority.HIGH,
            model_used='claude-3',
            processing_time=25.3,
            balance_before=20,
            balance_after=13
        )
        db.session.add(transaction)
        db.session.commit()
        
        transaction_dict = transaction.to_dict()
        
        assert transaction_dict['id'] == transaction.id
        assert transaction_dict['user_id'] == user.id
        assert transaction_dict['subscription_id'] == subscription.id
        assert transaction_dict['investigation_id'] == investigation.id
        assert transaction_dict['transaction_type'] == 'consumption'
        assert transaction_dict['amount'] == -7
        assert transaction_dict['description'] == 'Complex analysis'
        assert transaction_dict['complexity'] == 'complex'
        assert transaction_dict['priority'] == 'high'
        assert transaction_dict['model_used'] == 'claude-3'
        assert transaction_dict['processing_time'] == 25.3
        assert transaction_dict['balance_before'] == 20
        assert transaction_dict['balance_after'] == 13


@pytest.mark.unit
class TestCreditConsumptionRuleModel:
    """Test cases for CreditConsumptionRule model"""
    
    def test_credit_consumption_rule_creation(self, db):
        """Test basic credit consumption rule creation"""
        rule = CreditConsumptionRule(
            operation_type='deep_analysis',
            complexity=InvestigationComplexity.COMPLEX,
            priority=ProcessingPriority.NORMAL,
            tier=SubscriptionTier.PRO,
            base_credits=10,
            per_artifact_credits=2,
            model_multiplier=1.5,
            priority_multiplier=1.0
        )
        db.session.add(rule)
        db.session.commit()
        
        assert rule.id is not None
        assert rule.operation_type == 'deep_analysis'
        assert rule.complexity == InvestigationComplexity.COMPLEX
        assert rule.priority == ProcessingPriority.NORMAL
        assert rule.tier == SubscriptionTier.PRO
        assert rule.base_credits == 10
        assert rule.per_artifact_credits == 2
        assert rule.model_multiplier == 1.5
        assert rule.priority_multiplier == 1.0
    
    def test_credit_consumption_rule_calculate_credits(self, db):
        """Test credit calculation logic"""
        rule = CreditConsumptionRule(
            operation_type='comprehensive',
            complexity=InvestigationComplexity.ELITE,
            priority=ProcessingPriority.HIGH,
            tier=SubscriptionTier.ENTERPRISE,
            base_credits=20,
            per_artifact_credits=5,
            model_multiplier=2.0,
            priority_multiplier=1.5
        )
        db.session.add(rule)
        db.session.commit()
        
        # Test with 1 artifact
        cost = rule.calculate_credits(artifact_count=1)
        expected = int((20 + 5 * 1) * 2.0 * 1.5 * 1.0)  # base + artifacts * multipliers
        assert cost == expected
        
        # Test with multiple artifacts
        cost = rule.calculate_credits(artifact_count=3, model_tier_multiplier=1.2)
        expected = int((20 + 5 * 3) * 2.0 * 1.5 * 1.2)
        assert cost == expected
        
        # Test minimum cost
        minimal_rule = CreditConsumptionRule(
            operation_type='quick_scan',
            complexity=InvestigationComplexity.SIMPLE,
            priority=ProcessingPriority.LOW,
            tier=SubscriptionTier.FREE,
            base_credits=0,
            per_artifact_credits=0,
            model_multiplier=0.1,
            priority_multiplier=0.1
        )
        cost = minimal_rule.calculate_credits()
        assert cost >= 1  # Should enforce minimum of 1 credit
    
    def test_credit_consumption_rule_to_dict(self, db):
        """Test credit consumption rule to_dict conversion"""
        rule = CreditConsumptionRule(
            operation_type='elite_intelligence',
            complexity=InvestigationComplexity.ELITE,
            priority=ProcessingPriority.URGENT,
            tier=SubscriptionTier.ENTERPRISE,
            base_credits=50,
            per_artifact_credits=10,
            model_multiplier=3.0,
            priority_multiplier=2.0
        )
        db.session.add(rule)
        db.session.commit()
        
        rule_dict = rule.to_dict()
        
        assert rule_dict['id'] == rule.id
        assert rule_dict['operation_type'] == 'elite_intelligence'
        assert rule_dict['complexity'] == 'elite'
        assert rule_dict['priority'] == 'urgent'
        assert rule_dict['tier'] == 'enterprise'
        assert rule_dict['base_credits'] == 50
        assert rule_dict['per_artifact_credits'] == 10
        assert rule_dict['model_multiplier'] == 3.0
        assert rule_dict['priority_multiplier'] == 2.0


@pytest.mark.unit
class TestCreditUsageAnalyticsModel:
    """Test cases for CreditUsageAnalytics model"""
    
    def test_credit_usage_analytics_creation(self, db, user):
        """Test basic credit usage analytics creation"""
        today = date.today()
        analytics = CreditUsageAnalytics(
            period_start=today - timedelta(days=30),
            period_end=today,
            period_type='monthly',
            user_id=user.id,
            subscription_tier=SubscriptionTier.PRO,
            total_credits_consumed=150,
            total_investigations=25,
            avg_credits_per_investigation=6.0,
            quick_scan_count=10,
            deep_analysis_count=12,
            comprehensive_count=3,
            elite_intelligence_count=0,
            model_usage_breakdown={'gpt-4': 15, 'claude-3': 8, 'gemini': 2}
        )
        db.session.add(analytics)
        db.session.commit()
        
        assert analytics.id is not None
        assert analytics.period_start == today - timedelta(days=30)
        assert analytics.period_end == today
        assert analytics.period_type == 'monthly'
        assert analytics.user_id == user.id
        assert analytics.subscription_tier == SubscriptionTier.PRO
        assert analytics.total_credits_consumed == 150
        assert analytics.total_investigations == 25
        assert analytics.avg_credits_per_investigation == 6.0
        assert analytics.quick_scan_count == 10
        assert analytics.deep_analysis_count == 12
        assert analytics.comprehensive_count == 3
        assert analytics.elite_intelligence_count == 0
        assert analytics.model_usage_breakdown == {'gpt-4': 15, 'claude-3': 8, 'gemini': 2}
    
    def test_credit_usage_analytics_to_dict(self, db, user):
        """Test credit usage analytics to_dict conversion"""
        today = date.today()
        analytics = CreditUsageAnalytics(
            period_start=today - timedelta(days=7),
            period_end=today,
            period_type='weekly',
            user_id=user.id,
            subscription_tier=SubscriptionTier.ENTERPRISE,
            total_credits_consumed=500,
            total_investigations=100,
            avg_credits_per_investigation=5.0,
            elite_intelligence_count=25
        )
        db.session.add(analytics)
        db.session.commit()
        
        analytics_dict = analytics.to_dict()
        
        assert analytics_dict['id'] == analytics.id
        assert analytics_dict['period_start'] == (today - timedelta(days=7)).isoformat()
        assert analytics_dict['period_end'] == today.isoformat()
        assert analytics_dict['period_type'] == 'weekly'
        assert analytics_dict['user_id'] == user.id
        assert analytics_dict['subscription_tier'] == 'enterprise'
        assert analytics_dict['total_credits_consumed'] == 500
        assert analytics_dict['total_investigations'] == 100
        assert analytics_dict['avg_credits_per_investigation'] == 5.0
        assert analytics_dict['elite_intelligence_count'] == 25


@pytest.mark.unit
class TestCreditCalculator:
    """Test cases for CreditCalculator utility class"""
    
    def test_calculate_investigation_cost_with_rule(self, db):
        """Test credit calculation using existing consumption rule"""
        # Create a consumption rule
        rule = CreditConsumptionRule(
            operation_type='deep_analysis',
            complexity=InvestigationComplexity.MODERATE,
            priority=ProcessingPriority.NORMAL,
            tier=SubscriptionTier.BASIC,
            base_credits=5,
            per_artifact_credits=1,
            model_multiplier=1.2,
            priority_multiplier=1.0
        )
        db.session.add(rule)
        db.session.commit()
        
        cost = CreditCalculator.calculate_investigation_cost(
            investigation_type='deep_analysis',
            complexity=InvestigationComplexity.MODERATE,
            priority=ProcessingPriority.NORMAL,
            tier=SubscriptionTier.BASIC,
            artifact_count=3,
            model_tier_multiplier=1.5
        )
        
        # Expected: (5 + 1*3) * 1.2 * 1.0 * 1.5 = 8 * 1.8 = 14.4 -> 14
        assert cost == 14
    
    def test_calculate_investigation_cost_fallback(self, db):
        """Test credit calculation using fallback logic when no rule exists"""
        cost = CreditCalculator.calculate_investigation_cost(
            investigation_type='nonexistent_type',
            complexity=InvestigationComplexity.COMPLEX,
            priority=ProcessingPriority.HIGH,
            tier=SubscriptionTier.PRO,
            artifact_count=2,
            model_tier_multiplier=2.0
        )
        
        # Fallback calculation:
        # base_cost = 7 (complex)
        # priority_mult = 1.5 (high)
        # tier_mult = 0.7 (pro)
        # model_mult = 2.0
        # artifact_count = 2
        # total = 7 * 1.5 * 0.7 * 2.0 * 2 = 29.4 -> 29
        assert cost == 29
    
    def test_calculate_investigation_cost_minimum(self, db):
        """Test that credit calculation enforces minimum cost"""
        cost = CreditCalculator.calculate_investigation_cost(
            investigation_type='minimal_scan',
            complexity=InvestigationComplexity.SIMPLE,
            priority=ProcessingPriority.LOW,
            tier=SubscriptionTier.ENTERPRISE,
            artifact_count=1,
            model_tier_multiplier=0.1
        )
        
        # Even with very low multipliers, should be at least 1 credit
        assert cost >= 1


@pytest.mark.integration
class TestCreditSystemIntegration:
    """Integration tests for credit system models"""
    
    def test_full_subscription_lifecycle(self, db, user):
        """Test complete subscription lifecycle with credit management"""
        # Create subscription plan
        plan = SubscriptionPlan(
            tier=SubscriptionTier.PRO,
            name='Pro Plan',
            monthly_price=399.99,
            monthly_credits=100,
            credit_rollover_enabled=True,
            max_rollover_credits=50
        )
        db.session.add(plan)
        db.session.commit()
        
        # Create subscription
        subscription = Subscription(
            user_id=user.id,
            plan_id=plan.id,
            tier=SubscriptionTier.PRO,
            monthly_credits=100,
            current_credits=100,
            amount=399.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        # Create credit consumption rule
        rule = CreditConsumptionRule(
            operation_type='deep_analysis',
            complexity=InvestigationComplexity.MODERATE,
            priority=ProcessingPriority.NORMAL,
            tier=SubscriptionTier.PRO,
            base_credits=5,
            per_artifact_credits=2,
            model_multiplier=1.0,
            priority_multiplier=1.0
        )
        db.session.add(rule)
        db.session.commit()
        
        # Perform multiple investigations and track credit usage
        investigations_performed = 0
        total_credits_consumed = 0
        
        while subscription.total_credits >= 5:  # Minimum cost
            # Calculate cost for investigation
            cost = CreditCalculator.calculate_investigation_cost(
                investigation_type='deep_analysis',
                complexity=InvestigationComplexity.MODERATE,
                priority=ProcessingPriority.NORMAL,
                tier=SubscriptionTier.PRO,
                artifact_count=2
            )
            
            if subscription.total_credits < cost:
                break
            
            # Consume credits
            balance_before = subscription.total_credits
            success = subscription.consume_credits(cost)
            assert success is True
            
            # Record transaction
            transaction = CreditTransaction(
                user_id=user.id,
                subscription_id=subscription.id,
                transaction_type=CreditTransactionType.CONSUMPTION,
                amount=-cost,
                description=f'Investigation {investigations_performed + 1}',
                complexity=InvestigationComplexity.MODERATE,
                priority=ProcessingPriority.NORMAL,
                balance_before=balance_before,
                balance_after=subscription.total_credits
            )
            db.session.add(transaction)
            
            investigations_performed += 1
            total_credits_consumed += cost
        
        db.session.commit()
        
        # Verify final state
        assert investigations_performed > 0
        assert total_credits_consumed > 0
        assert subscription.total_credits < 100  # Should have consumed some credits
        
        # Check transaction history
        transactions = CreditTransaction.query.filter_by(
            user_id=user.id,
            subscription_id=subscription.id
        ).all()
        assert len(transactions) == investigations_performed
        
        # Test monthly reset
        subscription.reset_monthly_credits()
        assert subscription.current_credits == 100  # Reset to monthly allowance
        
        # Test adding bonus credits
        subscription.add_credits(25, 'bonus')
        assert subscription.total_credits == 125  # 100 current + 25 bonus
    
    def test_subscription_relationships(self, db, user, subscription_plan):
        """Test relationships between subscription models"""
        subscription = Subscription(
            user_id=user.id,
            plan_id=subscription_plan.id,
            tier=SubscriptionTier.BASIC,
            monthly_credits=10,
            current_credits=10,
            amount=19.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        # Test user relationship
        assert subscription.user == user
        assert subscription in user.subscriptions
        
        # Test plan relationship
        assert subscription.plan == subscription_plan
        
        # Create transactions and test relationship
        transaction1 = CreditTransaction(
            user_id=user.id,
            subscription_id=subscription.id,
            transaction_type=CreditTransactionType.CONSUMPTION,
            amount=-3,
            balance_before=10,
            balance_after=7
        )
        transaction2 = CreditTransaction(
            user_id=user.id,
            subscription_id=subscription.id,
            transaction_type=CreditTransactionType.BONUS,
            amount=5,
            balance_before=7,
            balance_after=12
        )
        
        db.session.add_all([transaction1, transaction2])
        db.session.commit()
        
        # Test transaction relationships
        assert transaction1.user == user
        assert transaction1.subscription == subscription
        assert transaction2.user == user
        assert transaction2.subscription == subscription
        
        # Test reverse relationships
        assert transaction1 in user.credit_transactions
        assert transaction2 in user.credit_transactions
