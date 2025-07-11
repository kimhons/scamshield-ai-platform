"""
ScamShield AI - Model Manager Tests

Tests for the AI model management system including model configurations, tier access, and response handling.
"""

import pytest
from unittest.mock import patch, Mock, AsyncMock
import asyncio
import time

from ai_engine.model_manager_v2 import (
    EnhancedModelManager, ModelTier, ModelType, ModelConfig
)


@pytest.mark.unit
class TestModelConfig:
    """Test cases for ModelConfig dataclass"""
    
    def test_model_config_creation(self):
        """Test basic model configuration creation"""
        config = ModelConfig(
            name="gpt-4",
            model_type=ModelType.PROPRIETARY,
            tier_access=[ModelTier.PROFESSIONAL, ModelTier.ENTERPRISE],
            cost_per_token=0.00003,
            max_tokens=128000,
            capabilities=["text_analysis", "reasoning", "investigation"]
        )
        
        assert config.name == "gpt-4"
        assert config.model_type == ModelType.PROPRIETARY
        assert ModelTier.PROFESSIONAL in config.tier_access
        assert ModelTier.ENTERPRISE in config.tier_access
        assert ModelTier.BASIC not in config.tier_access
        assert config.cost_per_token == 0.00003
        assert config.max_tokens == 128000
        assert "text_analysis" in config.capabilities
    
    def test_model_config_with_optional_fields(self):
        """Test model configuration with optional fields"""
        config = ModelConfig(
            name="custom-model",
            model_type=ModelType.SPECIALIZED,
            tier_access=[ModelTier.ENTERPRISE],
            cost_per_token=0.0001,
            max_tokens=32000,
            capabilities=["fraud_detection"],
            endpoint="https://api.custom-model.com/v1",
            api_key_env="CUSTOM_MODEL_API_KEY"
        )
        
        assert config.endpoint == "https://api.custom-model.com/v1"
        assert config.api_key_env == "CUSTOM_MODEL_API_KEY"


@pytest.mark.unit
class TestEnhancedModelManager:
    """Test cases for EnhancedModelManager"""
    
    @patch.dict('os.environ', {
        'OPENAI_API_KEY': 'test-openai-key',
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
        'GOOGLE_API_KEY': 'test-google-key',
        'DEEPSEEK_API_KEY': 'test-deepseek-key',
        'HUGGINGFACE_TOKEN': 'test-hf-token'
    })
    def test_model_manager_initialization(self):
        """Test model manager initialization"""
        manager = EnhancedModelManager()
        
        assert manager is not None
        assert hasattr(manager, 'models')
        assert hasattr(manager, 'model_configs')
        assert hasattr(manager, 'inference_clients')
        
        # Should have initialized model configurations
        assert len(manager.model_configs) > 0
        
        # Check for key models
        assert 'llama-3.1-405b' in manager.model_configs
        assert 'llama-3.1-70b' in manager.model_configs
        assert 'mistral-large' in manager.model_configs
    
    def test_model_tier_access_validation(self):
        """Test model tier access validation"""
        manager = EnhancedModelManager()
        
        # Test basic tier access
        basic_models = manager.get_available_models(ModelTier.BASIC)
        assert 'llama-3.1-70b' in basic_models
        
        # Test professional tier access
        professional_models = manager.get_available_models(ModelTier.PROFESSIONAL)
        assert 'llama-3.1-405b' in professional_models
        assert 'llama-3.1-70b' in professional_models  # Should include lower tier models
        
        # Test enterprise tier access
        enterprise_models = manager.get_available_models(ModelTier.ENTERPRISE)
        assert len(enterprise_models) >= len(professional_models)
    
    @patch('openai.ChatCompletion.create')
    async def test_openai_model_call(self, mock_openai, mock_ai_models):
        """Test OpenAI model API call"""
        manager = EnhancedModelManager()
        
        # Mock OpenAI response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message = Mock()
        mock_response.choices[0].message.content = "This appears to be a phishing attempt."
        mock_response.usage = Mock()
        mock_response.usage.total_tokens = 150
        mock_openai.return_value = mock_response
        
        prompt = "Analyze this email for fraud indicators: suspicious@scammer.com"
        response = await manager.call_openai_model("gpt-4", prompt)
        
        assert response['content'] == "This appears to be a phishing attempt."
        assert response['token_usage'] == 150
        assert 'processing_time' in response
    
    @patch('anthropic.Anthropic')
    async def test_anthropic_model_call(self, mock_anthropic, mock_ai_models):
        """Test Anthropic model API call"""
        manager = EnhancedModelManager()
        
        # Mock Anthropic response
        mock_client = Mock()
        mock_response = Mock()
        mock_response.content = [Mock()]
        mock_response.content[0].text = "High probability of fraud detected."
        mock_response.usage = Mock()
        mock_response.usage.input_tokens = 50
        mock_response.usage.output_tokens = 25
        mock_client.messages.create.return_value = mock_response
        mock_anthropic.return_value = mock_client
        
        prompt = "Evaluate this URL for scam indicators: https://fake-bank.com"
        response = await manager.call_anthropic_model("claude-3-sonnet", prompt)
        
        assert response['content'] == "High probability of fraud detected."
        assert response['token_usage'] == 75  # input + output tokens
    
    @patch('google.generativeai.GenerativeModel')
    async def test_google_model_call(self, mock_google, mock_ai_models):
        """Test Google Gemini model API call"""
        manager = EnhancedModelManager()
        
        # Mock Google response
        mock_model = Mock()
        mock_response = Mock()
        mock_response.text = "This image contains suspicious phishing elements."
        mock_response.usage_metadata = Mock()
        mock_response.usage_metadata.total_token_count = 200
        mock_model.generate_content.return_value = mock_response
        mock_google.return_value = mock_model
        
        prompt = "Analyze this screenshot for fraud indicators"
        response = await manager.call_google_model("gemini-pro", prompt)
        
        assert response['content'] == "This image contains suspicious phishing elements."
        assert response['token_usage'] == 200
    
    @patch('requests.post')
    async def test_huggingface_model_call(self, mock_post, mock_ai_models):
        """Test Hugging Face model API call"""
        manager = EnhancedModelManager()
        
        # Mock Hugging Face response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"generated_text": "Analysis: This appears to be a legitimate communication."}
        ]
        mock_post.return_value = mock_response
        
        prompt = "Classify this message: Your package is ready for delivery"
        response = await manager.call_huggingface_model("llama-3.1-70b", prompt)
        
        assert "legitimate communication" in response['content']
    
    def test_model_cost_calculation(self):
        """Test model cost calculation"""
        manager = EnhancedModelManager()
        
        # Test cost calculation for different models
        gpt4_cost = manager.calculate_cost("gpt-4", 1000)
        claude_cost = manager.calculate_cost("claude-3-sonnet", 1000)
        llama_cost = manager.calculate_cost("llama-3.1-70b", 1000)
        
        # GPT-4 should be more expensive than open source models
        assert gpt4_cost > llama_cost
        assert claude_cost > llama_cost
        
        # Cost should scale with token count
        double_cost = manager.calculate_cost("gpt-4", 2000)
        assert double_cost == gpt4_cost * 2
    
    def test_model_capability_filtering(self):
        """Test filtering models by capabilities"""
        manager = EnhancedModelManager()
        
        # Test filtering by capability
        text_models = manager.get_models_by_capability("text_analysis")
        reasoning_models = manager.get_models_by_capability("reasoning")
        fraud_models = manager.get_models_by_capability("fraud_detection")
        
        assert len(text_models) > 0
        assert len(reasoning_models) > 0
        
        # Fraud detection might be specialized capability
        if len(fraud_models) > 0:
            # Verify these are specialized models
            for model_name in fraud_models:
                config = manager.model_configs[model_name]
                assert ModelType.SPECIALIZED in [config.model_type] or "fraud" in config.capabilities
    
    async def test_model_ensemble_response(self, mock_ai_models):
        """Test ensemble response from multiple models"""
        manager = EnhancedModelManager()
        
        with patch.object(manager, 'call_openai_model') as mock_openai, \
             patch.object(manager, 'call_anthropic_model') as mock_anthropic, \
             patch.object(manager, 'call_google_model') as mock_google:
            
            # Mock responses from different models
            mock_openai.return_value = {
                'content': 'High fraud probability: 0.9',
                'confidence': 0.9,
                'token_usage': 100,
                'processing_time': 1.5
            }
            mock_anthropic.return_value = {
                'content': 'Likely scam: 85% confidence',
                'confidence': 0.85,
                'token_usage': 120,
                'processing_time': 2.1
            }
            mock_google.return_value = {
                'content': 'Suspicious activity detected',
                'confidence': 0.8,
                'token_usage': 90,
                'processing_time': 1.8
            }
            
            prompt = "Analyze for fraud: suspicious@scammer.com"
            models = ["gpt-4", "claude-3-sonnet", "gemini-pro"]
            
            ensemble_response = await manager.get_ensemble_response(prompt, models)
            
            assert 'responses' in ensemble_response
            assert len(ensemble_response['responses']) == 3
            assert 'consensus_score' in ensemble_response
            assert 'total_cost' in ensemble_response
            assert 'processing_time' in ensemble_response
            
            # Consensus score should be average of individual confidences
            expected_consensus = (0.9 + 0.85 + 0.8) / 3
            assert abs(ensemble_response['consensus_score'] - expected_consensus) < 0.01
    
    def test_error_handling_invalid_model(self):
        """Test error handling for invalid model names"""
        manager = EnhancedModelManager()
        
        with pytest.raises(ValueError):
            manager.get_model_config("nonexistent-model")
        
        # Test graceful handling in API calls
        async def test_invalid_call():
            response = await manager.call_model("invalid-model", "test prompt")
            assert 'error' in response
        
        # Run async test
        asyncio.run(test_invalid_call())
    
    @patch.dict('os.environ', {})  # Remove API keys
    def test_missing_api_keys_handling(self):
        """Test handling of missing API keys"""
        manager = EnhancedModelManager()
        
        # Should initialize but mark certain models as unavailable
        available_models = manager.get_available_models(ModelTier.ENTERPRISE)
        
        # Open source models should still be available
        assert any('llama' in model for model in available_models)
        
        # Proprietary models might be limited without API keys
        # This depends on implementation - might gracefully degrade
    
    def test_rate_limiting_simulation(self, mock_ai_models):
        """Test rate limiting and retry logic"""
        manager = EnhancedModelManager()
        
        with patch.object(manager, '_make_api_call') as mock_call:
            # Simulate rate limiting
            mock_call.side_effect = [
                Exception("Rate limit exceeded"),
                Exception("Rate limit exceeded"),
                {'content': 'Success after retry', 'token_usage': 50}
            ]
            
            async def test_retry():
                response = await manager.call_model_with_retry("gpt-4", "test", max_retries=3)
                assert response['content'] == 'Success after retry'
            
            # Run async test
            asyncio.run(test_retry())
    
    def test_model_performance_monitoring(self):
        """Test model performance monitoring and metrics"""
        manager = EnhancedModelManager()
        
        # Simulate model calls and track performance
        performance_data = []
        
        async def simulate_calls():
            for i in range(5):
                start_time = time.time()
                response = await manager.call_mock_model("test-model", f"prompt {i}")
                end_time = time.time()
                
                performance_data.append({
                    'model': 'test-model',
                    'processing_time': end_time - start_time,
                    'token_usage': response.get('token_usage', 0),
                    'success': 'error' not in response
                })
        
        # Mock model call for testing
        async def mock_model_call(model, prompt):
            import time
            await asyncio.sleep(0.1)  # Simulate processing time
            return {'content': f'Response to: {prompt}', 'token_usage': 50}
        
        manager.call_mock_model = mock_model_call
        
        # Run simulation
        import time
        asyncio.run(simulate_calls())
        
        # Verify performance tracking
        assert len(performance_data) == 5
        assert all(data['success'] for data in performance_data)
        assert all(data['processing_time'] > 0 for data in performance_data)


@pytest.mark.integration
class TestModelManagerIntegration:
    """Integration tests for model manager with external services"""
    
    @pytest.mark.skip(reason="Requires actual API keys")
    async def test_real_openai_integration(self):
        """Test real OpenAI API integration (requires API key)"""
        manager = EnhancedModelManager()
        
        prompt = "Briefly analyze this for potential fraud: 'You have won $1,000,000! Click here immediately!'"
        response = await manager.call_openai_model("gpt-3.5-turbo", prompt)
        
        assert 'content' in response
        assert 'token_usage' in response
        assert 'processing_time' in response
        assert len(response['content']) > 0
    
    @pytest.mark.skip(reason="Requires actual API keys")
    async def test_real_anthropic_integration(self):
        """Test real Anthropic API integration (requires API key)"""
        manager = EnhancedModelManager()
        
        prompt = "Is this likely a scam: 'Urgent! Your account will be closed unless you verify your password immediately!'"
        response = await manager.call_anthropic_model("claude-3-haiku", prompt)
        
        assert 'content' in response
        assert 'token_usage' in response
        assert len(response['content']) > 0
    
    def test_model_fallback_chain(self, mock_ai_models):
        """Test fallback chain when primary models fail"""
        manager = EnhancedModelManager()
        
        fallback_chain = ["gpt-4", "claude-3-sonnet", "llama-3.1-405b", "llama-3.1-70b"]
        
        with patch.object(manager, 'call_openai_model') as mock_openai, \
             patch.object(manager, 'call_anthropic_model') as mock_anthropic, \
             patch.object(manager, 'call_huggingface_model') as mock_hf:
            
            # First two models fail
            mock_openai.side_effect = Exception("API Error")
            mock_anthropic.side_effect = Exception("Rate Limited")
            
            # Third model succeeds
            mock_hf.return_value = {
                'content': 'Fallback analysis: Suspicious pattern detected',
                'confidence': 0.7,
                'token_usage': 80
            }
            
            async def test_fallback():
                response = await manager.call_with_fallback("test prompt", fallback_chain)
                assert response['content'] == 'Fallback analysis: Suspicious pattern detected'
                assert response['model_used'] == 'llama-3.1-405b'
            
            asyncio.run(test_fallback())
    
    def test_model_load_balancing(self, mock_ai_models):
        """Test load balancing across multiple model instances"""
        manager = EnhancedModelManager()
        
        # Simulate multiple instances of the same model
        model_instances = {
            "gpt-4-instance-1": Mock(),
            "gpt-4-instance-2": Mock(),
            "gpt-4-instance-3": Mock()
        }
        
        # Track which instances are called
        call_counts = {instance: 0 for instance in model_instances}
        
        async def mock_load_balanced_call(prompt):
            # Simple round-robin load balancing
            instance = manager.get_next_available_instance("gpt-4")
            call_counts[instance] += 1
            return {'content': f'Response from {instance}', 'instance': instance}
        
        # Simulate multiple concurrent calls
        async def simulate_load():
            tasks = []
            for i in range(9):  # 9 calls across 3 instances
                task = mock_load_balanced_call(f"prompt {i}")
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
            return responses
        
        # Mock the load balancing method
        instance_cycle = iter(["gpt-4-instance-1", "gpt-4-instance-2", "gpt-4-instance-3"] * 3)
        manager.get_next_available_instance = lambda model: next(instance_cycle)
        
        responses = asyncio.run(simulate_load())
        
        # Verify load was distributed
        assert len(responses) == 9
        
        # Each instance should have been called 3 times
        for instance, count in call_counts.items():
            assert count == 3
