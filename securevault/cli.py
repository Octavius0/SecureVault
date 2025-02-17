"""
Command line interface for SecureVault
"""

import click
from .generator import PasswordGenerator


@click.group()
@click.version_option(version="0.1.0")
def main():
    """SecureVault - A personal password manager"""
    pass


@main.command()
@click.option('--length', '-l', default=16, help='Password length')
@click.option('--no-uppercase', is_flag=True, help='Exclude uppercase letters')
@click.option('--no-digits', is_flag=True, help='Exclude digits')
@click.option('--no-symbols', is_flag=True, help='Exclude symbols')
def generate(length, no_uppercase, no_digits, no_symbols):
    """Generate a random password"""
    generator = PasswordGenerator()

    password = generator.generate(
        length=length,
        use_uppercase=not no_uppercase,
        use_digits=not no_digits,
        use_symbols=not no_symbols
    )

    click.echo(f"Generated password: {password}")


@main.command()
@click.option('--words', '-w', default=4, help='Number of words')
@click.option('--separator', '-s', default='-', help='Word separator')
def memorable(words, separator):
    """Generate a memorable password"""
    generator = PasswordGenerator()
    password = generator.generate_memorable(word_count=words, separator=separator)
    click.echo(f"Memorable password: {password}")


@main.command()
def init():
    """Initialize a new vault"""
    click.echo("Vault initialization not yet implemented")


@main.command()
def add():
    """Add a new password entry"""
    click.echo("Add password not yet implemented")


@main.command()
def list():
    """List all password entries"""
    click.echo("List passwords not yet implemented")


if __name__ == '__main__':
    main()