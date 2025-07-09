"""
ScamShield AI - Enhanced Backend Application

Elite fraud investigation platform with hybrid AI capabilities, credit system, and advanced reporting
Enhanced with comprehensive error handling, logging, and security features.
"""

import os
import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import uuid
import json

from flask import Flask, request, jsonify, send_from_directory, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import base64

# Import AI Engine components
from ai_engine.investigation_engine import InvestigationEngine, InvestigationRequest, InvestigationType
from ai_engine.model_manager_v2 import ModelTier
from ai_engine.prompt_engineering import prompt_engineer, AnalysisDepth

# Import Credit System components
from models.credit_system import (
    Subscription, CreditTransaction, SubscriptionTier, CreditCalculator,
    InvestigationComplexity, ProcessingPriority
)
from routes.credit_management import credit_bp

# Import Report Generation components
from report_templates.report_generator import (
    ReportGenerator, ReportTier, ReportFormat, ReportStatus
)

# Import Database models
from models.user import db as user_db, User
from models.investigation import Investigation, Report, Evidence, ScamDatabase, EvidenceType

# Import Enhanced Utilities
from utils.error_handler import (
    ErrorHandler, APIError, ValidationError, SecurityError, BusinessLogicError, ErrorContext
)
from utils.logging_config import setup_logging, get_logger, log_request_middleware
from utils.validators import (
    validate_email, validate_phone, validate_url, sanitize_input, 
    validate_required_fields, validate_username
)
from utils.security_utils import (
    TokenSecurity, PasswordSecurity, SecurityMonitoring, CSRFProtection,
    hash_password, verify_password
)

# Setup enhanced logging
setup_logging(
    app_name="scamshield_ai",
    log_level=os.environ.get('LOG_LEVEL', 'INFO'),
    enable_structured=True,
    enable_security_filter=True,
    enable_performance_filter=False
)

logger = get_logger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')

# Enhanced Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'scamshield-ai-secret-key-2025')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///scamshield_ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['DEBUG'] = os.environ.get('FLASK_ENV') == 'development'

# Security Configuration
app.config['WTF_CSRF_ENABLED'] = True
app.config['SESSION_COOKIE_SECURE'] = not app.config['DEBUG']
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Initialize enhanced extensions
CORS(app, origins=["*"], supports_credentials=True)
user_db.init_app(app)

# Initialize enhanced error handling
error_handler = ErrorHandler(app)

# Initialize security components
token_security = TokenSecurity(app.config['SECRET_KEY'])
security_monitor = SecurityMonitoring()
csrf_protection = CSRFProtection(app.config['SECRET_KEY'])

# Register request middleware for logging
log_request_middleware(app)

# Register blueprints
app.register_blueprint(credit_bp)

# Initialize AI Investigation Engine
investigation_engine = InvestigationEngine()

# Tier pricing configuration
TIER_PRICING = {
    ModelTier.BASIC: {"price": 9.99, "credits": 10, "name": "Basic Scam Detection"},
    ModelTier.PROFESSIONAL: {"price": 49.99, "credits": 25, "name": "Professional Investigation"},
    ModelTier.ENTERPRISE: {"price": 199.99, "credits": 100, "name": "Enterprise Intelligence"},
    ModelTier.INTELLIGENCE: {"price": 499.99, "credits": 250, "name": "Elite Intelligence Analysis"}
}

@app.before_first_request
def create_tables():
    """Create database tables and initialize application"""
    with app.app_context():
        user_db.create_all()
        logger.info("Database tables created")
        
        # Initialize default data if needed
        from models.credit_system import DEFAULT_SUBSCRIPTION_PLANS, SubscriptionPlan
        for plan_data in DEFAULT_SUBSCRIPTION_PLANS:
            existing_plan = SubscriptionPlan.query.filter_by(tier=plan_data['tier']).first()
            if not existing_plan:
                plan = SubscriptionPlan(**plan_data)
                user_db.session.add(plan)
        
        try:
            user_db.session.commit()
            logger.info("Default subscription plans initialized")
        except Exception as e:
            user_db.session.rollback()
            logger.error(f"Error initializing default data: {str(e)}")

@app.before_request
def security_checks():
    """Enhanced security checks for each request"""
    # Generate request ID for tracking
    g.request_id = str(uuid.uuid4())
    
    # Rate limiting check
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if security_monitor.check_rate_limit(client_ip, limit=100, window=60):
        logger.security("Rate limit exceeded", ip_address=client_ip)
        raise APIError(
            message="Rate limit exceeded",
            error_type="rate_limit",
            status_code=429,
            user_message="Too many requests. Please try again later."
        )
    
    # Check for suspicious IP
    if security_monitor.is_suspicious_ip(client_ip):
        logger.security("Request from suspicious IP", ip_address=client_ip)
        # Log but don't block - might be legitimate user
    
    # Detect suspicious patterns
    request_data = {
        'method': request.method,
        'path': request.path,
        'user_agent': request.headers.get('User-Agent', ''),
        'ip_address': client_ip
    }
    
    suspicious_patterns = security_monitor.detect_suspicious_patterns(request_data)
    if suspicious_patterns:
        logger.security("Suspicious request patterns detected",
                       patterns=suspicious_patterns,
                       **request_data)
    
    # Add security headers
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Content-Security-Policy'] = "default-src 'self'"
        
        # Add request ID to response for tracking
        if hasattr(g, 'request_id'):
            response.headers['X-Request-ID'] = g.request_id
        
        return response

# ============ CORE API ENDPOINTS ============

@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health')
def health_check():
    """Enhanced health check endpoint with system metrics"""
    with ErrorContext("health_check"):
        try:
            # Check database connectivity
            user_db.session.execute('SELECT 1')
            db_status = "healthy"
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            db_status = "unhealthy"
        
        # Check AI engine status
        try:
            ai_status = "operational" if investigation_engine else "unavailable"
        except Exception:
            ai_status = "error"
        
        # Get error statistics
        error_stats = error_handler.get_error_statistics()
        
        health_data = {
            "status": "healthy" if db_status == "healthy" and ai_status == "operational" else "degraded",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "version": "2.1.0",
            "components": {
                "database": db_status,
                "ai_engine": ai_status,
                "error_handler": "operational"
            },
            "error_statistics": {
                "total_errors": sum(error_stats["error_counts"].values()),
                "critical_errors": error_stats["critical_errors_count"]
            },
            "request_id": getattr(g, 'request_id', 'unknown')
        }
        
        logger.info("Health check completed", extra=health_data)
        return jsonify(health_data)

# ============ ENHANCED USER MANAGEMENT ============

@app.route('/api/users', methods=['POST'])
def create_user():
    """Enhanced user creation with comprehensive validation and security"""
    with ErrorContext("create_user", user_id=None):
        try:
            # Validate request data
            if not request.is_json:
                raise ValidationError("Request must be JSON", field="content_type")
            
            data = request.get_json()
            if not data:
                raise ValidationError("Request body is required", field="body")
            
            # Sanitize input data
            data = sanitize_input(data, max_length=255)
            
            # Validate required fields
            validate_required_fields(data, ['username', 'email', 'password'])
            
            # Validate individual fields
            username = validate_username(data['username'])
            email = validate_email(data['email'])
            password = data['password']
            
            # Password strength validation
            password_strength = PasswordSecurity.check_password_strength(password)
            if password_strength['score'] < 40:
                raise ValidationError(
                    "Password is too weak",
                    field="password",
                    details={
                        "strength": password_strength['strength'],
                        "issues": password_strength['issues'],
                        "suggestions": password_strength.get('requirements_met', [])
                    }
                )
            
            # Check for existing user
            existing_user = User.query.filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.username == username:
                    raise ValidationError("Username already exists", field="username")
                else:
                    raise ValidationError("Email already registered", field="email")
            
            # Create user with hashed password
            hashed_password = hash_password(password)
            
            user = User(
                username=username,
                email=email,
                password=hashed_password,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                company=data.get('company'),
                phone=data.get('phone')
            )
            
            user_db.session.add(user)
            user_db.session.commit()
            
            # Log successful user creation
            logger.business("User created successfully", 
                          user_id=user.id, 
                          username=username,
                          email=email)
            
            # Return user data (excluding sensitive information)
            response_data = {
                "user": user.to_dict(),
                "message": "User created successfully",
                "request_id": g.request_id
            }
            
            return jsonify(response_data), 201
            
        except ValidationError:
            raise  # Re-raise validation errors
        except Exception as e:
            user_db.session.rollback()
            logger.error(f"User creation failed: {str(e)}")
            raise APIError(
                message=f"Failed to create user: {str(e)}",
                error_type="internal",
                status_code=500
            )

@app.route('/api/auth/login', methods=['POST'])
def login_user():
    """Enhanced user authentication with security monitoring"""
    with ErrorContext("user_login"):
        try:
            # Validate request
            if not request.is_json:
                raise ValidationError("Request must be JSON", field="content_type")
            
            data = request.get_json()
            if not data:
                raise ValidationError("Request body is required", field="body")
            
            # Sanitize and validate input
            data = sanitize_input(data)
            validate_required_fields(data, ['username', 'password'])
            
            username = data['username']
            password = data['password']
            client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
            
            # Find user
            user = User.query.filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if not user:
                # Track failed attempt (even for non-existent users)
                security_monitor.track_failed_login(username, client_ip)
                logger.security("Login attempt for non-existent user",
                               username=username,
                               ip_address=client_ip)
                raise SecurityError("Invalid credentials")
            
            # Check if account is locked
            if user.is_account_locked():
                logger.security("Login attempt for locked account",
                               user_id=user.id,
                               ip_address=client_ip)
                raise SecurityError("Account is temporarily locked due to multiple failed attempts")
            
            # Verify password
            if not verify_password(password, user.password_hash):
                # Track failed attempt
                should_lock = security_monitor.track_failed_login(user.id, client_ip)
                user.increment_failed_login()
                
                if should_lock:
                    logger.security("Account locked due to multiple failed attempts",
                                   user_id=user.id,
                                   ip_address=client_ip)
                
                user_db.session.commit()
                raise SecurityError("Invalid credentials")
            
            # Successful login
            user.update_last_login()
            user_db.session.commit()
            
            # Generate JWT token
            token_payload = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'is_admin': user.is_admin
            }
            
            access_token = token_security.generate_jwt_token(token_payload)
            
            logger.business("User logged in successfully",
                          user_id=user.id,
                          username=user.username,
                          ip_address=client_ip)
            
            response_data = {
                "user": user.to_dict(),
                "access_token": access_token,
                "token_type": "Bearer",
                "message": "Login successful",
                "request_id": g.request_id
            }
            
            return jsonify(response_data), 200
            
        except (ValidationError, SecurityError):
            raise  # Re-raise these specific errors
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise APIError(
                message="Login failed",
                error_type="internal",
                status_code=500
            )

# ============ ENHANCED INVESTIGATION ENDPOINTS ============

@app.route('/api/investigations', methods=['POST'])
def create_investigation():
    """Enhanced investigation creation with comprehensive validation"""
    with ErrorContext("create_investigation"):
        try:
            # Validate request
            if not request.is_json:
                raise ValidationError("Request must be JSON", field="content_type")
            
            data = request.get_json()
            if not data:
                raise ValidationError("Request body is required", field="body")
            
            # Sanitize input
            data = sanitize_input(data, max_length=1000)
            
            # Validate required fields
            validate_required_fields(data, ['user_id', 'title', 'investigation_type', 'artifacts'])
            
            user_id = data['user_id']
            title = data['title']
            investigation_type = data['investigation_type']
            artifacts = data['artifacts']
            
            # Validate user exists
            user = User.query.get(user_id)
            if not user:
                raise ValidationError("User not found", field="user_id")
            
            # Validate investigation type
            valid_types = ['quick_scan', 'deep_analysis', 'comprehensive', 'elite_intelligence']
            if investigation_type not in valid_types:
                raise ValidationError(
                    f"Invalid investigation type. Must be one of: {', '.join(valid_types)}",
                    field="investigation_type"
                )
            
            # Validate artifacts
            if not isinstance(artifacts, list) or len(artifacts) == 0:
                raise ValidationError("At least one artifact is required", field="artifacts")
            
            for i, artifact in enumerate(artifacts):
                if not isinstance(artifact, dict):
                    raise ValidationError(f"Artifact {i} must be an object", field=f"artifacts[{i}]")
                
                validate_required_fields(artifact, ['type', 'content'])
                
                # Validate artifact content based on type
                artifact_type = artifact['type']
                content = artifact['content']
                
                if artifact_type == 'url':
                    validate_url(content)
                elif artifact_type == 'email':
                    validate_email(content)
                elif artifact_type == 'phone':
                    validate_phone(content)
                # Add more artifact type validations as needed
            
            # Check user's credit balance
            subscription = Subscription.query.filter_by(
                user_id=user_id,
                status='active'
            ).first()
            
            if not subscription:
                raise BusinessLogicError(
                    "No active subscription found",
                    suggestion="Please subscribe to a plan to create investigations"
                )
            
            # Calculate investigation cost
            complexity = InvestigationComplexity.MODERATE  # Default
            priority = ProcessingPriority.NORMAL
            
            estimated_cost = CreditCalculator.calculate_investigation_cost(
                investigation_type=investigation_type,
                complexity=complexity,
                priority=priority,
                tier=subscription.tier,
                artifact_count=len(artifacts)
            )
            
            if subscription.total_credits < estimated_cost:
                raise BusinessLogicError(
                    f"Insufficient credits. Required: {estimated_cost}, Available: {subscription.total_credits}",
                    suggestion="Please purchase additional credits or upgrade your plan"
                )
            
            # Create investigation
            investigation = Investigation(
                user_id=user_id,
                title=title,
                description=data.get('description'),
                investigation_type=investigation_type,
                model_tier=data.get('model_tier', 'basic'),
                priority=data.get('priority', 'normal')
            )
            
            user_db.session.add(investigation)
            user_db.session.flush()  # Get investigation ID
            
            # Create evidence records
            for artifact in artifacts:
                # Map artifact type to evidence type enum
                evidence_type_map = {
                    'url': EvidenceType.URL,
                    'email': EvidenceType.EMAIL,
                    'phone': EvidenceType.PHONE,
                    'image': EvidenceType.IMAGE,
                    'document': EvidenceType.DOCUMENT,
                    'social_media': EvidenceType.SOCIAL_MEDIA,
                    'cryptocurrency': EvidenceType.CRYPTOCURRENCY,
                    'ip_address': EvidenceType.IP_ADDRESS,
                    'domain': EvidenceType.DOMAIN
                }
                
                evidence_type = evidence_type_map.get(artifact['type'])
                if not evidence_type:
                    raise ValidationError(
                        f"Invalid artifact type: {artifact['type']}",
                        field="artifacts"
                    )
                
                evidence = Evidence(
                    investigation_id=investigation.id,
                    evidence_type=evidence_type,
                    content=artifact['content'],
                    metadata=artifact.get('metadata', {})
                )
                user_db.session.add(evidence)
            
            user_db.session.commit()
            
            logger.business("Investigation created",
                          investigation_id=investigation.id,
                          user_id=user_id,
                          investigation_type=investigation_type,
                          artifact_count=len(artifacts),
                          estimated_cost=estimated_cost)
            
            # Start investigation processing asynchronously
            # This would typically be handled by a background task queue
            logger.info(f"Investigation {investigation.id} queued for processing")
            
            response_data = {
                "investigation": investigation.to_dict(include_detailed=False),
                "estimated_cost": estimated_cost,
                "message": "Investigation created and queued for processing",
                "request_id": g.request_id
            }
            
            return jsonify(response_data), 201
            
        except (ValidationError, BusinessLogicError):
            raise  # Re-raise these specific errors
        except Exception as e:
            user_db.session.rollback()
            logger.error(f"Investigation creation failed: {str(e)}")
            raise APIError(
                message=f"Failed to create investigation: {str(e)}",
                error_type="internal",
                status_code=500
            )

@app.route('/api/tiers')
def get_tiers():
    """Get available investigation tiers"""
    tiers = []
    for tier, config in TIER_PRICING.items():
        tiers.append({
            "tier": tier.value,
            "name": config["name"],
            "price": config["price"],
            "credits": config["credits"],
            "features": get_tier_features(tier)
        })
    
    return jsonify({"tiers": tiers})

def get_tier_features(tier: ModelTier) -> List[str]:
    """Get features for each tier"""
    features = {
        ModelTier.BASIC: [
            "Quick scam detection",
            "Basic risk assessment",
            "Community database check",
            "Simple fraud patterns",
            "Basic recommendations"
        ],
        ModelTier.PROFESSIONAL: [
            "Advanced AI analysis",
            "Multi-modal artifact analysis",
            "Behavioral profiling",
            "Technical infrastructure analysis",
            "Detailed investigation reports",
            "Priority support"
        ],
        ModelTier.ENTERPRISE: [
            "Elite AI model ensemble",
            "Comprehensive threat intelligence",
            "Strategic attribution analysis",
            "Campaign tracking",
            "Advanced pattern recognition",
            "Custom investigation workflows",
            "API access",
            "Dedicated support"
        ],
        ModelTier.INTELLIGENCE: [
            "Maximum AI capabilities",
            "Real-time threat correlation",
            "Strategic intelligence assessment",
            "Predictive threat modeling",
            "Elite-level analysis depth",
            "Custom AI model training",
            "White-glove service",
            "24/7 expert support"
        ]
    }
    return features.get(tier, [])

# ============ INVESTIGATION ENDPOINTS ============

@app.route('/api/investigate', methods=['POST'])
async def create_investigation():
    """Create a new investigation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['tier', 'artifacts']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Parse tier
        try:
            tier = ModelTier(data['tier'])
        except ValueError:
            return jsonify({"error": "Invalid tier specified"}), 400
        
        # Parse investigation type
        investigation_type = InvestigationType(data.get('investigation_type', 'comprehensive'))
        
        # Generate investigation ID
        investigation_id = str(uuid.uuid4())
        
        # Create investigation request
        investigation_request = InvestigationRequest(
            investigation_id=investigation_id,
            user_id=data.get('user_id', 'anonymous'),
            tier=tier,
            investigation_type=investigation_type,
            artifacts=data['artifacts'],
            context=data.get('context'),
            priority=data.get('priority', 'normal')
        )
        
        # Start investigation (async)
        result = await investigation_engine.conduct_investigation(investigation_request)
        
        # Store investigation in database
        investigation = Investigation(
            id=investigation_id,
            user_id=investigation_request.user_id,
            tier=tier.value,
            status='completed',
            artifacts_count=len(investigation_request.artifacts),
            threat_level=result.threat_level.value,
            confidence_score=result.confidence_score,
            processing_time=result.processing_time,
            cost=result.cost,
            created_at=investigation_request.timestamp,
            completed_at=result.timestamp
        )
        
        user_db.session.add(investigation)
        user_db.session.commit()
        
        # Create investigation report
        report = Report(
            investigation_id=investigation_id,
            executive_summary=result.executive_summary,
            detailed_findings=json.dumps(result.detailed_findings),
            evidence_analysis=json.dumps(result.evidence_analysis),
            recommendations=json.dumps(result.recommendations),
            models_used=json.dumps(result.models_used)
        )
        
        user_db.session.add(report)
        user_db.session.commit()
        
        return jsonify({
            "investigation_id": investigation_id,
            "status": "completed",
            "result": result.to_dict()
        })
        
    except Exception as e:
        logger.error(f"Investigation creation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/investigate/quick', methods=['POST'])
async def quick_investigation():
    """Perform quick investigation for basic tier"""
    try:
        data = request.get_json()
        
        if 'url' not in data and 'content' not in data:
            return jsonify({"error": "URL or content required"}), 400
        
        # Create artifact from input
        if 'url' in data:
            artifact = {"type": "url", "content": data['url']}
        else:
            artifact = {"type": "text", "content": data['content']}
        
        # Create quick investigation request
        investigation_id = str(uuid.uuid4())
        investigation_request = InvestigationRequest(
            investigation_id=investigation_id,
            user_id='anonymous',
            tier=ModelTier.BASIC,
            investigation_type=InvestigationType.QUICK_SCAN,
            artifacts=[artifact]
        )
        
        # Conduct investigation
        result = await investigation_engine.conduct_investigation(investigation_request)
        
        return jsonify({
            "investigation_id": investigation_id,
            "threat_level": result.threat_level.value,
            "confidence_score": result.confidence_score,
            "executive_summary": result.executive_summary,
            "recommendations": result.recommendations[:3],  # Top 3 recommendations
            "processing_time": result.processing_time
        })
        
    except Exception as e:
        logger.error(f"Quick investigation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/investigate/<investigation_id>')
def get_investigation(investigation_id):
    """Get investigation details"""
    try:
        investigation = Investigation.query.filter_by(id=investigation_id).first()
        if not investigation:
            return jsonify({"error": "Investigation not found"}), 404
        
        report = Report.query.filter_by(investigation_id=investigation_id).first()
        
        result = {
            "investigation_id": investigation_id,
            "tier": investigation.tier,
            "status": investigation.status,
            "threat_level": investigation.threat_level,
            "confidence_score": investigation.confidence_score,
            "processing_time": investigation.processing_time,
            "cost": investigation.cost,
            "created_at": investigation.created_at.isoformat(),
            "completed_at": investigation.completed_at.isoformat() if investigation.completed_at else None
        }
        
        if report:
            result.update({
                "executive_summary": report.executive_summary,
                "detailed_findings": json.loads(report.detailed_findings) if report.detailed_findings else {},
                "evidence_analysis": json.loads(report.evidence_analysis) if report.evidence_analysis else {},
                "recommendations": json.loads(report.recommendations) if report.recommendations else [],
                "models_used": json.loads(report.models_used) if report.models_used else []
            })
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Failed to get investigation {investigation_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/investigate/<investigation_id>/status')
def get_investigation_status(investigation_id):
    """Get investigation status"""
    try:
        # Check active investigations first
        status = investigation_engine.get_investigation_status(investigation_id)
        if status:
            return jsonify(status)
        
        # Check database for completed investigations
        investigation = Investigation.query.filter_by(id=investigation_id).first()
        if investigation:
            return jsonify({
                "investigation_id": investigation_id,
                "status": investigation.status,
                "tier": investigation.tier,
                "created_at": investigation.created_at.isoformat()
            })
        
        return jsonify({"error": "Investigation not found"}), 404
        
    except Exception as e:
        logger.error(f"Failed to get investigation status: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ ARTIFACT UPLOAD ENDPOINTS ============

@app.route('/api/upload', methods=['POST'])
def upload_artifact():
    """Upload artifact for investigation"""
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Secure filename
        filename = secure_filename(file.filename)
        
        # Read file content
        file_content = file.read()
        file_size = len(file_content)
        
        # Determine file type
        file_extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        
        # Create artifact object
        artifact = {
            "type": "document" if file_extension in ['pdf', 'doc', 'docx', 'txt'] else "image" if file_extension in ['jpg', 'jpeg', 'png', 'gif'] else "unknown",
            "filename": filename,
            "file_size": file_size,
            "file_type": file_extension,
            "content": base64.b64encode(file_content).decode('utf-8') if file_extension in ['jpg', 'jpeg', 'png', 'gif'] else file_content.decode('utf-8', errors='ignore')
        }
        
        return jsonify({
            "artifact": artifact,
            "message": "File uploaded successfully"
        })
        
    except Exception as e:
        logger.error(f"File upload failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ SCAM DATABASE ENDPOINTS ============

@app.route('/api/scam-database')
def get_scam_database():
    """Get scam database entries"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        query = ScamDatabase.query
        
        if search:
            query = query.filter(
                ScamDatabase.entity_name.contains(search) |
                ScamDatabase.domain.contains(search) |
                ScamDatabase.description.contains(search)
            )
        
        scams = query.order_by(ScamDatabase.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            "scams": [{
                "id": scam.id,
                "entity_name": scam.entity_name,
                "domain": scam.domain,
                "threat_type": scam.threat_type,
                "risk_level": scam.risk_level,
                "description": scam.description,
                "evidence_count": scam.evidence_count,
                "verified": scam.verified,
                "created_at": scam.created_at.isoformat()
            } for scam in scams.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": scams.total,
                "pages": scams.pages,
                "has_next": scams.has_next,
                "has_prev": scams.has_prev
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get scam database: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/scam-database/<int:scam_id>')
def get_scam_details(scam_id):
    """Get detailed scam information"""
    try:
        scam = ScamDatabase.query.get_or_404(scam_id)
        
        return jsonify({
            "id": scam.id,
            "entity_name": scam.entity_name,
            "domain": scam.domain,
            "threat_type": scam.threat_type,
            "risk_level": scam.risk_level,
            "description": scam.description,
            "indicators": json.loads(scam.indicators) if scam.indicators else [],
            "evidence_count": scam.evidence_count,
            "verified": scam.verified,
            "created_at": scam.created_at.isoformat(),
            "updated_at": scam.updated_at.isoformat()
        })
        
    except Exception as e:
        logger.error(f"Failed to get scam details: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/report-scam', methods=['POST'])
def report_scam():
    """Report a new scam"""
    try:
        data = request.get_json()
        
        required_fields = ['entity_name', 'description']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create new scam report
        scam = ScamDatabase(
            entity_name=data['entity_name'],
            domain=data.get('domain', ''),
            threat_type=data.get('threat_type', 'unknown'),
            risk_level=data.get('risk_level', 'medium'),
            description=data['description'],
            indicators=json.dumps(data.get('indicators', [])),
            evidence_count=data.get('evidence_count', 0),
            verified=False  # Requires manual verification
        )
        
        user_db.session.add(scam)
        user_db.session.commit()
        
        return jsonify({
            "message": "Scam reported successfully",
            "scam_id": scam.id
        })
        
    except Exception as e:
        logger.error(f"Failed to report scam: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ STATISTICS ENDPOINTS ============

@app.route('/api/stats')
def get_statistics():
    """Get platform statistics"""
    try:
        # Investigation statistics
        total_investigations = Investigation.query.count()
        recent_investigations = Investigation.query.filter(
            Investigation.created_at >= datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        
        # Threat level distribution
        threat_levels = user_db.session.query(
            Investigation.threat_level,
            user_db.func.count(Investigation.threat_level)
        ).group_by(Investigation.threat_level).all()
        
        threat_distribution = {level: count for level, count in threat_levels}
        
        # Scam database statistics
        total_scams = ScamDatabase.query.count()
        verified_scams = ScamDatabase.query.filter_by(verified=True).count()
        
        # Tier usage statistics
        tier_usage = user_db.session.query(
            Investigation.tier,
            user_db.func.count(Investigation.tier)
        ).group_by(Investigation.tier).all()
        
        tier_distribution = {tier: count for tier, count in tier_usage}
        
        return jsonify({
            "investigations": {
                "total": total_investigations,
                "today": recent_investigations,
                "threat_distribution": threat_distribution,
                "tier_distribution": tier_distribution
            },
            "scam_database": {
                "total_entries": total_scams,
                "verified_entries": verified_scams,
                "verification_rate": (verified_scams / total_scams * 100) if total_scams > 0 else 0
            },
            "ai_engine": {
                "status": "operational",
                "models_available": len(investigation_engine.model_manager.model_configs),
                "active_investigations": len(investigation_engine.active_investigations)
            }
        })
        
    except Exception as e:
        logger.error(f"Failed to get statistics: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ AI MODEL ENDPOINTS ============

@app.route('/api/models')
def get_available_models():
    """Get available AI models"""
    try:
        models = []
        for model_name, config in investigation_engine.model_manager.model_configs.items():
            models.append({
                "name": model_name,
                "type": config.model_type.value,
                "tiers": [tier.value for tier in config.tier_access],
                "capabilities": config.capabilities,
                "cost_per_token": config.cost_per_token,
                "max_tokens": config.max_tokens
            })
        
        return jsonify({"models": models})
        
    except Exception as e:
        logger.error(f"Failed to get models: {str(e)}")
        return jsonify({"error": str(e)}), 500

# ============ ERROR HANDLERS ============

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

# ============ MAIN APPLICATION ============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting ScamShield AI Backend on port {port}")
    logger.info(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

