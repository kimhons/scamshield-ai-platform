"""
ScamShield AI - Enhanced Error Handling

Comprehensive error handling system with detailed logging, user-friendly messages,
and security-aware error responses.
"""

import logging
import traceback
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Union
from enum import Enum
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
import uuid

logger = logging.getLogger(__name__)

class ErrorType(Enum):
    """Error type enumeration"""
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    AUTHORIZATION = "authorization"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    RATE_LIMIT = "rate_limit"
    INTERNAL = "internal"
    EXTERNAL_API = "external_api"
    SECURITY = "security"
    BUSINESS_LOGIC = "business_logic"

class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class APIError(Exception):
    """Base API Error class with enhanced details"""
    
    def __init__(
        self,
        message: str,
        error_type: ErrorType = ErrorType.INTERNAL,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        user_message: Optional[str] = None,
        error_code: Optional[str] = None,
        suggestion: Optional[str] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_type = error_type
        self.status_code = status_code
        self.details = details or {}
        self.severity = severity
        self.user_message = user_message or self._get_user_friendly_message()
        self.error_code = error_code or self._generate_error_code()
        self.suggestion = suggestion
        self.timestamp = datetime.now(timezone.utc)
        self.error_id = str(uuid.uuid4())
    
    def _get_user_friendly_message(self) -> str:
        """Generate user-friendly error messages"""
        friendly_messages = {
            ErrorType.VALIDATION: "Please check your input and try again.",
            ErrorType.AUTHENTICATION: "Please log in to continue.",
            ErrorType.AUTHORIZATION: "You don't have permission to perform this action.",
            ErrorType.NOT_FOUND: "The requested resource was not found.",
            ErrorType.CONFLICT: "This action conflicts with existing data.",
            ErrorType.RATE_LIMIT: "Too many requests. Please try again later.",
            ErrorType.INTERNAL: "An unexpected error occurred. Please try again.",
            ErrorType.EXTERNAL_API: "External service is temporarily unavailable.",
            ErrorType.SECURITY: "Security validation failed.",
            ErrorType.BUSINESS_LOGIC: "This action cannot be completed as requested."
        }
        return friendly_messages.get(self.error_type, "An error occurred.")
    
    def _generate_error_code(self) -> str:
        """Generate error code for tracking"""
        return f"ERR_{self.error_type.value.upper()}_{self.status_code}"
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert error to dictionary representation"""
        error_dict = {
            "error": {
                "code": self.error_code,
                "type": self.error_type.value,
                "message": self.user_message,
                "severity": self.severity.value,
                "timestamp": self.timestamp.isoformat(),
                "error_id": self.error_id
            }
        }
        
        if self.suggestion:
            error_dict["error"]["suggestion"] = self.suggestion
        
        if include_sensitive:
            error_dict["error"]["technical_message"] = self.message
            error_dict["error"]["details"] = self.details
        
        return error_dict

class ValidationError(APIError):
    """Validation error for input validation failures"""
    
    def __init__(self, message: str, field: str = None, details: Dict[str, Any] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.VALIDATION,
            status_code=400,
            details=details,
            severity=ErrorSeverity.LOW
        )
        if field:
            self.details["field"] = field

class SecurityError(APIError):
    """Security-related errors"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(
            message=message,
            error_type=ErrorType.SECURITY,
            status_code=403,
            details=details,
            severity=ErrorSeverity.HIGH,
            user_message="Access denied for security reasons."
        )

class BusinessLogicError(APIError):
    """Business logic errors"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None, suggestion: str = None):
        super().__init__(
            message=message,
            error_type=ErrorType.BUSINESS_LOGIC,
            status_code=422,
            details=details,
            severity=ErrorSeverity.MEDIUM,
            suggestion=suggestion
        )

class ExternalAPIError(APIError):
    """External API errors"""
    
    def __init__(self, service: str, message: str, details: Dict[str, Any] = None):
        super().__init__(
            message=f"{service}: {message}",
            error_type=ErrorType.EXTERNAL_API,
            status_code=503,
            details=details,
            severity=ErrorSeverity.HIGH,
            user_message=f"The {service} service is temporarily unavailable. Please try again later."
        )

class ErrorHandler:
    """Enhanced error handling and logging system"""
    
    def __init__(self, app: Flask = None):
        self.app = app
        self.error_counts = {}
        self.critical_errors = []
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize error handler with Flask app"""
        self.app = app
        app.errorhandler(APIError)(self.handle_api_error)
        app.errorhandler(HTTPException)(self.handle_http_error)
        app.errorhandler(Exception)(self.handle_generic_error)
    
    def handle_api_error(self, error: APIError):
        """Handle custom API errors"""
        self._log_error(error)
        self._track_error(error)
        
        # Determine if sensitive info should be included
        include_sensitive = self.app.config.get('DEBUG', False)
        
        response = jsonify(error.to_dict(include_sensitive=include_sensitive))
        response.status_code = error.status_code
        
        # Add security headers
        self._add_security_headers(response)
        
        return response
    
    def handle_http_error(self, error: HTTPException):
        """Handle standard HTTP errors"""
        api_error = APIError(
            message=error.description or str(error),
            error_type=self._map_http_error_type(error.code),
            status_code=error.code,
            severity=self._get_severity_for_http_code(error.code)
        )
        
        return self.handle_api_error(api_error)
    
    def handle_generic_error(self, error: Exception):
        """Handle unexpected errors"""
        # Log full traceback for debugging
        logger.exception("Unhandled exception occurred")
        
        # Create API error
        api_error = APIError(
            message=str(error),
            error_type=ErrorType.INTERNAL,
            status_code=500,
            severity=ErrorSeverity.CRITICAL,
            details={"exception_type": type(error).__name__}
        )
        
        # Track critical error
        self._track_critical_error(error)
        
        return self.handle_api_error(api_error)
    
    def _log_error(self, error: APIError):
        """Enhanced error logging"""
        log_data = {
            "error_id": error.error_id,
            "error_type": error.error_type.value,
            "error_code": error.error_code,
            "severity": error.severity.value,
            "status_code": error.status_code,
            "message": error.message,
            "user_message": error.user_message,
            "timestamp": error.timestamp.isoformat(),
            "details": error.details
        }
        
        # Add request context if available
        if request:
            log_data.update({
                "request_id": getattr(request, 'id', None),
                "method": request.method,
                "url": request.url,
                "user_agent": request.headers.get('User-Agent'),
                "ip_address": self._get_client_ip(),
                "user_id": getattr(request, 'user_id', None)
            })
        
        # Log based on severity
        if error.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]:
            logger.error("Error occurred", extra=log_data)
        else:
            logger.warning("Error occurred", extra=log_data)
        
        # Additional logging for critical errors
        if error.severity == ErrorSeverity.CRITICAL:
            logger.critical(f"CRITICAL ERROR: {error.message}", extra=log_data)
    
    def _track_error(self, error: APIError):
        """Track error statistics"""
        error_key = f"{error.error_type.value}_{error.status_code}"
        self.error_counts[error_key] = self.error_counts.get(error_key, 0) + 1
        
        # Track critical errors separately
        if error.severity == ErrorSeverity.CRITICAL:
            self.critical_errors.append({
                "error_id": error.error_id,
                "timestamp": error.timestamp,
                "error_type": error.error_type.value,
                "message": error.message
            })
            
            # Keep only last 100 critical errors
            if len(self.critical_errors) > 100:
                self.critical_errors = self.critical_errors[-100:]
    
    def _track_critical_error(self, error: Exception):
        """Track critical system errors"""
        critical_error_data = {
            "error_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc),
            "exception_type": type(error).__name__,
            "message": str(error),
            "traceback": traceback.format_exception(type(error), error, error.__traceback__)
        }
        
        self.critical_errors.append(critical_error_data)
        
        # Alert mechanisms could be added here
        self._alert_critical_error(critical_error_data)
    
    def _alert_critical_error(self, error_data: Dict[str, Any]):
        """Alert mechanisms for critical errors"""
        # This could integrate with monitoring services like Sentry, DataDog, etc.
        logger.critical(f"SYSTEM CRITICAL ERROR: {error_data['message']}")
        
        # In production, you might want to:
        # - Send alerts to Slack/Teams
        # - Create tickets in JIRA
        # - Send emails to dev team
        # - Push to monitoring dashboards
    
    def _get_client_ip(self) -> str:
        """Get client IP address safely"""
        if not request:
            return "unknown"
        
        # Check for forwarded headers (behind proxy)
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()
        
        real_ip = request.headers.get('X-Real-IP')
        if real_ip:
            return real_ip
        
        return request.remote_addr or "unknown"
    
    def _map_http_error_type(self, status_code: int) -> ErrorType:
        """Map HTTP status codes to error types"""
        mapping = {
            400: ErrorType.VALIDATION,
            401: ErrorType.AUTHENTICATION,
            403: ErrorType.AUTHORIZATION,
            404: ErrorType.NOT_FOUND,
            409: ErrorType.CONFLICT,
            429: ErrorType.RATE_LIMIT,
            500: ErrorType.INTERNAL,
            502: ErrorType.EXTERNAL_API,
            503: ErrorType.EXTERNAL_API,
            504: ErrorType.EXTERNAL_API
        }
        return mapping.get(status_code, ErrorType.INTERNAL)
    
    def _get_severity_for_http_code(self, status_code: int) -> ErrorSeverity:
        """Get severity level for HTTP status codes"""
        if status_code >= 500:
            return ErrorSeverity.HIGH
        elif status_code >= 400:
            return ErrorSeverity.MEDIUM
        else:
            return ErrorSeverity.LOW
    
    def _add_security_headers(self, response):
        """Add security headers to error responses"""
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics for monitoring"""
        return {
            "error_counts": self.error_counts,
            "critical_errors_count": len(self.critical_errors),
            "recent_critical_errors": self.critical_errors[-10:] if self.critical_errors else []
        }
    
    def reset_statistics(self):
        """Reset error statistics"""
        self.error_counts.clear()
        self.critical_errors.clear()

# Utility functions for common error scenarios
def validate_required_fields(data: Dict[str, Any], required_fields: List[str]) -> None:
    """Validate that required fields are present and not empty"""
    missing_fields = []
    empty_fields = []
    
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
        elif not data[field] or (isinstance(data[field], str) and not data[field].strip()):
            empty_fields.append(field)
    
    if missing_fields:
        raise ValidationError(
            f"Missing required fields: {', '.join(missing_fields)}",
            details={"missing_fields": missing_fields}
        )
    
    if empty_fields:
        raise ValidationError(
            f"Empty required fields: {', '.join(empty_fields)}",
            details={"empty_fields": empty_fields}
        )

def handle_database_error(error: Exception, operation: str) -> None:
    """Handle database-related errors"""
    error_message = str(error).lower()
    
    if "duplicate" in error_message or "unique constraint" in error_message:
        raise APIError(
            message=f"Database constraint violation during {operation}",
            error_type=ErrorType.CONFLICT,
            status_code=409,
            user_message="This data already exists.",
            suggestion="Please check for existing records or use different values."
        )
    elif "foreign key" in error_message:
        raise APIError(
            message=f"Foreign key constraint violation during {operation}",
            error_type=ErrorType.VALIDATION,
            status_code=400,
            user_message="Referenced data does not exist.",
            suggestion="Please ensure all referenced data exists before proceeding."
        )
    elif "connection" in error_message:
        raise APIError(
            message=f"Database connection error during {operation}",
            error_type=ErrorType.INTERNAL,
            status_code=503,
            severity=ErrorSeverity.HIGH,
            user_message="Database service temporarily unavailable.",
            suggestion="Please try again in a few moments."
        )
    else:
        raise APIError(
            message=f"Database error during {operation}: {str(error)}",
            error_type=ErrorType.INTERNAL,
            status_code=500,
            severity=ErrorSeverity.HIGH
        )

def handle_ai_model_error(error: Exception, model_name: str) -> None:
    """Handle AI model-related errors"""
    error_message = str(error).lower()
    
    if "rate limit" in error_message or "quota" in error_message:
        raise ExternalAPIError(
            service=f"AI Model ({model_name})",
            message="Rate limit exceeded",
            details={"model": model_name, "error_type": "rate_limit"}
        )
    elif "timeout" in error_message:
        raise ExternalAPIError(
            service=f"AI Model ({model_name})",
            message="Request timeout",
            details={"model": model_name, "error_type": "timeout"}
        )
    elif "authentication" in error_message or "api key" in error_message:
        raise APIError(
            message=f"AI model authentication error: {model_name}",
            error_type=ErrorType.INTERNAL,
            status_code=503,
            severity=ErrorSeverity.CRITICAL,
            user_message="AI service temporarily unavailable."
        )
    else:
        raise ExternalAPIError(
            service=f"AI Model ({model_name})",
            message=str(error),
            details={"model": model_name, "error_type": "unknown"}
        )

# Context manager for error handling
class ErrorContext:
    """Context manager for enhanced error handling"""
    
    def __init__(self, operation: str, user_id: str = None, details: Dict[str, Any] = None):
        self.operation = operation
        self.user_id = user_id
        self.details = details or {}
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now(timezone.utc)
        logger.info(f"Starting operation: {self.operation}", extra={
            "operation": self.operation,
            "user_id": self.user_id,
            "details": self.details
        })
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        duration = (datetime.now(timezone.utc) - self.start_time).total_seconds()
        
        if exc_type is None:
            logger.info(f"Operation completed: {self.operation}", extra={
                "operation": self.operation,
                "user_id": self.user_id,
                "duration": duration,
                "status": "success"
            })
        else:
            logger.error(f"Operation failed: {self.operation}", extra={
                "operation": self.operation,
                "user_id": self.user_id,
                "duration": duration,
                "status": "failed",
                "error_type": exc_type.__name__,
                "error_message": str(exc_value)
            })
        
        return False  # Don't suppress exceptions
