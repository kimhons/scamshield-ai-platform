"""
ScamShield AI - User Model Tests

Comprehensive tests for the User model including authentication, security, and data integrity.
"""

import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import patch

from models.user import User
from models.credit_system import Subscription, SubscriptionTier


@pytest.mark.unit
class TestUserModel:
    """Test cases for User model"""
    
    def test_user_creation(self, db):
        """Test basic user creation"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='securepassword123'
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.password_hash is not None
        assert user.password_hash != 'securepassword123'  # Password should be hashed
        assert user.is_active is True
        assert user.is_verified is False
        assert user.is_admin is False
        assert user.failed_login_attempts == 0
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_user_creation_with_optional_fields(self, db):
        """Test user creation with optional fields"""
        user = User(
            username='testuser2',
            email='test2@example.com',
            password='securepassword123',
            first_name='John',
            last_name='Doe',
            company='Test Company',
            phone='+1234567890'
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'
        assert user.company == 'Test Company'
        assert user.phone == '+1234567890'
    
    def test_password_hashing(self, db):
        """Test password hashing functionality"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('mypassword123')
        
        assert user.password_hash is not None
        assert user.password_hash != 'mypassword123'
        assert user.check_password('mypassword123') is True
        assert user.check_password('wrongpassword') is False
    
    def test_password_validation(self, db):
        """Test password validation edge cases"""
        user = User(username='testuser', email='test@example.com')
        
        # Test empty password
        with pytest.raises(ValueError):
            user.set_password('')
        
        with pytest.raises(ValueError):
            user.set_password(None)
        
        # Test password checking without setting password
        assert user.check_password('anypassword') is False
    
    def test_email_case_normalization(self, db):
        """Test that emails are normalized to lowercase"""
        user = User(
            username='testuser',
            email='Test@EXAMPLE.COM',
            password='password123'
        )
        db.session.add(user)
        db.session.commit()
        
        assert user.email == 'test@example.com'
    
    def test_unique_constraints(self, db):
        """Test unique constraints on username and email"""
        # Create first user
        user1 = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        db.session.add(user1)
        db.session.commit()
        
        # Try to create user with same username
        user2 = User(
            username='testuser',
            email='different@example.com',
            password='password123'
        )
        db.session.add(user2)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db.session.commit()
        
        db.session.rollback()
        
        # Try to create user with same email
        user3 = User(
            username='differentuser',
            email='test@example.com',
            password='password123'
        )
        db.session.add(user3)
        
        with pytest.raises(Exception):  # Should raise IntegrityError
            db.session.commit()
    
    def test_last_login_update(self, db):
        """Test last login functionality"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        user.failed_login_attempts = 3
        user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        assert user.last_login_at is None
        
        user.update_last_login()
        
        assert user.last_login_at is not None
        assert user.failed_login_attempts == 0
        assert user.locked_until is None
    
    def test_failed_login_attempts(self, db):
        """Test failed login attempt tracking"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        assert user.failed_login_attempts == 0
        assert user.is_account_locked() is False
        
        # Increment failed attempts
        for i in range(4):
            user.increment_failed_login()
            assert user.failed_login_attempts == i + 1
            assert user.is_account_locked() is False
        
        # 5th failed attempt should lock account
        user.increment_failed_login()
        assert user.failed_login_attempts == 5
        assert user.is_account_locked() is True
        assert user.locked_until is not None
    
    def test_account_lock_expiration(self, db):
        """Test account lock expiration"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        # Set lock to past time (expired)
        user.locked_until = datetime.now(timezone.utc) - timedelta(minutes=1)
        assert user.is_account_locked() is False
        
        # Set lock to future time (active)
        user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=30)
        assert user.is_account_locked() is True
    
    def test_to_dict_basic(self, db):
        """Test basic to_dict functionality"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        db.session.add(user)
        db.session.commit()
        
        user_dict = user.to_dict()
        
        assert user_dict['id'] == user.id
        assert user_dict['username'] == 'testuser'
        assert user_dict['email'] == 'test@example.com'
        assert user_dict['first_name'] == 'John'
        assert user_dict['last_name'] == 'Doe'
        assert user_dict['is_active'] is True
        assert user_dict['is_verified'] is False
        assert user_dict['is_admin'] is False
        assert 'password_hash' not in user_dict  # Should not include sensitive data
        assert 'failed_login_attempts' not in user_dict
    
    def test_to_dict_with_sensitive_data(self, db):
        """Test to_dict with sensitive data included"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        user.failed_login_attempts = 3
        user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=30)
        db.session.add(user)
        db.session.commit()
        
        user_dict = user.to_dict(include_sensitive=True)
        
        assert user_dict['failed_login_attempts'] == 3
        assert user_dict['locked_until'] is not None
        assert user_dict['is_account_locked'] is True
        assert 'password_hash' not in user_dict  # Still should not include password
    
    def test_user_repr(self, db):
        """Test user string representation"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        
        assert repr(user) == '<User testuser>'
    
    def test_user_relationships(self, db, subscription_plan):
        """Test user model relationships"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        db.session.add(user)
        db.session.commit()
        
        # Test subscription relationship
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
        
        assert len(user.subscriptions) == 1
        assert user.subscriptions[0] == subscription
        assert user.subscriptions[0].user == user


@pytest.mark.security
class TestUserSecurity:
    """Security-focused tests for User model"""
    
    def test_password_complexity_requirements(self, db):
        """Test that passwords meet security requirements"""
        # This would be enhanced based on actual password policy
        user = User(username='testuser', email='test@example.com')
        
        # Test various password scenarios
        passwords_to_test = [
            ('simple', False),  # Too simple
            ('password123', True),  # Acceptable for testing
            ('VerySecurePassword123!', True),  # Strong password
        ]
        
        for password, should_work in passwords_to_test:
            try:
                user.set_password(password)
                assert should_work, f"Password '{password}' should not be accepted"
            except ValueError:
                assert not should_work, f"Password '{password}' should be accepted"
    
    def test_timing_attack_resistance(self, db):
        """Test that password checking is resistant to timing attacks"""
        user = User(
            username='testuser',
            email='test@example.com',
            password='correctpassword123'
        )
        
        # Both correct and incorrect passwords should take similar time
        import time
        
        # Test with correct password
        start_time = time.time()
        result1 = user.check_password('correctpassword123')
        time1 = time.time() - start_time
        
        # Test with incorrect password
        start_time = time.time()
        result2 = user.check_password('wrongpassword123')
        time2 = time.time() - start_time
        
        assert result1 is True
        assert result2 is False
        # Time difference should be minimal (within reasonable bounds)
        assert abs(time1 - time2) < 0.1  # 100ms tolerance
    
    def test_sql_injection_resistance(self, db):
        """Test that user inputs are resistant to SQL injection"""
        # Test with potential SQL injection strings
        malicious_inputs = [
            "'; DROP TABLE users; --",
            "admin' OR '1'='1",
            "' UNION SELECT * FROM users --",
        ]
        
        for malicious_input in malicious_inputs:
            user = User(
                username=malicious_input,
                email=f"{malicious_input}@example.com",
                password='password123'
            )
            
            # Should be able to save safely
            db.session.add(user)
            db.session.commit()
            
            # Username should be stored as-is (not executed)
            saved_user = User.query.filter_by(username=malicious_input).first()
            assert saved_user is not None
            assert saved_user.username == malicious_input
            
            # Clean up
            db.session.delete(saved_user)
            db.session.commit()
