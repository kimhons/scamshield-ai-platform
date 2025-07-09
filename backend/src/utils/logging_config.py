"""
ScamShield AI - Enhanced Logging Configuration

Comprehensive logging system with structured logging, security considerations,
and monitoring integration.
"""

import logging
import logging.handlers
import json
import os
import sys
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pathlib import Path
import uuid


class StructuredFormatter(logging.Formatter):
    """Structured JSON formatter for logs"""
    
    def __init__(self, include_request_id: bool = True):
        super().__init__()
        self.include_request_id = include_request_id
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as structured JSON"""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields from record
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname',
                          'filename', 'module', 'lineno', 'funcName', 'created',
                          'msecs', 'relativeCreated', 'thread', 'threadName',
                          'processName', 'process', 'exc_info', 'exc_text', 'stack_info']:
                log_data[key] = value
        
        # Add request ID if available
        if self.include_request_id:
            try:
                from flask import request, g
                if request and hasattr(g, 'request_id'):
                    log_data["request_id"] = g.request_id
            except (ImportError, RuntimeError):
                pass  # Not in Flask context
        
        return json.dumps(log_data, default=str, ensure_ascii=False)


class SecurityFilter(logging.Filter):
    """Filter sensitive information from logs"""
    
    SENSITIVE_PATTERNS = [
        'password', 'passwd', 'pwd', 'secret', 'token', 'key', 'auth',
        'credential', 'api_key', 'access_token', 'refresh_token',
        'private_key', 'certificate', 'ssn', 'social_security',
        'credit_card', 'card_number', 'cvv', 'pin'
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out or sanitize sensitive information"""
        # Sanitize the log message
        record.msg = self._sanitize_message(str(record.msg))
        
        # Sanitize extra fields
        for key, value in record.__dict__.items():
            if isinstance(value, (str, dict)):
                record.__dict__[key] = self._sanitize_data(value)
        
        return True
    
    def _sanitize_message(self, message: str) -> str:
        """Sanitize sensitive information in log messages"""
        import re
        
        # Pattern for potential sensitive data
        patterns = [
            # API keys and tokens
            (r'(["\']?(?:api[_-]?key|token|secret)["\']?\s*[:=]\s*["\']?)([^"\'\s]{8,})', r'\1***REDACTED***'),
            # Passwords
            (r'(["\']?password["\']?\s*[:=]\s*["\']?)([^"\'\s]{3,})', r'\1***REDACTED***'),
            # Email addresses (partial redaction)
            (r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'\1@***REDACTED***'),
            # Credit card numbers
            (r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', '***CARD_NUMBER_REDACTED***'),
            # Social security numbers
            (r'\b\d{3}[- ]?\d{2}[- ]?\d{4}\b', '***SSN_REDACTED***'),
        ]
        
        for pattern, replacement in patterns:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)
        
        return message
    
    def _sanitize_data(self, data) -> Any:
        """Recursively sanitize data structures"""
        if isinstance(data, str):
            return self._sanitize_message(data)
        elif isinstance(data, dict):
            return {key: self._sanitize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self._sanitize_data(item) for item in data]
        else:
            return data


class PerformanceFilter(logging.Filter):
    """Filter to add performance metrics to logs"""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Add performance metrics to log records"""
        import psutil
        import time
        
        # Add system metrics
        record.cpu_percent = psutil.cpu_percent()
        record.memory_percent = psutil.virtual_memory().percent
        
        # Add process metrics
        try:
            process = psutil.Process()
            record.process_memory_mb = process.memory_info().rss / 1024 / 1024
            record.process_cpu_percent = process.cpu_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        
        return True


def setup_logging(
    app_name: str = "scamshield_ai",
    log_level: str = "INFO",
    log_dir: Optional[str] = None,
    enable_console: bool = True,
    enable_file: bool = True,
    enable_structured: bool = True,
    enable_security_filter: bool = True,
    enable_performance_filter: bool = False,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 10
) -> logging.Logger:
    """
    Setup comprehensive logging configuration
    
    Args:
        app_name: Application name for log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (default: ./logs)
        enable_console: Enable console logging
        enable_file: Enable file logging
        enable_structured: Use structured JSON formatting
        enable_security_filter: Enable security filtering
        enable_performance_filter: Enable performance metrics
        max_file_size: Maximum size for log files before rotation
        backup_count: Number of backup files to keep
    
    Returns:
        Configured logger instance
    """
    # Create log directory
    if log_dir is None:
        log_dir = os.path.join(os.getcwd(), "logs")
    
    Path(log_dir).mkdir(exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    if enable_structured:
        formatter = StructuredFormatter()
        console_formatter = StructuredFormatter(include_request_id=False)
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = formatter
    
    # Setup filters
    filters = []
    
    if enable_security_filter:
        filters.append(SecurityFilter())
    
    if enable_performance_filter:
        filters.append(PerformanceFilter())
    
    # Console handler
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(console_formatter)
        
        for filter_obj in filters:
            console_handler.addFilter(filter_obj)
        
        root_logger.addHandler(console_handler)
    
    # File handlers
    if enable_file:
        # Main log file
        main_log_file = os.path.join(log_dir, f"{app_name}.log")
        file_handler = logging.handlers.RotatingFileHandler(
            main_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        for filter_obj in filters:
            file_handler.addFilter(filter_obj)
        
        root_logger.addHandler(file_handler)
        
        # Error log file (ERROR and CRITICAL only)
        error_log_file = os.path.join(log_dir, f"{app_name}_errors.log")
        error_handler = logging.handlers.RotatingFileHandler(
            error_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        
        for filter_obj in filters:
            error_handler.addFilter(filter_obj)
        
        root_logger.addHandler(error_handler)
        
        # Security log file (for security-related events)
        security_log_file = os.path.join(log_dir, f"{app_name}_security.log")
        security_handler = logging.handlers.RotatingFileHandler(
            security_log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        security_handler.setLevel(logging.WARNING)
        security_handler.setFormatter(formatter)
        security_handler.addFilter(SecurityLogFilter())
        
        root_logger.addHandler(security_handler)
    
    # Setup specific loggers
    setup_specific_loggers(log_level)
    
    # Log startup message
    logger = get_logger(__name__)
    logger.info(f"Logging initialized for {app_name}", extra={
        "log_level": log_level,
        "log_dir": log_dir,
        "structured_logging": enable_structured,
        "security_filtering": enable_security_filter
    })
    
    return root_logger


def setup_specific_loggers(log_level: str):
    """Setup specific loggers for different components"""
    
    # Database logger
    db_logger = logging.getLogger('sqlalchemy.engine')
    db_logger.setLevel(logging.WARNING)  # Reduce DB query noise
    
    # HTTP request logger
    request_logger = logging.getLogger('werkzeug')
    request_logger.setLevel(logging.WARNING)  # Reduce HTTP noise
    
    # AI Engine logger
    ai_logger = logging.getLogger('ai_engine')
    ai_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Security logger
    security_logger = logging.getLogger('security')
    security_logger.setLevel(logging.WARNING)
    
    # Investigation logger
    investigation_logger = logging.getLogger('investigation')
    investigation_logger.setLevel(getattr(logging, log_level.upper()))


class SecurityLogFilter(logging.Filter):
    """Filter for security-related log events"""
    
    SECURITY_KEYWORDS = [
        'security', 'auth', 'login', 'logout', 'access_denied',
        'unauthorized', 'forbidden', 'rate_limit', 'suspicious',
        'attack', 'breach', 'violation', 'failed_login'
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Only allow security-related logs"""
        message = record.getMessage().lower()
        return any(keyword in message for keyword in self.SECURITY_KEYWORDS)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with security and performance enhancements"""
    logger = logging.getLogger(name)
    
    # Add custom log methods
    def log_security_event(message: str, **kwargs):
        """Log security-related events"""
        extra = {
            'event_type': 'security',
            'severity': 'high',
            **kwargs
        }
        logger.warning(f"SECURITY: {message}", extra=extra)
    
    def log_performance_metric(operation: str, duration: float, **kwargs):
        """Log performance metrics"""
        extra = {
            'event_type': 'performance',
            'operation': operation,
            'duration_ms': duration * 1000,
            **kwargs
        }
        logger.info(f"PERFORMANCE: {operation} completed in {duration:.3f}s", extra=extra)
    
    def log_business_event(event: str, user_id: str = None, **kwargs):
        """Log business-related events"""
        extra = {
            'event_type': 'business',
            'user_id': user_id,
            **kwargs
        }
        logger.info(f"BUSINESS: {event}", extra=extra)
    
    # Attach custom methods to logger
    logger.security = log_security_event
    logger.performance = log_performance_metric
    logger.business = log_business_event
    
    return logger


def log_request_middleware(app):
    """Middleware to log HTTP requests with security information"""
    
    @app.before_request
    def log_request_info():
        from flask import request, g
        import time
        
        # Generate request ID
        g.request_id = str(uuid.uuid4())
        g.request_start_time = time.time()
        
        logger = get_logger('request')
        
        # Log request details
        logger.info("Request received", extra={
            'request_id': g.request_id,
            'method': request.method,
            'url': request.url,
            'path': request.path,
            'user_agent': request.headers.get('User-Agent'),
            'ip_address': request.remote_addr,
            'content_length': request.content_length,
            'content_type': request.content_type
        })
        
        # Log security-relevant headers
        security_headers = [
            'X-Forwarded-For', 'X-Real-IP', 'X-Forwarded-Proto',
            'Authorization', 'Cookie', 'Origin', 'Referer'
        ]
        
        security_data = {}
        for header in security_headers:
            value = request.headers.get(header)
            if value:
                # Sanitize authorization headers
                if header.lower() == 'authorization':
                    security_data[header] = 'Bearer ***REDACTED***' if value.startswith('Bearer ') else '***REDACTED***'
                elif header.lower() == 'cookie':
                    security_data[header] = '***REDACTED***'
                else:
                    security_data[header] = value
        
        if security_data:
            logger.security("Request security headers", 
                          request_id=g.request_id, 
                          headers=security_data)
    
    @app.after_request
    def log_response_info(response):
        from flask import g
        import time
        
        logger = get_logger('request')
        
        # Calculate request duration
        duration = time.time() - getattr(g, 'request_start_time', time.time())
        
        # Log response details
        logger.info("Request completed", extra={
            'request_id': getattr(g, 'request_id', 'unknown'),
            'status_code': response.status_code,
            'content_length': response.content_length,
            'duration_ms': duration * 1000
        })
        
        # Log slow requests
        if duration > 5.0:  # Requests taking more than 5 seconds
            logger.warning("Slow request detected", extra={
                'request_id': getattr(g, 'request_id', 'unknown'),
                'duration_ms': duration * 1000,
                'threshold_ms': 5000
            })
        
        # Log errors
        if response.status_code >= 400:
            logger.warning("Request failed", extra={
                'request_id': getattr(g, 'request_id', 'unknown'),
                'status_code': response.status_code,
                'error_category': 'client_error' if response.status_code < 500 else 'server_error'
            })
        
        return response


def setup_monitoring_integration():
    """Setup integration with monitoring services"""
    
    # Example integration with external monitoring
    class MonitoringHandler(logging.Handler):
        """Custom handler for monitoring service integration"""
        
        def emit(self, record):
            if record.levelno >= logging.ERROR:
                # Send to monitoring service (e.g., Sentry, DataDog)
                self.send_to_monitoring(record)
        
        def send_to_monitoring(self, record):
            """Send log record to monitoring service"""
            # This would integrate with actual monitoring services
            # For now, just log to console for demonstration
            print(f"MONITORING ALERT: {record.getMessage()}")
    
    # Add monitoring handler to root logger
    monitoring_handler = MonitoringHandler()
    monitoring_handler.setLevel(logging.ERROR)
    
    root_logger = logging.getLogger()
    root_logger.addHandler(monitoring_handler)


# Context manager for operation logging
class LogOperation:
    """Context manager for logging operations with timing and outcome"""
    
    def __init__(self, operation: str, logger: logging.Logger = None, **kwargs):
        self.operation = operation
        self.logger = logger or get_logger(__name__)
        self.extra_data = kwargs
        self.start_time = None
    
    def __enter__(self):
        import time
        self.start_time = time.time()
        
        self.logger.info(f"Starting operation: {self.operation}", extra={
            'operation': self.operation,
            'status': 'started',
            **self.extra_data
        })
        
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        import time
        duration = time.time() - self.start_time
        
        if exc_type is None:
            self.logger.info(f"Operation completed: {self.operation}", extra={
                'operation': self.operation,
                'status': 'completed',
                'duration_ms': duration * 1000,
                **self.extra_data
            })
        else:
            self.logger.error(f"Operation failed: {self.operation}", extra={
                'operation': self.operation,
                'status': 'failed',
                'duration_ms': duration * 1000,
                'error_type': exc_type.__name__,
                'error_message': str(exc_value),
                **self.extra_data
            })
        
        return False  # Don't suppress exceptions
