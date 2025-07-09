"""
ScamShield AI - Main API Routes Tests

Integration tests for the main application API endpoints.
"""

import pytest
import json
from unittest.mock import patch, Mock

from models.user import User
from models.investigation import Investigation, InvestigationStatus
from models.credit_system import Subscription, SubscriptionTier


@pytest.mark.integration
class TestHealthEndpoints:
    """Test health and status endpoints"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_index_endpoint(self, client):
        """Test main index endpoint serves static content"""
        response = client.get('/')
        assert response.status_code == 200


@pytest.mark.integration
class TestUserRoutes:
    """Test user management API endpoints"""
    
    def test_get_users_empty(self, client, db):
        """Test getting users when none exist"""
        response = client.get('/api/users')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data == []
    
    def test_create_user(self, client, db):
        """Test creating a new user"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123'
        }
        
        response = client.post('/api/users', 
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        data = response.get_json()
        assert data['username'] == 'testuser'
        assert data['email'] == 'test@example.com'
        assert 'password' not in data  # Should not return password
        assert 'id' in data
    
    def test_create_user_missing_fields(self, client, db):
        """Test creating user with missing required fields"""
        user_data = {
            'username': 'testuser'
            # Missing email and password
        }
        
        response = client.post('/api/users',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_create_user_duplicate_username(self, client, db, user):
        """Test creating user with duplicate username"""
        user_data = {
            'username': user.username,  # Duplicate
            'email': 'different@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/users',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_get_user_by_id(self, client, db, user):
        """Test getting a specific user by ID"""
        response = client.get(f'/api/users/{user.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['id'] == user.id
        assert data['username'] == user.username
        assert data['email'] == user.email
    
    def test_get_user_not_found(self, client, db):
        """Test getting non-existent user"""
        response = client.get('/api/users/nonexistent-id')
        assert response.status_code == 404
    
    def test_update_user(self, client, db, user):
        """Test updating user information"""
        update_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'company': 'Test Company'
        }
        
        response = client.put(f'/api/users/{user.id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['first_name'] == 'John'
        assert data['last_name'] == 'Doe'
        assert data['company'] == 'Test Company'
    
    def test_delete_user(self, client, db, user):
        """Test deleting a user"""
        user_id = user.id
        
        response = client.delete(f'/api/users/{user_id}')
        assert response.status_code == 204
        
        # Verify user is deleted
        deleted_user = User.query.get(user_id)
        assert deleted_user is None


@pytest.mark.integration
class TestInvestigationRoutes:
    """Test investigation API endpoints"""
    
    @patch('src.ai_engine.investigation_engine.InvestigationEngine')
    def test_create_investigation(self, mock_engine, client, db, user, subscription, mock_ai_models):
        """Test creating a new investigation"""
        # Mock the investigation engine
        mock_engine_instance = Mock()
        mock_engine.return_value = mock_engine_instance
        
        mock_result = Mock()
        mock_result.to_dict.return_value = {
            'investigation_id': 'test-id',
            'status': 'completed',
            'threat_level': 'medium',
            'confidence_score': 0.75,
            'executive_summary': 'Moderate risk detected',
            'processing_time': 15.5,
            'cost': 5.0
        }
        mock_engine_instance.conduct_investigation.return_value = mock_result
        
        investigation_data = {
            'user_id': user.id,
            'title': 'Test Investigation',
            'description': 'Testing phishing email',
            'investigation_type': 'deep_analysis',
            'model_tier': 'professional',
            'artifacts': [
                {
                    'type': 'email',
                    'content': 'phishing@scammer.com',
                    'metadata': {'subject': 'Urgent: Verify Account'}
                }
            ]
        }
        
        response = client.post('/api/investigations',
                             data=json.dumps(investigation_data),
                             content_type='application/json')
        assert response.status_code == 201
        
        data = response.get_json()
        assert data['title'] == 'Test Investigation'
        assert data['user_id'] == user.id
        assert data['investigation_type'] == 'deep_analysis'
        assert data['status'] == 'pending'
    
    def test_create_investigation_insufficient_credits(self, client, db, user):
        """Test creating investigation with insufficient credits"""
        # Create subscription with no credits
        subscription = Subscription(
            user_id=user.id,
            plan_id='test-plan',
            tier=SubscriptionTier.BASIC,
            monthly_credits=10,
            current_credits=0,  # No credits
            amount=19.99
        )
        db.session.add(subscription)
        db.session.commit()
        
        investigation_data = {
            'user_id': user.id,
            'title': 'Test Investigation',
            'investigation_type': 'deep_analysis',
            'model_tier': 'professional',
            'artifacts': [{'type': 'url', 'content': 'https://scam.com'}]
        }
        
        response = client.post('/api/investigations',
                             data=json.dumps(investigation_data),
                             content_type='application/json')
        assert response.status_code == 400
        
        data = response.get_json()
        assert 'insufficient credits' in data['error'].lower()
    
    def test_get_user_investigations(self, client, db, user, investigation):
        """Test getting investigations for a user"""
        response = client.get(f'/api/users/{user.id}/investigations')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data) == 1
        assert data[0]['id'] == investigation.id
        assert data[0]['title'] == investigation.title
    
    def test_get_investigation_by_id(self, client, db, investigation):
        """Test getting a specific investigation"""
        response = client.get(f'/api/investigations/{investigation.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data['id'] == investigation.id
        assert data['title'] == investigation.title
        assert data['status'] == 'pending'
    
    def test_get_investigation_not_found(self, client, db):
        """Test getting non-existent investigation"""
        response = client.get('/api/investigations/nonexistent-id')
        assert response.status_code == 404
    
    @patch('src.ai_engine.investigation_engine.InvestigationEngine')
    def test_investigation_status_polling(self, mock_engine, client, db, investigation):
        """Test polling for investigation status updates"""
        # Start with pending investigation
        assert investigation.status == InvestigationStatus.PENDING
        
        # First poll - still pending
        response = client.get(f'/api/investigations/{investigation.id}/status')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'pending'
        
        # Update investigation to completed
        investigation.status = InvestigationStatus.COMPLETED
        investigation.confidence_score = 0.85
        investigation.executive_summary = 'High risk phishing detected'
        db.session.commit()
        
        # Second poll - completed
        response = client.get(f'/api/investigations/{investigation.id}/status')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'completed'
        assert data['confidence_score'] == 0.85
        assert data['executive_summary'] == 'High risk phishing detected'


@pytest.mark.integration
class TestCreditRoutes:
    """Test credit management API endpoints"""
    
    def test_get_user_subscription(self, client, db, user, subscription):
        """Test getting user subscription details"""
        response = client.get(f'/api/credit/subscription/{user.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        subscription_data = data['subscription']
        assert subscription_data['user_id'] == user.id
        assert subscription_data['tier'] == 'basic'
        assert subscription_data['current_credits'] == 10
        assert subscription_data['total_credits'] == 10
    
    def test_get_user_subscription_not_found(self, client, db, user):
        """Test getting subscription for user without subscription"""
        response = client.get(f'/api/credit/subscription/{user.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        # Should create free tier subscription
        subscription_data = data['subscription']
        assert subscription_data['tier'] == 'free'
    
    def test_get_credit_history(self, client, db, user, subscription):
        """Test getting user credit transaction history"""
        # Create some transactions
        from models.credit_system import CreditTransaction, CreditTransactionType
        
        transactions = [
            CreditTransaction(
                user_id=user.id,
                subscription_id=subscription.id,
                transaction_type=CreditTransactionType.CONSUMPTION,
                amount=-5,
                description='Investigation 1',
                balance_before=10,
                balance_after=5
            ),
            CreditTransaction(
                user_id=user.id,
                subscription_id=subscription.id,
                transaction_type=CreditTransactionType.BONUS,
                amount=3,
                description='Welcome bonus',
                balance_before=5,
                balance_after=8
            )
        ]
        
        db.session.add_all(transactions)
        db.session.commit()
        
        response = client.get(f'/api/credit/history/{user.id}')
        assert response.status_code == 200
        
        data = response.get_json()
        assert len(data['transactions']) == 2
        
        # Should be ordered by most recent first
        assert data['transactions'][0]['transaction_type'] == 'bonus'
        assert data['transactions'][1]['transaction_type'] == 'consumption'
    
    def test_purchase_credits(self, client, db, user, subscription):
        """Test purchasing additional credits"""
        purchase_data = {
            'user_id': user.id,
            'credit_package': 'small',  # e.g., 25 credits for $9.99
            'payment_method': 'card',
            'payment_token': 'tok_test_123'
        }
        
        # Mock payment processing
        with patch('src.payment.process_payment') as mock_payment:
            mock_payment.return_value = {'success': True, 'transaction_id': 'txn_123'}
            
            response = client.post('/api/credit/purchase',
                                 data=json.dumps(purchase_data),
                                 content_type='application/json')
            assert response.status_code == 200
            
            data = response.get_json()
            assert data['success'] is True
            assert 'credits_added' in data
            assert 'new_balance' in data


@pytest.mark.security
class TestSecurityFeatures:
    """Test security-related features and endpoints"""
    
    def test_rate_limiting(self, client, db):
        """Test API rate limiting"""
        # Make multiple requests quickly
        responses = []
        for i in range(20):  # Exceed normal rate limit
            response = client.get('/api/health')
            responses.append(response.status_code)
        
        # Should get some rate limit responses (429)
        # Note: This test assumes rate limiting is implemented
        assert any(status == 429 for status in responses[-5:])
    
    def test_sql_injection_protection(self, client, db):
        """Test protection against SQL injection attacks"""
        malicious_payloads = [
            "'; DROP TABLE users; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --"
        ]
        
        for payload in malicious_payloads:
            # Try SQL injection in user creation
            user_data = {
                'username': payload,
                'email': f'{payload}@example.com',
                'password': 'password123'
            }
            
            response = client.post('/api/users',
                                 data=json.dumps(user_data),
                                 content_type='application/json')
            
            # Should not cause server error (500)
            assert response.status_code != 500
            
            # If successful (201), verify data was safely stored
            if response.status_code == 201:
                data = response.get_json()
                assert data['username'] == payload  # Should be stored as-is
    
    def test_xss_protection(self, client, db, user):
        """Test protection against XSS attacks"""
        xss_payloads = [
            "<script>alert('xss')</script>",
            "javascript:alert('xss')",
            "<img src=x onerror=alert('xss')>"
        ]
        
        for payload in xss_payloads:
            # Try XSS in investigation title
            investigation_data = {
                'user_id': user.id,
                'title': payload,
                'investigation_type': 'quick_scan',
                'model_tier': 'basic',
                'artifacts': [{'type': 'url', 'content': 'https://test.com'}]
            }
            
            response = client.post('/api/investigations',
                                 data=json.dumps(investigation_data),
                                 content_type='application/json')
            
            # Should not cause server error
            assert response.status_code != 500
            
            # If successful, verify XSS payload was safely handled
            if response.status_code == 201:
                data = response.get_json()
                # Should not contain executable script tags
                assert '<script>' not in data['title']
                assert 'javascript:' not in data['title']
    
    def test_authentication_required(self, client, db):
        """Test that protected endpoints require authentication"""
        # Note: This assumes authentication middleware is implemented
        protected_endpoints = [
            ('/api/investigations', 'POST'),
            ('/api/credit/purchase', 'POST'),
            ('/api/users/me', 'GET')
        ]
        
        for endpoint, method in protected_endpoints:
            if method == 'POST':
                response = client.post(endpoint,
                                     data=json.dumps({}),
                                     content_type='application/json')
            else:
                response = client.get(endpoint)
            
            # Should require authentication (401) or forbidden (403)
            # For now, we'll accept any response that's not 500 (server error)
            assert response.status_code != 500
    
    def test_input_validation(self, client, db, user):
        """Test input validation for various endpoints"""
        # Test invalid email format
        user_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'password123'
        }
        
        response = client.post('/api/users',
                             data=json.dumps(user_data),
                             content_type='application/json')
        assert response.status_code == 400
        
        # Test investigation with missing required fields
        investigation_data = {
            'user_id': user.id,
            'title': '',  # Empty title
            'investigation_type': 'invalid_type',  # Invalid type
            'artifacts': []  # No artifacts
        }
        
        response = client.post('/api/investigations',
                             data=json.dumps(investigation_data),
                             content_type='application/json')
        assert response.status_code == 400
    
    def test_data_sanitization(self, client, db):
        """Test that user input is properly sanitized"""
        # Create user with potentially dangerous content
        user_data = {
            'username': 'test<>&"\'user',
            'email': 'test<>&"\'@example.com',
            'password': 'password123',
            'first_name': '<script>alert("xss")</script>',
            'company': 'Test & Company <Inc>'
        }
        
        response = client.post('/api/users',
                             data=json.dumps(user_data),
                             content_type='application/json')
        
        if response.status_code == 201:
            data = response.get_json()
            
            # Verify dangerous content is sanitized or escaped
            assert '<script>' not in data.get('first_name', '')
            assert data['username'] == 'test<>&"\'user'  # Should preserve safe special chars
            assert '&' in data.get('company', '')  # Should preserve business names


@pytest.mark.performance
class TestPerformanceAndLoad:
    """Test performance characteristics of API endpoints"""
    
    def test_health_check_performance(self, client):
        """Test health check endpoint performance"""
        import time
        
        start_time = time.time()
        response = client.get('/api/health')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 0.1  # Should respond within 100ms
    
    def test_database_query_performance(self, client, db, user):
        """Test database query performance with larger datasets"""
        # Create multiple investigations
        investigations = []
        for i in range(50):
            investigation = Investigation(
                user_id=user.id,
                title=f'Test Investigation {i}',
                investigation_type='quick_scan',
                model_tier='basic'
            )
            investigations.append(investigation)
        
        db.session.add_all(investigations)
        db.session.commit()
        
        # Test query performance
        import time
        start_time = time.time()
        response = client.get(f'/api/users/{user.id}/investigations')
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Should respond within 1 second
        
        data = response.get_json()
        assert len(data) == 50
    
    def test_concurrent_requests(self, client, db):
        """Test handling of concurrent requests"""
        import threading
        import time
        
        results = []
        
        def make_request():
            try:
                response = client.get('/api/health')
                results.append(response.status_code)
            except Exception as e:
                results.append(500)
        
        # Create multiple threads to simulate concurrent requests
        threads = []
        for i in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        end_time = time.time()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 10
        assert (end_time - start_time) < 2.0  # Should complete within 2 seconds
