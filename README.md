# SecureVault

A personal password manager with strong encryption for secure local storage.

## Features
- ✅ Secure password storage with AES encryption
- ✅ Password generation with customizable rules
- ✅ Master password protection
- ✅ Search and categorize passwords
- ✅ Command line interface

## Installation

```bash
pip install -e .
```

## Usage

### Initialize a new vault
```bash
securevault init
```

### Generate passwords
```bash
# Random password
securevault generate --length 20

# Memorable password
securevault memorable --words 4
```

### Manage passwords
```bash
# Add a new entry
securevault add

# List all entries
securevault list

# Search entries
securevault list --search github

# Get specific entry
securevault get mysite
securevault get mysite --show-password
```

## Security Notes
- All passwords are encrypted using AES-256
- Master password is hashed with PBKDF2 (100,000 iterations)
- Vault stored locally at ~/.securevault/vault.enc
- No data is transmitted over network