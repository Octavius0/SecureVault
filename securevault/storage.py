"""
Secure storage for password entries
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from .crypto import CryptoManager


class PasswordEntry:
    """Represents a single password entry"""

    def __init__(self, name: str, username: str, password: str,
                 url: str = "", notes: str = "", category: str = ""):
        self.name = name
        self.username = username
        self.password = password
        self.url = url
        self.notes = notes
        self.category = category

    def to_dict(self) -> Dict:
        """Convert entry to dictionary"""
        return {
            'name': self.name,
            'username': self.username,
            'password': self.password,
            'url': self.url,
            'notes': self.notes,
            'category': self.category
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'PasswordEntry':
        """Create entry from dictionary"""
        return cls(
            name=data.get('name', ''),
            username=data.get('username', ''),
            password=data.get('password', ''),
            url=data.get('url', ''),
            notes=data.get('notes', ''),
            category=data.get('category', '')
        )


class SecureVault:
    """Manages encrypted storage of password entries"""

    def __init__(self, vault_path: str = None):
        if vault_path is None:
            vault_path = os.path.join(Path.home(), '.securevault', 'vault.enc')

        self.vault_path = Path(vault_path)
        self.vault_dir = self.vault_path.parent
        self.crypto = CryptoManager()
        self.entries: List[PasswordEntry] = []
        self._is_unlocked = False

    def init_vault(self, master_password: str) -> bool:
        """Initialize a new vault with master password"""
        if self.vault_path.exists():
            return False

        self.vault_dir.mkdir(parents=True, exist_ok=True)

        # Create initial empty vault
        self.crypto.derive_key(master_password)
        self._save_vault()
        self._is_unlocked = True
        return True

    def unlock(self, master_password: str) -> bool:
        """Unlock vault with master password"""
        if not self.vault_path.exists():
            return False

        try:
            with open(self.vault_path, 'rb') as f:
                encrypted_data = f.read()

            # First 16 bytes are salt
            salt = encrypted_data[:16]
            vault_data = encrypted_data[16:]

            self.crypto.derive_key(master_password, salt)
            decrypted_json = self.crypto.decrypt(vault_data)

            vault_data = json.loads(decrypted_json)
            self.entries = [PasswordEntry.from_dict(entry) for entry in vault_data.get('entries', [])]

            self._is_unlocked = True
            return True

        except Exception:
            return False

    def add_entry(self, entry: PasswordEntry) -> bool:
        """Add a new password entry"""
        if not self._is_unlocked:
            return False

        self.entries.append(entry)
        self._save_vault()
        return True

    def get_entries(self, category: str = None) -> List[PasswordEntry]:
        """Get all entries, optionally filtered by category"""
        if not self._is_unlocked:
            return []

        if category:
            return [entry for entry in self.entries if entry.category == category]
        return self.entries.copy()

    def search_entries(self, query: str) -> List[PasswordEntry]:
        """Search entries by name, username, or URL"""
        if not self._is_unlocked:
            return []

        query = query.lower()
        results = []

        for entry in self.entries:
            if (query in entry.name.lower() or
                query in entry.username.lower() or
                query in entry.url.lower()):
                results.append(entry)

        return results

    def _save_vault(self):
        """Save vault to encrypted file"""
        if not self._is_unlocked:
            return

        vault_data = {
            'entries': [entry.to_dict() for entry in self.entries]
        }

        json_data = json.dumps(vault_data, indent=2)
        encrypted_data = self.crypto.encrypt(json_data)

        # Prepend salt to encrypted data
        with open(self.vault_path, 'wb') as f:
            f.write(self.crypto.get_salt())
            f.write(encrypted_data)

    def lock(self):
        """Lock the vault and clear sensitive data"""
        self.entries.clear()
        self.crypto.key = None
        self._is_unlocked = False