"""
Authentication and User Management Module
Handles user registration, login, and profile management
"""
import json
import os
import hashlib
from datetime import datetime
from typing import Optional, Dict
import secrets


class AuthManager:
    """Manages user authentication and profiles"""
    
    def __init__(self, users_file: str = "users.json"):
        self.users_file = users_file
        self.users = self._load_users()
    
    def _load_users(self) -> Dict:
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, email: str = "", full_name: str = "") -> tuple[bool, str]:
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        # Validate input
        if not username or not password:
            return False, "Username and password are required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Check if user already exists
        if username in self.users:
            return False, "Username already exists"
        
        # Create user
        user_id = len(self.users) + 1
        self.users[username] = {
            "id": user_id,
            "username": username,
            "password_hash": self._hash_password(password),
            "email": email,
            "full_name": full_name,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "profile": {
                "currency": "USD",
                "date_format": "YYYY-MM-DD",
                "theme": "light"
            }
        }
        
        self._save_users()
        return True, "User registered successfully"
    
    def authenticate_user(self, username: str, password: str) -> tuple[bool, str]:
        """
        Authenticate a user
        Returns: (success: bool, message: str)
        """
        if username not in self.users:
            return False, "Invalid username or password"
        
        user = self.users[username]
        password_hash = self._hash_password(password)
        
        if user["password_hash"] != password_hash:
            return False, "Invalid username or password"
        
        # Update last login
        user["last_login"] = datetime.now().isoformat()
        self._save_users()
        
        return True, "Login successful"
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user information"""
        return self.users.get(username)
    
    def update_user_profile(self, username: str, **kwargs) -> bool:
        """Update user profile information"""
        if username not in self.users:
            return False
        
        user = self.users[username]
        
        # Update allowed fields
        allowed_fields = ["email", "full_name"]
        for field, value in kwargs.items():
            if field in allowed_fields:
                user[field] = value
            elif field == "currency" or field == "date_format" or field == "theme":
                user["profile"][field] = value
        
        self._save_users()
        return True
    
    def change_password(self, username: str, old_password: str, new_password: str) -> tuple[bool, str]:
        """Change user password"""
        if username not in self.users:
            return False, "User not found"
        
        # Verify old password
        user = self.users[username]
        old_password_hash = self._hash_password(old_password)
        
        if user["password_hash"] != old_password_hash:
            return False, "Current password is incorrect"
        
        # Validate new password
        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long"
        
        # Update password
        user["password_hash"] = self._hash_password(new_password)
        self._save_users()
        
        return True, "Password changed successfully"
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists"""
        return username in self.users
