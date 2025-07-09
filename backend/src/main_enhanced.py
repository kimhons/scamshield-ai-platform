"""
ScamShield AI - Enhanced Backend Application

Elite fraud investigation platform with hybrid AI capabilities, credit system, and advanced reporting
"""

import os
import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
import uuid
import json

from flask import Flask, request, jsonify, send_from_directory
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
    InvestigationComplexity, ProcessingPriority, CreditTransactionType
)
from routes.credit_management import credit_bp

# Import Report Generation components
from report_templates.report_generator import (
    ReportGenerator, ReportTier, ReportFormat, ReportStatus
)

# Import Database models
from models.user import db as user_db, User
from models.investigation import Investigation, Report, Evidence, ScamDatabase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='static', static_url_path='')

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'scamshield-ai-secret-key-2025')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///scamshield_ai.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Initialize extensions
CORS(app, origins=["*"])
user_db.init_app(app)

# Register blueprints
app.register_blueprint(credit_bp)

# Initialize AI Investigation Engine
investigation_engine = InvestigationEngine()

# Initialize Report Generator
report_generator = ReportGenerator()

# Subscription tier to report tier mapping
TIER_MAPPING = {
    SubscriptionTier.FREE: ReportTier.FREE,
    SubscriptionTier.BASIC: ReportTier.BASIC,
    SubscriptionTier.PLUS: ReportTier.PLUS,
    SubscriptionTier.PRO: ReportTier.PRO,
    SubscriptionTier.ENTERPRISE: ReportTier.ENTERPRISE
}

def _get_analysis_depth_from_tier(tier: SubscriptionTier) -> AnalysisDepth:
    """Map subscription tier to analysis depth"""
    mapping = {
        SubscriptionTier.FREE: AnalysisDepth.BASIC,
        SubscriptionTier.BASIC: AnalysisDepth.STANDARD,
        SubscriptionTier.PLUS: AnalysisDepth.ADVANCED,
        SubscriptionTier.PRO: AnalysisDepth.ELITE,
        SubscriptionTier.ENTERPRISE: AnalysisDepth.ELITE
    }
    return mapping.get(tier, AnalysisDepth.BASIC)

@app.before_first_request
def create_tables():
    """Create database tables"""
    with app.app_context():
        user_db.create_all()
        logger.info("Database tables created")

# ============ CORE API ENDPOINTS ============

@app.route('/')
def index():
    """Serve the main application"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "3.0.0",
        "ai_engine": "operational",
        "credit_system": "operational",
        "report_generator": "operational",
        "features": [
            "Elite AI Investigation",
            "Credit-Based Pricing",
            "Advanced Report Generation",
            "Multi-Tier Analysis",
            "Legal Compliance Framework"
        ]
    })

# ============ ENHANCED INVESTIGATION ENDPOINTS ============

@app.route('/api/investigate', methods=['POST'])
async def create_investigation():
    """Create a new investigation with credit system integration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['user_id', 'artifacts']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        user_id = data['user_id']
        artifacts = data['artifacts']
        context = data.get('context', 'Standard fraud investigation')
        priority = data.get('priority', 'standard')
        
        # Get user subscription
        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        if not subscription:
            return jsonify({"error": "No active subscription found"}), 404
        
        # Determine investigation parameters based on subscription
        subscription_tier = SubscriptionTier(subscription.tier)
        investigation_type = InvestigationType.COMPREHENSIVE_INVESTIGATION
        analysis_depth = _get_analysis_depth_from_tier(subscription_tier)
        
        # Calculate credit cost
        try:
            priority_enum = ProcessingPriority(priority)
        except ValueError:
            priority_enum = ProcessingPriority.STANDARD
        
        complexity = CreditCalculator.get_complexity_from_tier(subscription_tier)
        ai_model_tier = CreditCalculator.get_tier_ai_models(subscription_tier)
        
        credit_cost = CreditCalculator.calculate_investigation_cost(
            operation_type='comprehensive_investigation',
            complexity=complexity,
            ai_model_tier=ai_model_tier,
            artifact_count=len(artifacts),
            priority=priority_enum
        )
        
        # Check if user can afford the investigation
        if not subscription.can_afford(credit_cost):
            return jsonify({
                "error": "Insufficient credits",
                "required_credits": credit_cost,
                "available_credits": subscription.total_credits,
                "upgrade_url": "/api/credit/plans"
            }), 402  # Payment Required
        
        # Generate investigation ID
        investigation_id = str(uuid.uuid4())
        
        # Create investigation request with enhanced prompts
        investigation_request = InvestigationRequest(
            investigation_id=investigation_id,
            user_id=user_id,
            tier=ModelTier(subscription_tier.value),
            investigation_type=investigation_type,
            artifacts=artifacts,
            context=context,
            priority=priority
        )
        
        # Consume credits before starting investigation
        success = subscription.consume_credits(
            credit_cost,
            f"Investigation {investigation_id} - {investigation_type.value}"
        )
        
        if not success:
            return jsonify({"error": "Failed to consume credits"}), 500
        
        # Update transaction with investigation ID
        latest_transaction = CreditTransaction.query.filter_by(
            subscription_id=subscription.id,
            user_id=user_id
        ).order_by(CreditTransaction.created_at.desc()).first()
        
        if latest_transaction:
            latest_transaction.investigation_id = investigation_id
        
        user_db.session.commit()
        
        # Start investigation (async)
        result = await investigation_engine.conduct_investigation(investigation_request)
        
        # Store investigation in database
        investigation = Investigation(
            id=investigation_id,
            user_id=user_id,
            tier=subscription_tier.value,
            status='completed',
            artifacts_count=len(artifacts),
            threat_level=result.threat_level.value,
            confidence_score=result.confidence_score,
            processing_time=result.processing_time,
            cost=credit_cost,
            created_at=investigation_request.timestamp,
            completed_at=result.timestamp
        )
        
        user_db.session.add(investigation)
        
        # Generate comprehensive report
        report_tier = TIER_MAPPING.get(subscription_tier, ReportTier.BASIC)
        report_content, report_metadata = report_generator.generate_report(
            investigation_data=result.to_dict(),
            user_id=user_id,
            tier=report_tier,
            format=ReportFormat.JSON,
            investigation_id=investigation_id
        )
        
        # Create investigation report in database
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
        
        logger.info(f"Investigation {investigation_id} completed for user {user_id}")
        
        return jsonify({
            "investigation_id": investigation_id,
            "status": "completed",
            "credits_consumed": credit_cost,
            "remaining_credits": subscription.total_credits,
            "report_status": report_metadata.status.value,
            "result": result.to_dict(),
            "report_metadata": {
                "report_id": report_metadata.report_id,
                "tier": report_metadata.tier.value,
                "format": report_metadata.format.value,
                "requires_approval": report_metadata.status == ReportStatus.UNDER_REVIEW
            }
        })
        
    except Exception as e:
        # Refund credits if investigation fails
        if 'subscription' in locals() and 'credit_cost' in locals():
            subscription.add_credits(
                credit_cost,
                CreditTransactionType.REFUND,
                f"Investigation {investigation_id} failed - refund"
            )
            user_db.session.commit()
        
        logger.error(f"Investigation creation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/investigate/estimate', methods=['POST'])
def estimate_investigation_cost():
    """Estimate credit cost for an investigation"""
    try:
        data = request.get_json()
        
        user_id = data.get('user_id')
        artifact_count = data.get('artifact_count', 1)
        priority = data.get('priority', 'standard')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        # Get user subscription
        subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
        if not subscription:
            return jsonify({"error": "No active subscription found"}), 404
        
        # Calculate cost estimate
        subscription_tier = SubscriptionTier(subscription.tier)
        complexity = CreditCalculator.get_complexity_from_tier(subscription_tier)
        ai_model_tier = CreditCalculator.get_tier_ai_models(subscription_tier)
        
        try:
            priority_enum = ProcessingPriority(priority)
        except ValueError:
            priority_enum = ProcessingPriority.STANDARD
        
        estimated_cost = CreditCalculator.calculate_investigation_cost(
            operation_type='comprehensive_investigation',
            complexity=complexity,
            ai_model_tier=ai_model_tier,
            artifact_count=artifact_count,
            priority=priority_enum
        )
        
        can_afford = subscription.can_afford(estimated_cost)
        
        return jsonify({
            "estimated_cost": estimated_cost,
            "user_balance": subscription.total_credits,
            "can_afford": can_afford,
            "subscription_tier": subscription_tier.value,
            "analysis_depth": complexity.value,
            "ai_model_tier": ai_model_tier,
            "priority_multiplier": 1.0 if priority_enum == ProcessingPriority.STANDARD else 1.5 if priority_enum == ProcessingPriority.PRIORITY else 2.0,
            "breakdown": {
                "base_cost": CreditCalculator.OPERATION_COSTS.get('comprehensive_investigation', {}).get(complexity, {}).get(ai_model_tier, 100),
                "artifact_count": artifact_count,
                "priority": priority_enum.value
            }
        })
        
    except Exception as e:
        logger.error(f"Cost estimation failed: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/investigate/quick', methods=['POST'])
async def quick_investigation():
    """Perform quick investigation for basic tier"""
    try:
        data = request.get_json()
        
        if 'url' not in data and 'content' not in data:
            return jsonify({"error": "URL or content required"}), 400
        
        user_id = data.get('user_id', 'anonymous')
        
        # Create artifact from input
        if 'url' in data:
            artifact = {"type": "url", "content": data['url']}
        else:
            artifact = {"type": "text", "content": data['content']}
        
        # Create quick investigation request
        investigation_id = str(uuid.uuid4())
        investigation_request = InvestigationRequest(
            investigation_id=investigation_id,
            user_id=user_id,
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

# ============ REPORT GENERATION ENDPOINTS ============

@app.route('/api/reports/<investigation_id>')
def get_investigation_report(investigation_id):
    """Get formatted investigation report"""
    try:
        investigation = Investigation.query.filter_by(id=investigation_id).first()
        if not investigation:
            return jsonify({"error": "Investigation not found"}), 404
        
        report = Report.query.filter_by(investigation_id=investigation_id).first()
        if not report:
            return jsonify({"error": "Report not found"}), 404
        
        # Get user subscription to determine report tier
        subscription = Subscription.query.filter_by(user_id=investigation.user_id, status='active').first()
        if not subscription:
            report_tier = ReportTier.FREE
        else:
            subscription_tier = SubscriptionTier(subscription.tier)
            report_tier = TIER_MAPPING.get(subscription_tier, ReportTier.FREE)
        
        # Prepare investigation data for report
        investigation_data = {
            "executive_summary": report.executive_summary,
            "threat_level": investigation.threat_level,
            "confidence_score": investigation.confidence_score,
            "detailed_findings": json.loads(report.detailed_findings) if report.detailed_findings else {},
            "evidence_analysis": json.loads(report.evidence_analysis) if report.evidence_analysis else {},
            "recommendations": json.loads(report.recommendations) if report.recommendations else [],
            "models_used": json.loads(report.models_used) if report.models_used else [],
            "processing_time": investigation.processing_time,
            "artifacts_count": investigation.artifacts_count
        }
        
        # Generate formatted report
        report_content, report_metadata = report_generator.generate_report(
            investigation_data=investigation_data,
            user_id=investigation.user_id,
            tier=report_tier,
            format=ReportFormat.HTML,
            investigation_id=investigation_id
        )
        
        return report_content, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        logger.error(f"Failed to get report for investigation {investigation_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/reports/<investigation_id>/pdf')
def get_investigation_report_pdf(investigation_id):
    """Get PDF investigation report"""
    try:
        # Similar to HTML report but return PDF
        investigation = Investigation.query.filter_by(id=investigation_id).first()
        if not investigation:
            return jsonify({"error": "Investigation not found"}), 404
        
        report = Report.query.filter_by(investigation_id=investigation_id).first()
        if not report:
            return jsonify({"error": "Report not found"}), 404
        
        # Get user subscription to determine report tier
        subscription = Subscription.query.filter_by(user_id=investigation.user_id, status='active').first()
        if not subscription:
            report_tier = ReportTier.FREE
        else:
            subscription_tier = SubscriptionTier(subscription.tier)
            report_tier = TIER_MAPPING.get(subscription_tier, ReportTier.FREE)
        
        # Prepare investigation data
        investigation_data = {
            "executive_summary": report.executive_summary,
            "threat_level": investigation.threat_level,
            "confidence_score": investigation.confidence_score,
            "detailed_findings": json.loads(report.detailed_findings) if report.detailed_findings else {},
            "evidence_analysis": json.loads(report.evidence_analysis) if report.evidence_analysis else {},
            "recommendations": json.loads(report.recommendations) if report.recommendations else [],
            "models_used": json.loads(report.models_used) if report.models_used else [],
            "processing_time": investigation.processing_time,
            "artifacts_count": investigation.artifacts_count
        }
        
        # Generate PDF report
        pdf_content = report_generator.template_manager.generate_pdf_report(
            investigation_data, report_tier, 
            report_generator.ReportMetadata(
                report_id=str(uuid.uuid4()),
                investigation_id=investigation_id,
                user_id=investigation.user_id,
                tier=report_tier,
                format=ReportFormat.PDF,
                status=ReportStatus.PUBLISHED,
                generated_at=datetime.now(timezone.utc)
            )
        )
        
        return pdf_content, 200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': f'attachment; filename=scamshield_report_{investigation_id}.pdf'
        }
        
    except Exception as e:
        logger.error(f"Failed to generate PDF report for investigation {investigation_id}: {str(e)}")
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
        
        # Check file size limits based on user tier
        user_id = request.form.get('user_id')
        if user_id:
            subscription = Subscription.query.filter_by(user_id=user_id, status='active').first()
            if subscription:
                # Get plan limits (would be implemented with SubscriptionPlan model)
                max_file_size = 100 * 1024 * 1024  # Default 100MB
                if file_size > max_file_size:
                    return jsonify({"error": f"File too large. Maximum size: {max_file_size // (1024*1024)}MB"}), 413
        
        # Determine file type
        file_extension = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        
        # Create artifact object
        artifact = {
            "type": "document" if file_extension in ['pdf', 'doc', 'docx', 'txt'] else "image" if file_extension in ['jpg', 'jpeg', 'png', 'gif'] else "unknown",
            "filename": filename,
            "file_size": file_size,
            "file_type": file_extension,
            "content": base64.b64encode(file_content).decode('utf-8') if file_extension in ['jpg', 'jpeg', 'png', 'gif'] else file_content.decode('utf-8', errors='ignore'),
            "metadata": {
                "upload_timestamp": datetime.now(timezone.utc).isoformat(),
                "original_filename": file.filename
            }
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
        
        # Credit system statistics
        total_subscriptions = Subscription.query.filter_by(status='active').count()
        total_credits_consumed = user_db.session.query(
            user_db.func.sum(user_db.func.abs(CreditTransaction.amount))
        ).filter_by(transaction_type='consumption').scalar() or 0
        
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
            "credit_system": {
                "active_subscriptions": total_subscriptions,
                "total_credits_consumed": int(total_credits_consumed)
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

# ============ ADMIN ENDPOINTS ============

@app.route('/api/admin/reports/pending')
def get_pending_reports():
    """Get reports pending approval (admin function)"""
    try:
        # This would query reports with status 'under_review'
        # For now, return empty list
        return jsonify({
            "pending_reports": [],
            "count": 0
        })
        
    except Exception as e:
        logger.error(f"Failed to get pending reports: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/reports/<report_id>/approve', methods=['POST'])
def approve_report(report_id):
    """Approve a report for publication (admin function)"""
    try:
        data = request.get_json()
        approved_by = data.get('approved_by', 'admin')
        
        success = report_generator.approve_report(report_id, approved_by)
        
        if success:
            return jsonify({"message": "Report approved successfully"})
        else:
            return jsonify({"error": "Failed to approve report"}), 500
        
    except Exception as e:
        logger.error(f"Failed to approve report {report_id}: {str(e)}")
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

@app.errorhandler(402)
def payment_required(error):
    """Handle 402 Payment Required errors"""
    return jsonify({"error": "Insufficient credits", "upgrade_required": True}), 402

# ============ MAIN APPLICATION ============

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"Starting ScamShield AI Enhanced Backend on port {port}")
    logger.info(f"Debug mode: {debug}")
    logger.info("Features enabled:")
    logger.info("  - Elite AI Investigation Engine")
    logger.info("  - Credit-Based Pricing System")
    logger.info("  - Advanced Report Generation")
    logger.info("  - Multi-Tier Analysis Framework")
    logger.info("  - Legal Compliance Framework")
    
    app.run(host='0.0.0.0', port=port, debug=debug)

