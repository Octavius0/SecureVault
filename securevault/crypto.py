"""
Encryption and decryption utilities for SecureVault
"""

import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class CryptoManager:
    """Handles encryption and decryption of passwords"""

    def __init__(self):
        self.salt = None
        self.key = None

    def derive_key(self, password: str, salt: bytes = None) -> bytes:
        """Derive encryption key from master password"""
        if salt is None:
            salt = os.urandom(16)
        self.salt = salt

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )

        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.key = key
        return key

    def encrypt(self, data: str) -> bytes:
        """Encrypt data using derived key"""
        if not self.key:
            raise ValueError("No encryption key available. Call derive_key first.")

        f = Fernet(self.key)
        return f.encrypt(data.encode())

    def decrypt(self, encrypted_data: bytes) -> str:
        """Decrypt data using derived key"""
        if not self.key:
            raise ValueError("No encryption key available. Call derive_key first.")

        f = Fernet(self.key)
        return f.decrypt(encrypted_data).decode()

    def get_salt(self) -> bytes:
        """Get the salt used for key derivation"""
        return self.salt