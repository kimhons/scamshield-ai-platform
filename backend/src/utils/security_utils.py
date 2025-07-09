"""
ScamShield AI - Security Utilities

Comprehensive security utilities for authentication, encryption, and security checks.
"""

import hashlib
import hmac
import secrets
import base64
import os
import time
import jwt
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, Union, List, Tuple
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import bcrypt
import pyotp
import qrcode
from io import BytesIO

from .error_handler import SecurityError, ValidationError
from .logging_config import get_logger

logger = get_logger(__name__)


class PasswordSecurity:
    """Enhanced password security utilities"""
    
    @staticmethod
    def hash_password(password: str, rounds: int = 12) -> str:
        """
        Hash password using bcrypt with salt
        
        Args:
            password: Plain text password
            rounds: Number of bcrypt rounds (default: 12)
            
        Returns:
            Hashed password string
        """
        if not password:
            raise ValidationError("Password cannot be empty")
        
        # Generate salt and hash password
        salt = bcrypt.gensalt(rounds=rounds)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        logger.info("Password hashed successfully", extra={
            "rounds": rounds,
            "password_length": len(password)
        })
        
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        Verify password against hash
        
        Args:
            password: Plain text password
            hashed_password: Hashed password to verify against
            
        Returns:
            True if password matches, False otherwise
        """
        if not password or not hashed_password:
            return False
        
        try:
            result = bcrypt.checkpw(
                password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
            
            logger.security("Password verification attempt", 
                          success=result,
                          password_length=len(password))
            
            return result
        except Exception as e:
            logger.security("Password verification failed", 
                          error=str(e),
                          password_length=len(password))
            return False
    
    @staticmethod
    def generate_secure_password(
        length: int = 16,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_symbols: bool = True,
        exclude_ambiguous: bool = True
    ) -> str:
        """
        Generate a cryptographically secure password
        
        Args:
            length: Password length
            include_uppercase: Include uppercase letters
            include_lowercase: Include lowercase letters
            include_digits: Include digits
            include_symbols: Include symbols
            exclude_ambiguous: Exclude ambiguous characters (0, O, l, 1, etc.)
            
        Returns:
            Generated password
        """
        characters = ""
        
        if include_lowercase:
            chars = "abcdefghijklmnopqrstuvwxyz"
            if exclude_ambiguous:
                chars = chars.replace('l', '').replace('o', '')
            characters += chars
        
        if include_uppercase:
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            if exclude_ambiguous:
                chars = chars.replace('I', '').replace('O', '')
            characters += chars
        
        if include_digits:
            chars = "0123456789"
            if exclude_ambiguous:
                chars = chars.replace('0', '').replace('1', '')
            characters += chars
        
        if include_symbols:
            chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
            characters += chars
        
        if not characters:
            raise ValidationError("At least one character type must be included")
        
        # Ensure at least one character from each selected type
        password = []
        
        if include_lowercase:
            password.append(secrets.choice("abcdefghijklmnopqrstuvwxyz"))
        if include_uppercase:
            password.append(secrets.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
        if include_digits:
            password.append(secrets.choice("23456789"))  # Avoid ambiguous digits
        if include_symbols:
            password.append(secrets.choice("!@#$%^&*"))
        
        # Fill remaining length
        for _ in range(length - len(password)):
            password.append(secrets.choice(characters))
        
        # Shuffle password
        for i in range(len(password)):
            j = secrets.randbelow(len(password))
            password[i], password[j] = password[j], password[i]
        
        return ''.join(password)
    
    @staticmethod
    def check_password_strength(password: str) -> Dict[str, Any]:
        """
        Analyze password strength
        
        Args:
            password: Password to analyze
            
        Returns:
            Dictionary with strength analysis
        """
        if not password:
            return {"score": 0, "strength": "very_weak", "issues": ["Password is empty"]}
        
        score = 0
        issues = []
        requirements_met = []
        
        # Length check
        if len(password) >= 12:
            score += 25
            requirements_met.append("Adequate length (12+ characters)")
        elif len(password) >= 8:
            score += 15
            requirements_met.append("Minimum length (8+ characters)")
        else:
            issues.append("Password too short (minimum 8 characters)")
        
        # Character type checks
        if any(c.islower() for c in password):
            score += 10
            requirements_met.append("Contains lowercase letters")
        else:
            issues.append("Missing lowercase letters")
        
        if any(c.isupper() for c in password):
            score += 10
            requirements_met.append("Contains uppercase letters")
        else:
            issues.append("Missing uppercase letters")
        
        if any(c.isdigit() for c in password):
            score += 10
            requirements_met.append("Contains digits")
        else:
            issues.append("Missing digits")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 15
            requirements_met.append("Contains special characters")
        else:
            issues.append("Missing special characters")
        
        # Complexity bonuses
        unique_chars = len(set(password))
        if unique_chars >= len(password) * 0.8:
            score += 10
            requirements_met.append("High character diversity")
        
        # Pattern penalties
        if password.lower() in ["password", "123456", "qwerty", "admin"]:
            score -= 50
            issues.append("Common weak password")
        
        # Determine strength
        if score >= 80:
            strength = "very_strong"
        elif score >= 60:
            strength = "strong"
        elif score >= 40:
            strength = "moderate"
        elif score >= 20:
            strength = "weak"
        else:
            strength = "very_weak"
        
        return {
            "score": max(0, score),
            "strength": strength,
            "requirements_met": requirements_met,
            "issues": issues
        }


class TokenSecurity:
    """JWT and secure token utilities"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or os.environ.get('JWT_SECRET_KEY', self._generate_secret_key())
    
    def _generate_secret_key(self) -> str:
        """Generate a secure secret key"""
        return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8')
    
    def generate_jwt_token(
        self,
        payload: Dict[str, Any],
        expires_in: timedelta = timedelta(hours=24),
        algorithm: str = 'HS256'
    ) -> str:
        """
        Generate JWT token
        
        Args:
            payload: Token payload
            expires_in: Token expiration time
            algorithm: JWT algorithm
            
        Returns:
            JWT token string
        """
        now = datetime.now(timezone.utc)
        payload.update({
            'iat': now,
            'exp': now + expires_in,
            'jti': secrets.token_urlsafe(16)  # Unique token ID
        })
        
        token = jwt.encode(payload, self.secret_key, algorithm=algorithm)
        
        logger.security("JWT token generated", 
                       user_id=payload.get('user_id'),
                       expires_in=expires_in.total_seconds())
        
        return token
    
    def verify_jwt_token(self, token: str, algorithm: str = 'HS256') -> Dict[str, Any]:
        """
        Verify and decode JWT token
        
        Args:
            token: JWT token to verify
            algorithm: JWT algorithm
            
        Returns:
            Decoded payload
            
        Raises:
            SecurityError: If token is invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[algorithm])
            
            logger.security("JWT token verified successfully",
                           user_id=payload.get('user_id'),
                           token_id=payload.get('jti'))
            
            return payload
        
        except jwt.ExpiredSignatureError:
            logger.security("JWT token verification failed", reason="expired")
            raise SecurityError("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.security("JWT token verification failed", reason=str(e))
            raise SecurityError("Invalid token")
    
    def generate_api_key(self, length: int = 32) -> str:
        """
        Generate secure API key
        
        Args:
            length: Key length in bytes
            
        Returns:
            Base64-encoded API key
        """
        key = secrets.token_bytes(length)
        api_key = base64.urlsafe_b64encode(key).decode('utf-8')
        
        logger.security("API key generated", key_length=length)
        
        return api_key
    
    def generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def generate_csrf_token(self) -> str:
        """Generate CSRF protection token"""
        return secrets.token_urlsafe(24)


class TwoFactorAuth:
    """Two-Factor Authentication utilities"""
    
    @staticmethod
    def generate_totp_secret() -> str:
        """Generate TOTP secret for 2FA setup"""
        return pyotp.random_base32()
    
    @staticmethod
    def generate_qr_code(secret: str, user_email: str, issuer: str = "ScamShield AI") -> bytes:
        """
        Generate QR code for TOTP setup
        
        Args:
            secret: TOTP secret
            user_email: User's email address
            issuer: Service name
            
        Returns:
            QR code image bytes
        """
        totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
            name=user_email,
            issuer_name=issuer
        )
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(totp_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        img_buffer = BytesIO()
        img.save(img_buffer, format='PNG')
        
        return img_buffer.getvalue()
    
    @staticmethod
    def verify_totp_code(secret: str, code: str, window: int = 1) -> bool:
        """
        Verify TOTP code
        
        Args:
            secret: TOTP secret
            code: User-provided code
            window: Time window for code acceptance
            
        Returns:
            True if code is valid
        """
        if not secret or not code:
            return False
        
        totp = pyotp.TOTP(secret)
        result = totp.verify(code, valid_window=window)
        
        logger.security("TOTP verification attempt", 
                       success=result,
                       code_length=len(code))
        
        return result
    
    @staticmethod
    def generate_backup_codes(count: int = 10) -> List[str]:
        """
        Generate backup codes for 2FA recovery
        
        Args:
            count: Number of backup codes to generate
            
        Returns:
            List of backup codes
        """
        codes = []
        for _ in range(count):
            # Generate 8-character alphanumeric code
            code = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(8))
            codes.append(code)
        
        logger.security("Backup codes generated", count=count)
        
        return codes


class EncryptionUtils:
    """Data encryption and decryption utilities"""
    
    def __init__(self, key: bytes = None):
        if key:
            self.key = key
        else:
            self.key = self._generate_key()
        self.cipher = Fernet(self.key)
    
    def _generate_key(self) -> bytes:
        """Generate encryption key"""
        return Fernet.generate_key()
    
    def encrypt_data(self, data: Union[str, bytes]) -> str:
        """
        Encrypt data
        
        Args:
            data: Data to encrypt
            
        Returns:
            Base64-encoded encrypted data
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        encrypted = self.cipher.encrypt(data)
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')
    
    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt data
        
        Args:
            encrypted_data: Base64-encoded encrypted data
            
        Returns:
            Decrypted data as string
            
        Raises:
            SecurityError: If decryption fails
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted = self.cipher.decrypt(encrypted_bytes)
            return decrypted.decode('utf-8')
        except Exception as e:
            logger.security("Decryption failed", error=str(e))
            raise SecurityError("Failed to decrypt data")
    
    @staticmethod
    def derive_key_from_password(password: str, salt: bytes = None) -> Tuple[bytes, bytes]:
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: Password to derive key from
            salt: Salt bytes (generated if not provided)
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        
        return key, salt


class SecurityMonitoring:
    """Security monitoring and threat detection"""
    
    def __init__(self):
        self.failed_attempts = {}
        self.suspicious_ips = set()
        self.rate_limits = {}
    
    def track_failed_login(self, user_id: str, ip_address: str) -> bool:
        """
        Track failed login attempts
        
        Args:
            user_id: User identifier
            ip_address: IP address of attempt
            
        Returns:
            True if account should be locked
        """
        now = time.time()
        
        # Track by user
        if user_id not in self.failed_attempts:
            self.failed_attempts[user_id] = []
        
        self.failed_attempts[user_id].append(now)
        
        # Clean old attempts (older than 1 hour)
        self.failed_attempts[user_id] = [
            attempt for attempt in self.failed_attempts[user_id]
            if now - attempt < 3600
        ]
        
        # Check if threshold exceeded
        recent_attempts = len(self.failed_attempts[user_id])
        
        if recent_attempts >= 5:
            logger.security("Multiple failed login attempts detected",
                           user_id=user_id,
                           ip_address=ip_address,
                           attempt_count=recent_attempts)
            
            self.suspicious_ips.add(ip_address)
            return True
        
        return False
    
    def is_suspicious_ip(self, ip_address: str) -> bool:
        """Check if IP address is flagged as suspicious"""
        return ip_address in self.suspicious_ips
    
    def check_rate_limit(self, identifier: str, limit: int, window: int) -> bool:
        """
        Check rate limiting
        
        Args:
            identifier: Unique identifier (user_id, ip_address, etc.)
            limit: Maximum requests allowed
            window: Time window in seconds
            
        Returns:
            True if rate limit exceeded
        """
        now = time.time()
        
        if identifier not in self.rate_limits:
            self.rate_limits[identifier] = []
        
        # Clean old requests
        self.rate_limits[identifier] = [
            req_time for req_time in self.rate_limits[identifier]
            if now - req_time < window
        ]
        
        # Add current request
        self.rate_limits[identifier].append(now)
        
        # Check limit
        if len(self.rate_limits[identifier]) > limit:
            logger.security("Rate limit exceeded",
                           identifier=identifier,
                           limit=limit,
                           window=window,
                           request_count=len(self.rate_limits[identifier]))
            return True
        
        return False
    
    def detect_suspicious_patterns(self, request_data: Dict[str, Any]) -> List[str]:
        """
        Detect suspicious patterns in requests
        
        Args:
            request_data: Request information
            
        Returns:
            List of detected suspicious patterns
        """
        suspicious_patterns = []
        
        # Check user agent
        user_agent = request_data.get('user_agent', '').lower()
        bot_indicators = ['bot', 'crawler', 'spider', 'scraper', 'curl', 'wget']
        if any(indicator in user_agent for indicator in bot_indicators):
            suspicious_patterns.append("bot_user_agent")
        
        # Check for automation tools
        automation_tools = ['selenium', 'puppeteer', 'playwright', 'requests']
        if any(tool in user_agent for tool in automation_tools):
            suspicious_patterns.append("automation_tool")
        
        # Check request patterns
        if request_data.get('method') in ['PUT', 'DELETE', 'PATCH'] and 'admin' in request_data.get('path', ''):
            suspicious_patterns.append("admin_modification_attempt")
        
        # Check for common attack patterns
        path = request_data.get('path', '').lower()
        attack_patterns = ['..//', '..\\\\', 'etc/passwd', 'cmd.exe', 'powershell']
        if any(pattern in path for pattern in attack_patterns):
            suspicious_patterns.append("path_traversal_attempt")
        
        return suspicious_patterns


class CSRFProtection:
    """CSRF protection utilities"""
    
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
    
    def generate_csrf_token(self, session_id: str) -> str:
        """Generate CSRF token tied to session"""
        timestamp = str(int(time.time()))
        message = f"{session_id}:{timestamp}"
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        token = base64.urlsafe_b64encode(f"{message}:{signature}".encode('utf-8')).decode('utf-8')
        return token
    
    def verify_csrf_token(self, token: str, session_id: str, max_age: int = 3600) -> bool:
        """
        Verify CSRF token
        
        Args:
            token: CSRF token to verify
            session_id: Current session ID
            max_age: Maximum token age in seconds
            
        Returns:
            True if token is valid
        """
        try:
            decoded = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
            parts = decoded.split(':')
            
            if len(parts) != 3:
                return False
            
            token_session_id, timestamp, signature = parts
            
            # Check session ID
            if token_session_id != session_id:
                return False
            
            # Check timestamp
            now = int(time.time())
            token_time = int(timestamp)
            if now - token_time > max_age:
                return False
            
            # Verify signature
            message = f"{token_session_id}:{timestamp}"
            expected_signature = hmac.new(
                self.secret_key.encode('utf-8'),
                message.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
        
        except Exception:
            return False


# Convenience functions
def hash_password(password: str, rounds: int = 12) -> str:
    """Convenience function for password hashing"""
    return PasswordSecurity.hash_password(password, rounds)


def verify_password(password: str, hashed_password: str) -> bool:
    """Convenience function for password verification"""
    return PasswordSecurity.verify_password(password, hashed_password)


def generate_token(length: int = 32) -> str:
    """Generate secure random token"""
    return secrets.token_urlsafe(length)


def verify_token(token: str, secret_key: str) -> Dict[str, Any]:
    """Convenience function for JWT token verification"""
    token_security = TokenSecurity(secret_key)
    return token_security.verify_jwt_token(token)


def secure_random_string(length: int = 16, alphabet: str = None) -> str:
    """
    Generate cryptographically secure random string
    
    Args:
        length: String length
        alphabet: Character set to use
        
    Returns:
        Random string
    """
    if alphabet is None:
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def constant_time_compare(a: str, b: str) -> bool:
    """
    Compare strings in constant time to prevent timing attacks
    
    Args:
        a: First string
        b: Second string
        
    Returns:
        True if strings are equal
    """
    return hmac.compare_digest(a.encode('utf-8'), b.encode('utf-8'))
