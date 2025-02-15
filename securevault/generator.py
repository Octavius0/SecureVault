"""
Password generation utilities
"""

import random
import string


class PasswordGenerator:
    """Generate secure random passwords"""

    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    def generate(self, length: int = 16, use_uppercase: bool = True,
                 use_digits: bool = True, use_symbols: bool = True) -> str:
        """Generate a random password with specified options"""
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")

        chars = self.lowercase

        if use_uppercase:
            chars += self.uppercase
        if use_digits:
            chars += self.digits
        if use_symbols:
            chars += self.symbols

        password = ''.join(random.choice(chars) for _ in range(length))
        return password

    def generate_memorable(self, word_count: int = 4, separator: str = "-") -> str:
        """Generate a memorable password using random words"""
        # Simple word list for memorable passwords
        words = [
            "apple", "brave", "cloud", "dance", "eagle", "flame", "green", "happy",
            "island", "jungle", "knight", "lemon", "magic", "noble", "ocean", "peace",
            "quest", "river", "storm", "tiger", "unity", "violet", "winter", "zebra"
        ]

        selected_words = random.sample(words, min(word_count, len(words)))
        return separator.join(selected_words)