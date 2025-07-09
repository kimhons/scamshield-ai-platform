"""
ScamShield AI - Test Configuration

Pytest configuration and shared fixtures for testing.
"""

import os
import pytest
import tempfile
from unittest.mock import Mock, patch

from flask import Flask
from models.user import db as user_db
from models.investigation import Investigation, Evidence, Report, ScamDatabase
from models.credit_system import (
    Subscription, CreditTransaction, SubscriptionPlan, 
    CreditConsumptionRule, SubscriptionTier, DEFAULT_SUBSCRIPTION_PLANS
)

@pytest.fixture(scope='session')
def app():
    """Create and configure a test Flask application."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    app = Flask(__name__)
    app.config.update({
        'TESTING': True,
        'SECRET_KEY': 'test-secret-key',
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
    })
    
    # Initialize database
    user_db.init_app(app)
    
    with app.app_context():
        user_db.create_all()
        # Create default subscription plans
        create_default_subscription_plans()
    
    yield app
    
    # Clean up
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()

@pytest.fixture
def db(app):
    """Create a database for the tests."""
    with app.app_context():
        user_db.create_all()
        yield user_db
        user_db.session.remove()
        user_db.drop_all()

@pytest.fixture
def user(db):
    """Create a test user."""
    from models.user import User
    user = User(
        username='testuser',
        email='test@example.com',
        password='testpassword123'
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def subscription_plan(db):
    """Create a test subscription plan."""
    plan = SubscriptionPlan(
        tier=SubscriptionTier.BASIC,
        name='Test Basic Plan',
        description='Test plan for unit tests',
        monthly_price=19.99,
        monthly_credits=10,
        max_investigations_per_day=3,
        max_investigations_per_month=10
    )
    db.session.add(plan)
    db.session.commit()
    return plan

@pytest.fixture
def subscription(db, user, subscription_plan):
    """Create a test subscription."""
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
    return subscription

@pytest.fixture
def investigation(db, user):
    """Create a test investigation."""
    investigation = Investigation(
        user_id=user.id,
        title='Test Investigation',
        description='A test investigation for unit tests',
        investigation_type='quick_scan',
        model_tier='basic'
    )
    db.session.add(investigation)
    db.session.commit()
    return investigation

@pytest.fixture
def mock_ai_models():
    """Mock AI model responses for testing."""
    with patch('src.ai_engine.model_manager_v2.EnhancedModelManager') as mock_manager:
        mock_instance = Mock()
        mock_instance.generate_response.return_value = {
            'content': 'This is a test AI response',
            'confidence': 0.85,
            'model_used': 'test-model',
            'processing_time': 1.5
        }
        mock_manager.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_external_apis():
    """Mock external API calls for testing."""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post:
        
        # Mock successful API responses
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success', 'data': {}}
        mock_response.text = 'Mock response content'
        
        mock_get.return_value = mock_response
        mock_post.return_value = mock_response
        
        yield mock_get, mock_post

def create_default_subscription_plans():
    """Create default subscription plans for testing."""
    for plan_data in DEFAULT_SUBSCRIPTION_PLANS:
        existing_plan = SubscriptionPlan.query.filter_by(tier=plan_data['tier']).first()
        if not existing_plan:
            plan = SubscriptionPlan(**plan_data)
            user_db.session.add(plan)
    user_db.session.commit()

# Custom test markers
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.security = pytest.mark.security
pytest.mark.performance = pytest.mark.performance
