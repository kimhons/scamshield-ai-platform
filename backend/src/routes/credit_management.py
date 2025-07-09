"""
ScamShield AI - Credit Management Routes

API endpoints for credit system management and subscription handling
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
import json
import logging

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import func, and_, or_
from sqlalchemy.exc import IntegrityError

from models.user import db, User
from models.credit_system import (
    Subscription, CreditTransaction, CreditConsumptionRule, SubscriptionPlan,
    CreditUsageAnalytics, SubscriptionTier, CreditTransactionType,
    InvestigationComplexity, ProcessingPriority, CreditCalculator,
    DEFAULT_SUBSCRIPTION_PLANS
)

# Configure logging
logger = logging.getLogger(__name__)

# Create blueprint
credit_bp = Blueprint('credit', __name__, url_prefix='/api/credit')

# ============ SUBSCRIPTION MANAGEMENT ============

@credit_bp.route('/subscription/<user_id>')
def get_user_subscription(user_id):
    """Get user's current subscription details"""
    try:
        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        
        if not subscription:
            # Create free tier subscription for new users
            subscription = create_free_subscription(user_id)
        
        # Get subscription plan details
        plan = SubscriptionPlan.query.filter_by(tier=subscription.tier).first()
        
        response = {
            "subscription": {
                "id": subscription.id,
                "user_id": subscription.user_id,
                "tier": subscription.tier,
                "status": subscription.status,
                "monthly_credits": subscription.monthly_credits,
                "current_credits": subscription.current_credits,
                "rollover_credits": subscription.rollover_credits,
                "bonus_credits": subscription.bonus_credits,
                "total_credits": subscription.total_credits,
                "price": subscription.price,
                "billing_cycle": subscription.billing_cycle,
                "next_billing_date": subscription.next_billing_date.isoformat() if subscription.next_billing_date else None,
                "expires_at": subscription.expires_at.isoformat() if subscription.expires_at else None,
                "created_at": subscription.created_at.isoformat(),
                "updated_at": subscription.updated_at.isoformat()
            }
        }
        
        if plan:
            response["plan"] = {
                "name": plan.name,
                "description": plan.description,
                "features": plan.features_list,
                "max_concurrent_investigations": plan.max_concurrent_investigations,
                "api_access": plan.api_access,
                "priority_support": plan.priority_support,
                "custom_branding": plan.custom_branding,
                "max_file_size_mb": plan.max_file_size_mb,
                "max_artifacts_per_investigation": plan.max_artifacts_per_investigation
            }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Failed to get subscription for user {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@credit_bp.route('/subscription/<user_id>/upgrade', methods=['POST'])
def upgrade_subscription(user_id):
    """Upgrade user subscription to a higher tier"""
    try:
        data = request.get_json()
        new_tier = data.get('tier')
        billing_cycle = data.get('billing_cycle', 'monthly')
        
        if not new_tier:
            return jsonify({"error": "Tier is required"}), 400
        
        # Validate tier
        try:
            tier_enum = SubscriptionTier(new_tier)
        except ValueError:
            return jsonify({"error": "Invalid tier specified"}), 400
        
        # Get subscription plan
        plan = SubscriptionPlan.query.filter_by(tier=new_tier, active=True).first()
        if not plan:
            return jsonify({"error": "Subscription plan not found"}), 404
        
        # Get current subscription
        current_subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        
        if current_subscription:
            # Deactivate current subscription
            current_subscription.status = 'upgraded'
            current_subscription.updated_at = datetime.now(timezone.utc)
        
        # Calculate pricing
        price = plan.annual_price if billing_cycle == 'annual' else plan.monthly_price
        
        # Create new subscription
        new_subscription = Subscription(
            user_id=user_id,
            tier=new_tier,
            status='active',
            monthly_credits=plan.monthly_credits,
            current_credits=plan.monthly_credits,
            rollover_credits=0,
            bonus_credits=0,
            price=price,
            billing_cycle=billing_cycle,
            next_billing_date=calculate_next_billing_date(billing_cycle),
            expires_at=calculate_expiry_date(billing_cycle)
        )
        
        db.session.add(new_subscription)
        
        # Create purchase transaction
        transaction = CreditTransaction(
            subscription_id=new_subscription.id,
            user_id=user_id,
            transaction_type=CreditTransactionType.PURCHASE.value,
            amount=plan.monthly_credits,
            description=f"Subscription upgrade to {plan.name}",
            balance_after=new_subscription.total_credits
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        logger.info(f"User {user_id} upgraded to {new_tier} tier")
        
        return jsonify({
            "message": "Subscription upgraded successfully",
            "subscription": {
                "tier": new_subscription.tier,
                "credits": new_subscription.total_credits,
                "price": new_subscription.price,
                "billing_cycle": new_subscription.billing_cycle
            }
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to upgrade subscription for user {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@credit_bp.route('/subscription/<user_id>/cancel', methods=['POST'])
def cancel_subscription(user_id):
    """Cancel user subscription"""
    try:
        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        
        if not subscription:
            return jsonify({"error": "No active subscription found"}), 404
        
        # Don't cancel free tier
        if subscription.tier == SubscriptionTier.FREE.value:
            return jsonify({"error": "Cannot cancel free tier subscription"}), 400
        
        # Mark as cancelled but keep active until expiry
        subscription.status = 'cancelled'
        subscription.updated_at = datetime.now(timezone.utc)
        
        # Create cancellation transaction
        transaction = CreditTransaction(
            subscription_id=subscription.id,
            user_id=user_id,
            transaction_type=CreditTransactionType.REFUND.value,
            amount=0,
            description="Subscription cancelled",
            balance_after=subscription.total_credits
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        logger.info(f"User {user_id} cancelled subscription")
        
        return jsonify({
            "message": "Subscription cancelled successfully",
            "expires_at": subscription.expires_at.isoformat() if subscription.expires_at else None
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to cancel subscription for user {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ CREDIT MANAGEMENT ============

@credit_bp.route('/balance/<user_id>')
def get_credit_balance(user_id):
    """Get user's current credit balance"""
    try:
        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        
        if not subscription:
            subscription = create_free_subscription(user_id)
        
        return jsonify({
            "user_id": user_id,
            "total_credits": subscription.total_credits,
            "current_credits": subscription.current_credits,
            "rollover_credits": subscription.rollover_credits,
            "bonus_credits": subscription.bonus_credits,
            "tier": subscription.tier,
            "last_updated": subscription.updated_at.isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get credit balance for user {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@credit_bp.route('/estimate', methods=['POST'])
def estimate_credit_cost():
    """Estimate credit cost for an investigation"""
    try:
        data = request.get_json()
        
        # Required parameters
        operation_type = data.get('operation_type', 'comprehensive_investigation')
        artifact_count = data.get('artifact_count', 1)
        user_id = data.get('user_id')
        priority = data.get('priority', 'standard')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        # Get user subscription
        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        if not subscription:
            subscription = create_free_subscription(user_id)
        
        # Determine complexity and AI tier based on subscription
        subscription_tier = SubscriptionTier(subscription.tier)
        complexity = CreditCalculator.get_complexity_from_tier(subscription_tier)
        ai_model_tier = CreditCalculator.get_tier_ai_models(subscription_tier)
        
        # Parse priority
        try:
            priority_enum = ProcessingPriority(priority)
        except ValueError:
            priority_enum = ProcessingPriority.STANDARD
        
        # Calculate cost
        estimated_cost = CreditCalculator.calculate_investigation_cost(
            operation_type=operation_type,
            complexity=complexity,
            ai_model_tier=ai_model_tier,
            artifact_count=artifact_count,
            priority=priority_enum
        )
        
        # Check if user can afford
        can_afford = subscription.can_afford(estimated_cost)
        
        return jsonify({
            "estimated_cost": estimated_cost,
            "operation_type": operation_type,
            "complexity": complexity.value,
            "ai_model_tier": ai_model_tier,
            "artifact_count": artifact_count,
            "priority": priority_enum.value,
            "user_balance": subscription.total_credits,
            "can_afford": can_afford,
            "breakdown": {
                "base_cost": CreditCalculator.OPERATION_COSTS.get(operation_type, {}).get(complexity, {}).get(ai_model_tier, 50),
                "artifact_multiplier": artifact_count,
                "priority_multiplier": 1.0 if priority_enum == ProcessingPriority.STANDARD else 1.5 if priority_enum == ProcessingPriority.PRIORITY else 2.0
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to estimate credit cost: {str(e)}")
        return jsonify({"error": str(e)}), 500

@credit_bp.route('/consume', methods=['POST'])
def consume_credits():
    """Consume credits for an investigation"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        investigation_id = data.get('investigation_id')
        credit_amount = data.get('credit_amount')
        description = data.get('description', 'Investigation credit consumption')
        
        if not all([user_id, investigation_id, credit_amount]):
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Get user subscription
        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        if not subscription:
            return jsonify({"error": "No active subscription found"}), 404
        
        # Check if user can afford
        if not subscription.can_afford(credit_amount):
            return jsonify({
                "error": "Insufficient credits",
                "required": credit_amount,
                "available": subscription.total_credits
            }), 400
        
        # Consume credits
        success = subscription.consume_credits(credit_amount, description)
        
        if not success:
            return jsonify({"error": "Failed to consume credits"}), 500
        
        # Update transaction with investigation ID
        latest_transaction = CreditTransaction.query.filter_by(
            subscription_id=subscription.id,
            transaction_type=CreditTransactionType.CONSUMPTION.value
        ).order_by(CreditTransaction.created_at.desc()).first()
        
        if latest_transaction:
            latest_transaction.investigation_id = investigation_id
        
        db.session.commit()
        
        logger.info(f"Consumed {credit_amount} credits for user {user_id}, investigation {investigation_id}")
        
        return jsonify({
            "message": "Credits consumed successfully",
            "consumed": credit_amount,
            "remaining_balance": subscription.total_credits,
            "investigation_id": investigation_id
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to consume credits: {str(e)}")
        return jsonify({"error": str(e)}), 500

@credit_bp.route('/add', methods=['POST'])
def add_credits():
    """Add credits to user account (admin function)"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        credit_amount = data.get('credit_amount')
        transaction_type = data.get('transaction_type', 'bonus')
        description = data.get('description', 'Admin credit addition')
        
        if not all([user_id, credit_amount]):
            return jsonify({"error": "Missing required parameters"}), 400
        
        # Validate transaction type
        try:
            trans_type = CreditTransactionType(transaction_type)
        except ValueError:
            return jsonify({"error": "Invalid transaction type"}), 400
        
        # Get user subscription
        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        if not subscription:
            subscription = create_free_subscription(user_id)
        
        # Add credits
        subscription.add_credits(credit_amount, trans_type, description)
        db.session.commit()
        
        logger.info(f"Added {credit_amount} credits to user {user_id} ({transaction_type})")
        
        return jsonify({
            "message": "Credits added successfully",
            "added": credit_amount,
            "new_balance": subscription.total_credits,
            "transaction_type": transaction_type
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to add credits: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ TRANSACTION HISTORY ============

@credit_bp.route('/transactions/<user_id>')
def get_transaction_history(user_id):
    """Get user's credit transaction history"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        transaction_type = request.args.get('type')
        
        query = CreditTransaction.query.filter_by(user_id=user_id)
        
        if transaction_type:
            query = query.filter_by(transaction_type=transaction_type)
        
        transactions = query.order_by(CreditTransaction.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            "transactions": [{
                "id": trans.id,
                "transaction_type": trans.transaction_type,
                "amount": trans.amount,
                "balance_after": trans.balance_after,
                "description": trans.description,
                "investigation_id": trans.investigation_id,
                "metadata": trans.metadata_dict,
                "created_at": trans.created_at.isoformat()
            } for trans in transactions.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": transactions.total,
                "pages": transactions.pages,
                "has_next": transactions.has_next,
                "has_prev": transactions.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get transaction history for user {user_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ SUBSCRIPTION PLANS ============

@credit_bp.route('/plans')
def get_subscription_plans():
    """Get all available subscription plans"""
    try:
        plans = SubscriptionPlan.query.filter_by(active=True).order_by(SubscriptionPlan.monthly_price).all()
        
        return jsonify({
            "plans": [{
                "tier": plan.tier,
                "name": plan.name,
                "description": plan.description,
                "monthly_price": plan.monthly_price,
                "annual_price": plan.annual_price,
                "monthly_credits": plan.monthly_credits,
                "rollover_percentage": plan.rollover_percentage,
                "features": plan.features_list,
                "max_concurrent_investigations": plan.max_concurrent_investigations,
                "api_access": plan.api_access,
                "priority_support": plan.priority_support,
                "custom_branding": plan.custom_branding,
                "max_file_size_mb": plan.max_file_size_mb,
                "max_artifacts_per_investigation": plan.max_artifacts_per_investigation
            } for plan in plans]
        })
        
    except Exception as e:
        logger.error(f"Failed to get subscription plans: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ ANALYTICS ============

@credit_bp.route('/analytics/usage')
def get_usage_analytics():
    """Get credit usage analytics"""
    try:
        days = request.args.get('days', 7, type=int)
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # Daily usage summary
        daily_usage = db.session.query(
            func.date(CreditTransaction.created_at).label('date'),
            func.sum(func.abs(CreditTransaction.amount)).label('total_credits'),
            func.count(CreditTransaction.id).label('total_transactions')
        ).filter(
            and_(
                CreditTransaction.created_at >= start_date,
                CreditTransaction.transaction_type == CreditTransactionType.CONSUMPTION.value
            )
        ).group_by(func.date(CreditTransaction.created_at)).all()
        
        # Tier distribution
        tier_usage = db.session.query(
            Subscription.tier,
            func.count(Subscription.id).label('user_count'),
            func.sum(Subscription.current_credits + Subscription.rollover_credits + Subscription.bonus_credits).label('total_credits')
        ).filter_by(status='active').group_by(Subscription.tier).all()
        
        return jsonify({
            "daily_usage": [{
                "date": usage.date.isoformat(),
                "total_credits": int(usage.total_credits or 0),
                "total_transactions": int(usage.total_transactions or 0)
            } for usage in daily_usage],
            "tier_distribution": [{
                "tier": tier.tier,
                "user_count": int(tier.user_count),
                "total_credits": int(tier.total_credits or 0)
            } for tier in tier_usage],
            "period": {
                "start_date": start_date.isoformat(),
                "end_date": datetime.now(timezone.utc).isoformat(),
                "days": days
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get usage analytics: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ UTILITY FUNCTIONS ============

def create_free_subscription(user_id: str) -> Subscription:
    """Create a free tier subscription for new users"""
    try:
        # Get free tier plan
        free_plan = SubscriptionPlan.query.filter_by(tier=SubscriptionTier.FREE.value).first()
        if not free_plan:
            # Create default free plan if it doesn't exist
            initialize_default_plans()
            free_plan = SubscriptionPlan.query.filter_by(tier=SubscriptionTier.FREE.value).first()
        
        # Create subscription
        subscription = Subscription(
            user_id=user_id,
            tier=SubscriptionTier.FREE.value,
            status='active',
            monthly_credits=free_plan.monthly_credits,
            current_credits=free_plan.monthly_credits,
            rollover_credits=0,
            bonus_credits=0,
            price=0.0,
            billing_cycle='monthly'
        )
        
        db.session.add(subscription)
        
        # Create initial transaction
        transaction = CreditTransaction(
            subscription_id=subscription.id,
            user_id=user_id,
            transaction_type=CreditTransactionType.PURCHASE.value,
            amount=free_plan.monthly_credits,
            description="Free tier subscription created",
            balance_after=subscription.total_credits
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        logger.info(f"Created free subscription for user {user_id}")
        return subscription
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to create free subscription for user {user_id}: {str(e)}")
        raise

def calculate_next_billing_date(billing_cycle: str) -> datetime:
    """Calculate next billing date based on cycle"""
    now = datetime.now(timezone.utc)
    if billing_cycle == 'annual':
        return now + timedelta(days=365)
    else:  # monthly
        return now + timedelta(days=30)

def calculate_expiry_date(billing_cycle: str) -> datetime:
    """Calculate subscription expiry date"""
    return calculate_next_billing_date(billing_cycle)

def initialize_default_plans():
    """Initialize default subscription plans"""
    try:
        for plan_data in DEFAULT_SUBSCRIPTION_PLANS:
            existing_plan = SubscriptionPlan.query.filter_by(tier=plan_data['tier']).first()
            if not existing_plan:
                plan = SubscriptionPlan(
                    tier=plan_data['tier'],
                    name=plan_data['name'],
                    description=plan_data['description'],
                    monthly_price=plan_data['monthly_price'],
                    annual_price=plan_data['annual_price'],
                    monthly_credits=plan_data['monthly_credits'],
                    rollover_percentage=plan_data['rollover_percentage'],
                    max_rollover_months=plan_data['max_rollover_months'],
                    features=json.dumps(plan_data['features']),
                    max_concurrent_investigations=plan_data['max_concurrent_investigations'],
                    api_access=plan_data['api_access'],
                    priority_support=plan_data['priority_support'],
                    custom_branding=plan_data['custom_branding'],
                    max_file_size_mb=plan_data['max_file_size_mb'],
                    max_artifacts_per_investigation=plan_data['max_artifacts_per_investigation']
                )
                db.session.add(plan)
        
        db.session.commit()
        logger.info("Default subscription plans initialized")
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to initialize default plans: {str(e)}")
        raise

# ============ ADMIN FUNCTIONS ============

@credit_bp.route('/admin/rollover', methods=['POST'])
def process_monthly_rollover():
    """Process monthly credit rollover for all subscriptions (admin function)"""
    try:
        processed_count = 0
        
        # Get all active subscriptions
        subscriptions = Subscription.query.filter_by(status='active').all()
        
        for subscription in subscriptions:
            # Skip free tier (no rollover)
            if subscription.tier == SubscriptionTier.FREE.value:
                continue
            
            # Get plan details
            plan = SubscriptionPlan.query.filter_by(tier=subscription.tier).first()
            if not plan or plan.rollover_percentage == 0:
                continue
            
            # Calculate rollover amount
            rollover_amount = int(subscription.current_credits * plan.rollover_percentage)
            
            if rollover_amount > 0:
                # Add to rollover credits
                subscription.rollover_credits += rollover_amount
                
                # Reset current credits to monthly allocation
                subscription.current_credits = subscription.monthly_credits
                
                # Create rollover transaction
                transaction = CreditTransaction(
                    subscription_id=subscription.id,
                    user_id=subscription.user_id,
                    transaction_type=CreditTransactionType.ROLLOVER.value,
                    amount=rollover_amount,
                    description=f"Monthly rollover ({plan.rollover_percentage*100}%)",
                    balance_after=subscription.total_credits
                )
                
                db.session.add(transaction)
                processed_count += 1
        
        db.session.commit()
        
        logger.info(f"Processed monthly rollover for {processed_count} subscriptions")
        
        return jsonify({
            "message": "Monthly rollover processed successfully",
            "processed_subscriptions": processed_count
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Failed to process monthly rollover: {str(e)}")
        return jsonify({"error": str(e)}), 500

@credit_bp.route('/admin/initialize', methods=['POST'])
def initialize_credit_system():
    """Initialize credit system with default plans (admin function)"""
    try:
        initialize_default_plans()
        
        return jsonify({
            "message": "Credit system initialized successfully"
        })
        
    except Exception as e:
        logger.error(f"Failed to initialize credit system: {str(e)}")
        return jsonify({"error": str(e)}), 500

