"""
ScamShield AI - Supabase Client Integration
Production-ready Supabase client with authentication and database operations
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Union
from datetime import datetime, timezone
from supabase import create_client, Client
from gotrue.errors import AuthError
import asyncio
from functools import wraps

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SupabaseClient:
    """Production-ready Supabase client for ScamShield AI"""
    
    def __init__(self):
        self.url = "https://unnrwgigpoewjuahspip.supabase.co"
        self.service_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVubnJ3Z2lncG9ld2p1YWhzcGlwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MjAzNzIwOSwiZXhwIjoyMDY3NjEzMjA5fQ.v1OiX_eo9blFZ1GHbvovSgYrqy63KjF03gBcsfLqEcE"
        self.anon_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVubnJ3Z2lncG9ld2p1YWhzcGlwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTIwMzcyMDksImV4cCI6MjA2NzYxMzIwOX0.I1A7gZPse01XUcr-snPWWn-mUUikO0yKs7hj2fTP7S0"
        
        # Create clients
        self.admin_client: Client = create_client(self.url, self.service_key)
        self.client: Client = create_client(self.url, self.anon_key)
        
        logger.info("Supabase client initialized successfully")
    
    def handle_errors(func):
        """Decorator to handle Supabase errors gracefully"""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except AuthError as e:
                logger.error(f"Authentication error in {func.__name__}: {str(e)}")
                raise Exception(f"Authentication failed: {str(e)}")
            except Exception as e:
                logger.error(f"Error in {func.__name__}: {str(e)}")
                raise Exception(f"Database operation failed: {str(e)}")
        return wrapper
    
    # User Management
    @handle_errors
    def create_user(self, email: str, password: str, full_name: str = None) -> Dict[str, Any]:
        """Create a new user account"""
        try:
            response = self.admin_client.auth.admin.create_user({
                "email": email,
                "password": password,
                "email_confirm": True,
                "user_metadata": {"full_name": full_name or email}
            })
            
            logger.info(f"User created successfully: {email}")
            return {
                "success": True,
                "user": response.user,
                "message": "User created successfully"
            }
        except Exception as e:
            logger.error(f"Failed to create user {email}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create user"
            }
    
    @handle_errors
    def authenticate_user(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate user and return session"""
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            logger.info(f"User authenticated successfully: {email}")
            return {
                "success": True,
                "session": response.session,
                "user": response.user,
                "message": "Authentication successful"
            }
        except Exception as e:
            logger.error(f"Authentication failed for {email}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Authentication failed"
            }
    
    @handle_errors
    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile by ID"""
        try:
            response = self.admin_client.table('profiles').select('*').eq('id', user_id).execute()
            
            if response.data:
                return {
                    "success": True,
                    "profile": response.data[0],
                    "message": "Profile retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Profile not found",
                    "message": "User profile not found"
                }
        except Exception as e:
            logger.error(f"Failed to get profile for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve profile"
            }
    
    @handle_errors
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            # Add updated_at timestamp
            updates['updated_at'] = datetime.now(timezone.utc).isoformat()
            
            response = self.admin_client.table('profiles').update(updates).eq('id', user_id).execute()
            
            logger.info(f"Profile updated for user {user_id}")
            return {
                "success": True,
                "profile": response.data[0] if response.data else None,
                "message": "Profile updated successfully"
            }
        except Exception as e:
            logger.error(f"Failed to update profile for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update profile"
            }
    
    # Investigation Management
    @handle_errors
    def create_investigation(self, user_id: str, investigation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new investigation"""
        try:
            # Prepare investigation data
            investigation = {
                "user_id": user_id,
                "title": investigation_data.get("title"),
                "target_url": investigation_data.get("target_url"),
                "target_email": investigation_data.get("target_email"),
                "target_phone": investigation_data.get("target_phone"),
                "target_company": investigation_data.get("target_company"),
                "investigation_type": investigation_data.get("investigation_type", "comprehensive"),
                "status": "pending",
                "priority": investigation_data.get("priority", "normal"),
                "evidence_data": investigation_data.get("evidence_data", {}),
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            response = self.admin_client.table('investigations').insert(investigation).execute()
            
            logger.info(f"Investigation created for user {user_id}")
            return {
                "success": True,
                "investigation": response.data[0] if response.data else None,
                "message": "Investigation created successfully"
            }
        except Exception as e:
            logger.error(f"Failed to create investigation for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create investigation"
            }
    
    @handle_errors
    def get_user_investigations(self, user_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get investigations for a user"""
        try:
            response = (self.admin_client.table('investigations')
                       .select('*')
                       .eq('user_id', user_id)
                       .order('created_at', desc=True)
                       .limit(limit)
                       .execute())
            
            return {
                "success": True,
                "investigations": response.data,
                "count": len(response.data),
                "message": "Investigations retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Failed to get investigations for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve investigations"
            }
    
    @handle_errors
    def update_investigation(self, investigation_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update investigation status and results"""
        try:
            # Add updated_at timestamp
            updates['updated_at'] = datetime.now(timezone.utc).isoformat()
            
            # Add completed_at if status is completed
            if updates.get('status') == 'completed':
                updates['completed_at'] = datetime.now(timezone.utc).isoformat()
            
            response = (self.admin_client.table('investigations')
                       .update(updates)
                       .eq('id', investigation_id)
                       .execute())
            
            logger.info(f"Investigation {investigation_id} updated")
            return {
                "success": True,
                "investigation": response.data[0] if response.data else None,
                "message": "Investigation updated successfully"
            }
        except Exception as e:
            logger.error(f"Failed to update investigation {investigation_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update investigation"
            }
    
    # Credit Management
    @handle_errors
    def update_user_credits(self, user_id: str, credit_change: int, 
                           transaction_type: str, description: str = None,
                           investigation_id: str = None) -> Dict[str, Any]:
        """Update user credit balance using stored procedure"""
        try:
            response = self.admin_client.rpc('update_credit_balance', {
                'user_uuid': user_id,
                'credit_change': credit_change,
                'transaction_type': transaction_type,
                'description': description,
                'investigation_uuid': investigation_id
            }).execute()
            
            if response.data:
                logger.info(f"Credits updated for user {user_id}: {credit_change}")
                return {
                    "success": True,
                    "result": response.data,
                    "message": "Credits updated successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Insufficient credits or invalid operation",
                    "message": "Failed to update credits"
                }
        except Exception as e:
            logger.error(f"Failed to update credits for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to update credits"
            }
    
    @handle_errors
    def get_user_credit_history(self, user_id: str, limit: int = 50) -> Dict[str, Any]:
        """Get credit transaction history for user"""
        try:
            response = (self.admin_client.table('credit_transactions')
                       .select('*')
                       .eq('user_id', user_id)
                       .order('created_at', desc=True)
                       .limit(limit)
                       .execute())
            
            return {
                "success": True,
                "transactions": response.data,
                "count": len(response.data),
                "message": "Credit history retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Failed to get credit history for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve credit history"
            }
    
    # Evidence Management
    @handle_errors
    def create_evidence_artifact(self, investigation_id: str, artifact_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create evidence artifact record"""
        try:
            artifact = {
                "investigation_id": investigation_id,
                "artifact_type": artifact_data.get("artifact_type"),
                "file_name": artifact_data.get("file_name"),
                "file_path": artifact_data.get("file_path"),
                "file_size": artifact_data.get("file_size"),
                "mime_type": artifact_data.get("mime_type"),
                "metadata": artifact_data.get("metadata", {}),
                "source_url": artifact_data.get("source_url"),
                "extraction_method": artifact_data.get("extraction_method"),
                "confidence_score": artifact_data.get("confidence_score"),
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            
            response = self.admin_client.table('evidence_artifacts').insert(artifact).execute()
            
            logger.info(f"Evidence artifact created for investigation {investigation_id}")
            return {
                "success": True,
                "artifact": response.data[0] if response.data else None,
                "message": "Evidence artifact created successfully"
            }
        except Exception as e:
            logger.error(f"Failed to create evidence artifact: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create evidence artifact"
            }
    
    # Analytics and Statistics
    @handle_errors
    def get_user_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get user statistics using stored procedure"""
        try:
            response = self.admin_client.rpc('get_user_stats', {
                'user_uuid': user_id
            }).execute()
            
            return {
                "success": True,
                "statistics": response.data,
                "message": "Statistics retrieved successfully"
            }
        except Exception as e:
            logger.error(f"Failed to get statistics for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve statistics"
            }
    
    @handle_errors
    def get_dashboard_data(self, user_id: str) -> Dict[str, Any]:
        """Get comprehensive dashboard data for user"""
        try:
            response = (self.admin_client.table('user_dashboard')
                       .select('*')
                       .eq('id', user_id)
                       .execute())
            
            if response.data:
                return {
                    "success": True,
                    "dashboard": response.data[0],
                    "message": "Dashboard data retrieved successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Dashboard data not found",
                    "message": "No dashboard data available"
                }
        except Exception as e:
            logger.error(f"Failed to get dashboard data for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to retrieve dashboard data"
            }
    
    # File Storage Operations
    @handle_errors
    def upload_file(self, bucket: str, file_path: str, file_data: bytes, 
                   content_type: str = None) -> Dict[str, Any]:
        """Upload file to Supabase storage"""
        try:
            response = self.admin_client.storage.from_(bucket).upload(
                file_path, file_data, {"content-type": content_type}
            )
            
            logger.info(f"File uploaded to {bucket}/{file_path}")
            return {
                "success": True,
                "path": file_path,
                "message": "File uploaded successfully"
            }
        except Exception as e:
            logger.error(f"Failed to upload file to {bucket}/{file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to upload file"
            }
    
    @handle_errors
    def get_file_url(self, bucket: str, file_path: str, expires_in: int = 3600) -> Dict[str, Any]:
        """Get signed URL for file access"""
        try:
            response = self.admin_client.storage.from_(bucket).create_signed_url(
                file_path, expires_in
            )
            
            return {
                "success": True,
                "url": response.get('signedURL'),
                "expires_in": expires_in,
                "message": "Signed URL created successfully"
            }
        except Exception as e:
            logger.error(f"Failed to create signed URL for {bucket}/{file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to create signed URL"
            }

# Global instance
supabase_client = SupabaseClient()

# Export for easy importing
__all__ = ['supabase_client', 'SupabaseClient']

