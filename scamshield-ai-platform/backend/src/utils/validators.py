"""
ScamShield AI - Input Validation and Sanitization

Comprehensive validation and sanitization utilities for user input,
with security-focused approaches to prevent injection attacks.
"""

import re
import html
import urllib.parse
from typing import Any, Dict, List, Optional, Union
from email_validator import validate_email as email_validate, EmailNotValidError
import phonenumbers
from urllib.parse import urlparse
import ipaddress
import hashlib
import bleach

from .error_handler import ValidationError


class InputValidator:
    """Comprehensive input validation class"""
    
    # Common regex patterns
    PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^\+?1?-?\(?\d{3}\)?-?\d{3}-?\d{4}$',
        'url': r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:[\w.])*)?)?$',
        'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$',
        'username': r'^[a-zA-Z0-9_-]{3,30}$',
        'bitcoin_address': r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
        'ethereum_address': r'^0x[a-fA-F0-9]{40}$',
        'ip_address': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    }
    
    # Dangerous input patterns
    DANGEROUS_PATTERNS = {
        'sql_injection': [
            r"(\b(?:union|select|insert|update|delete|drop|create|alter|exec|execute)\b)",
            r"(--|#|/\*|\*/)",
            r"(\b(?:or|and)\s+\d+\s*=\s*\d+)",
            r"('\s*or\s*'[^']*'\s*=\s*'[^']*')"
        ],
        'xss': [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe[^>]*>.*?</iframe>",
            r"<object[^>]*>.*?</object>",
            r"<embed[^>]*>.*?</embed>"
        ],
        'path_traversal': [
            r"\.\./",
            r"\.\.\\",
            r"%2e%2e/",
            r"%2e%2e\\",
            r"\.\.%2f",
            r"\.\.%5c"
        ],
        'command_injection': [
            r"[;&|`$()]",
            r"\b(?:cat|ls|dir|type|copy|del|rm|mv|cp|chmod|chown|wget|curl)\b",
            r">\s*[^>\s]",
            r"<\s*[^<\s]"
        ]
    }
    
    @classmethod
    def validate_email(cls, email: str, check_deliverability: bool = False) -> str:
        """
        Validate email address format and optionally check deliverability
        
        Args:
            email: Email address to validate
            check_deliverability: Whether to check if email is deliverable
            
        Returns:
            Normalized email address
            
        Raises:
            ValidationError: If email is invalid
        """
        if not email or not isinstance(email, str):
            raise ValidationError("Email is required and must be a string", field="email")
        
        email = email.strip().lower()
        
        try:
            # Use email-validator library for comprehensive validation
            valid = email_validate(
                email,
                check_deliverability=check_deliverability
            )
            return valid.email
        except EmailNotValidError as e:
            raise ValidationError(f"Invalid email format: {str(e)}", field="email")
    
    @classmethod
    def validate_phone(cls, phone: str, country_code: str = "US") -> str:
        """
        Validate phone number format
        
        Args:
            phone: Phone number to validate
            country_code: Country code for validation (default: US)
            
        Returns:
            Formatted phone number
            
        Raises:
            ValidationError: If phone number is invalid
        """
        if not phone or not isinstance(phone, str):
            raise ValidationError("Phone number is required and must be a string", field="phone")
        
        try:
            # Parse phone number
            parsed = phonenumbers.parse(phone, country_code)
            
            # Validate phone number
            if not phonenumbers.is_valid_number(parsed):
                raise ValidationError("Invalid phone number", field="phone")
            
            # Format phone number
            return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        
        except phonenumbers.NumberParseException as e:
            raise ValidationError(f"Invalid phone number format: {str(e)}", field="phone")
    
    @classmethod
    def validate_url(cls, url: str, allowed_schemes: List[str] = None) -> str:
        """
        Validate URL format and security
        
        Args:
            url: URL to validate
            allowed_schemes: Allowed URL schemes (default: ['http', 'https'])
            
        Returns:
            Normalized URL
            
        Raises:
            ValidationError: If URL is invalid or unsafe
        """
        if not url or not isinstance(url, str):
            raise ValidationError("URL is required and must be a string", field="url")
        
        if allowed_schemes is None:
            allowed_schemes = ['http', 'https']
        
        url = url.strip()
        
        try:
            parsed = urlparse(url)
            
            # Check scheme
            if parsed.scheme not in allowed_schemes:
                raise ValidationError(
                    f"URL scheme must be one of: {', '.join(allowed_schemes)}", 
                    field="url"
                )
            
            # Check if hostname exists
            if not parsed.netloc:
                raise ValidationError("URL must include a valid hostname", field="url")
            
            # Security checks
            cls._check_url_security(parsed)
            
            return url
        
        except ValueError as e:
            raise ValidationError(f"Invalid URL format: {str(e)}", field="url")
    
    @classmethod
    def validate_uuid(cls, uuid_string: str) -> str:
        """
        Validate UUID format
        
        Args:
            uuid_string: UUID string to validate
            
        Returns:
            Normalized UUID string
            
        Raises:
            ValidationError: If UUID is invalid
        """
        if not uuid_string or not isinstance(uuid_string, str):
            raise ValidationError("UUID is required and must be a string", field="uuid")
        
        uuid_string = uuid_string.strip().lower()
        
        if not re.match(cls.PATTERNS['uuid'], uuid_string, re.IGNORECASE):
            raise ValidationError("Invalid UUID format", field="uuid")
        
        return uuid_string
    
    @classmethod
    def validate_username(cls, username: str) -> str:
        """
        Validate username format
        
        Args:
            username: Username to validate
            
        Returns:
            Validated username
            
        Raises:
            ValidationError: If username is invalid
        """
        if not username or not isinstance(username, str):
            raise ValidationError("Username is required and must be a string", field="username")
        
        username = username.strip()
        
        if not re.match(cls.PATTERNS['username'], username):
            raise ValidationError(
                "Username must be 3-30 characters, containing only letters, numbers, hyphens, and underscores",
                field="username"
            )
        
        # Check for reserved usernames
        reserved_usernames = [
            'admin', 'administrator', 'root', 'system', 'test', 'user',
            'api', 'www', 'mail', 'ftp', 'support', 'help', 'info',
            'scamshield', 'security', 'fraud', 'investigation'
        ]
        
        if username.lower() in reserved_usernames:
            raise ValidationError("Username is reserved and cannot be used", field="username")
        
        return username
    
    @classmethod
    def validate_password(cls, password: str) -> str:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            
        Returns:
            Validated password
            
        Raises:
            ValidationError: If password is weak
        """
        if not password or not isinstance(password, str):
            raise ValidationError("Password is required and must be a string", field="password")
        
        # Password strength requirements
        min_length = 8
        max_length = 128
        
        if len(password) < min_length:
            raise ValidationError(f"Password must be at least {min_length} characters long", field="password")
        
        if len(password) > max_length:
            raise ValidationError(f"Password must be no more than {max_length} characters long", field="password")
        
        # Check for required character types
        requirements = {
            'lowercase': r'[a-z]',
            'uppercase': r'[A-Z]',
            'digit': r'\d',
            'special': r'[!@#$%^&*(),.?":{}|<>]'
        }
        
        missing_requirements = []
        for req_name, pattern in requirements.items():
            if not re.search(pattern, password):
                missing_requirements.append(req_name)
        
        if missing_requirements:
            raise ValidationError(
                f"Password must contain: {', '.join(missing_requirements)}",
                field="password",
                details={"missing_requirements": missing_requirements}
            )
        
        # Check for common weak passwords
        weak_passwords = [
            'password', 'password123', '123456', '12345678', 'qwerty',
            'abc123', 'admin', 'letmein', 'welcome', 'monkey'
        ]
        
        if password.lower() in weak_passwords:
            raise ValidationError("Password is too common and easily guessable", field="password")
        
        return password
    
    @classmethod
    def validate_cryptocurrency_address(cls, address: str, crypto_type: str = "bitcoin") -> str:
        """
        Validate cryptocurrency address
        
        Args:
            address: Cryptocurrency address to validate
            crypto_type: Type of cryptocurrency (bitcoin, ethereum)
            
        Returns:
            Validated address
            
        Raises:
            ValidationError: If address is invalid
        """
        if not address or not isinstance(address, str):
            raise ValidationError("Cryptocurrency address is required and must be a string", field="crypto_address")
        
        address = address.strip()
        
        if crypto_type.lower() == "bitcoin":
            if not re.match(cls.PATTERNS['bitcoin_address'], address):
                raise ValidationError("Invalid Bitcoin address format", field="crypto_address")
        elif crypto_type.lower() == "ethereum":
            if not re.match(cls.PATTERNS['ethereum_address'], address):
                raise ValidationError("Invalid Ethereum address format", field="crypto_address")
        else:
            raise ValidationError(f"Unsupported cryptocurrency type: {crypto_type}", field="crypto_address")
        
        return address
    
    @classmethod
    def validate_ip_address(cls, ip: str) -> str:
        """
        Validate IP address format
        
        Args:
            ip: IP address to validate
            
        Returns:
            Validated IP address
            
        Raises:
            ValidationError: If IP address is invalid
        """
        if not ip or not isinstance(ip, str):
            raise ValidationError("IP address is required and must be a string", field="ip_address")
        
        ip = ip.strip()
        
        try:
            # Validate IPv4 or IPv6
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            raise ValidationError("Invalid IP address format", field="ip_address")
    
    @classmethod
    def check_dangerous_input(cls, input_text: str, input_type: str = "general") -> None:
        """
        Check input for dangerous patterns
        
        Args:
            input_text: Text to check
            input_type: Type of input (general, url, filename, etc.)
            
        Raises:
            ValidationError: If dangerous patterns are detected
        """
        if not input_text or not isinstance(input_text, str):
            return
        
        input_lower = input_text.lower()
        
        # Check all dangerous patterns
        for category, patterns in cls.DANGEROUS_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, input_lower, re.IGNORECASE):
                    raise ValidationError(
                        f"Input contains potentially dangerous content",
                        field="input",
                        details={"category": category, "detected_pattern": pattern}
                    )
    
    @classmethod
    def _check_url_security(cls, parsed_url) -> None:
        """
        Check URL for security issues
        
        Args:
            parsed_url: Parsed URL object
            
        Raises:
            ValidationError: If URL is unsafe
        """
        hostname = parsed_url.hostname
        
        if not hostname:
            raise ValidationError("URL must have a valid hostname", field="url")
        
        # Check for private/local IP addresses
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local:
                raise ValidationError("URLs pointing to private/local addresses are not allowed", field="url")
        except ValueError:
            # Not an IP address, continue with hostname checks
            pass
        
        # Check for dangerous domains
        dangerous_domains = [
            'localhost', '127.0.0.1', '0.0.0.0', '::1',
            '10.', '172.16.', '192.168.'
        ]
        
        for dangerous in dangerous_domains:
            if hostname.startswith(dangerous):
                raise ValidationError("URLs pointing to private/local addresses are not allowed", field="url")
        
        # Check for suspicious patterns in URL
        suspicious_patterns = [
            r'[<>"\']',  # HTML/JS injection attempts
            r'\.\./',    # Path traversal
            r'%[0-9a-f]{2}.*%[0-9a-f]{2}',  # Multiple URL encoding
        ]
        
        full_url = parsed_url.geturl()
        for pattern in suspicious_patterns:
            if re.search(pattern, full_url, re.IGNORECASE):
                raise ValidationError("URL contains suspicious patterns", field="url")


def sanitize_input(
    input_data: Union[str, Dict, List],
    allowed_tags: List[str] = None,
    allowed_attributes: Dict[str, List[str]] = None,
    max_length: Optional[int] = None
) -> Union[str, Dict, List]:
    """
    Sanitize input data to prevent XSS and other injection attacks
    
    Args:
        input_data: Data to sanitize
        allowed_tags: HTML tags to allow (default: none)
        allowed_attributes: HTML attributes to allow per tag
        max_length: Maximum length for string inputs
        
    Returns:
        Sanitized data
    """
    if allowed_tags is None:
        allowed_tags = []
    
    if allowed_attributes is None:
        allowed_attributes = {}
    
    def _sanitize_string(text: str) -> str:
        if not isinstance(text, str):
            return text
        
        # Check length
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        # Check for dangerous patterns
        InputValidator.check_dangerous_input(text)
        
        # HTML sanitization
        text = bleach.clean(
            text,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
        
        # Additional escaping
        text = html.escape(text, quote=True)
        
        return text.strip()
    
    def _sanitize_recursive(data):
        if isinstance(data, str):
            return _sanitize_string(data)
        elif isinstance(data, dict):
            return {key: _sanitize_recursive(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [_sanitize_recursive(item) for item in data]
        else:
            return data
    
    return _sanitize_recursive(input_data)


def validate_file_upload(
    filename: str,
    content: bytes,
    allowed_extensions: List[str] = None,
    max_size: int = 10 * 1024 * 1024,  # 10MB
    scan_for_malware: bool = True
) -> Dict[str, Any]:
    """
    Validate file upload for security
    
    Args:
        filename: Original filename
        content: File content
        allowed_extensions: Allowed file extensions
        max_size: Maximum file size in bytes
        scan_for_malware: Whether to scan for malware patterns
        
    Returns:
        Validation result dictionary
        
    Raises:
        ValidationError: If file is invalid or unsafe
    """
    if allowed_extensions is None:
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf', '.txt', '.csv', '.json']
    
    # Sanitize filename
    safe_filename = sanitize_filename(filename)
    
    # Check file extension
    file_ext = safe_filename.lower().split('.')[-1] if '.' in safe_filename else ''
    if f'.{file_ext}' not in allowed_extensions:
        raise ValidationError(
            f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}",
            field="file"
        )
    
    # Check file size
    if len(content) > max_size:
        raise ValidationError(
            f"File too large. Maximum size: {max_size / 1024 / 1024:.1f}MB",
            field="file"
        )
    
    # Check for empty file
    if len(content) == 0:
        raise ValidationError("File is empty", field="file")
    
    # Basic malware scanning
    if scan_for_malware:
        malware_signatures = [
            b'<script',
            b'javascript:',
            b'<?php',
            b'<%',
            b'#!/bin/',
            b'cmd.exe',
            b'powershell'
        ]
        
        content_lower = content.lower()
        for signature in malware_signatures:
            if signature in content_lower:
                raise ValidationError("File contains suspicious content", field="file")
    
    # Generate file hash for integrity
    file_hash = hashlib.sha256(content).hexdigest()
    
    return {
        "safe_filename": safe_filename,
        "file_extension": file_ext,
        "file_size": len(content),
        "file_hash": file_hash,
        "validation_passed": True
    }


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename for safe storage
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    if not filename:
        return "unknown_file"
    
    # Remove path components
    filename = filename.split('/')[-1].split('\\')[-1]
    
    # Remove dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    filename = ''.join(char for char in filename if ord(char) >= 32)
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + '.' + ext if ext else name[:255]
    
    # Ensure it's not empty
    if not filename or filename == '.':
        filename = "unknown_file"
    
    return filename


# Convenience functions
def validate_email(email: str, check_deliverability: bool = False) -> str:
    """Convenience function for email validation"""
    return InputValidator.validate_email(email, check_deliverability)


def validate_phone(phone: str, country_code: str = "US") -> str:
    """Convenience function for phone validation"""
    return InputValidator.validate_phone(phone, country_code)


def validate_url(url: str, allowed_schemes: List[str] = None) -> str:
    """Convenience function for URL validation"""
    return InputValidator.validate_url(url, allowed_schemes)


def validate_uuid(uuid_string: str) -> str:
    """Convenience function for UUID validation"""
    return InputValidator.validate_uuid(uuid_string)


def validate_username(username: str) -> str:
    """Convenience function for username validation"""
    return InputValidator.validate_username(username)


def validate_password(password: str) -> str:
    """Convenience function for password validation"""
    return InputValidator.validate_password(password)
