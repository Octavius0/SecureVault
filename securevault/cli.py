"""
Command line interface for SecureVault
"""

import click
import getpass
from .generator import PasswordGenerator
from .storage import SecureVault, PasswordEntry


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
    vault = SecureVault()

    if vault.vault_path.exists():
        click.echo("Vault already exists!")
        return

    click.echo("Creating new SecureVault...")
    master_password = getpass.getpass("Enter master password: ")
    confirm_password = getpass.getpass("Confirm master password: ")

    if master_password != confirm_password:
        click.echo("Passwords don't match!")
        return

    if len(master_password) < 8:
        click.echo("Master password must be at least 8 characters!")
        return

    if vault.init_vault(master_password):
        click.echo(f"Vault created successfully at {vault.vault_path}")
    else:
        click.echo("Failed to create vault!")


@main.command()
@click.option('--name', prompt=True, help='Entry name')
@click.option('--username', prompt=True, help='Username')
@click.option('--password', help='Password (will prompt if not provided)')
@click.option('--url', default='', help='Website URL')
@click.option('--notes', default='', help='Additional notes')
@click.option('--category', default='', help='Category')
def add(name, username, password, url, notes, category):
    """Add a new password entry"""
    vault = SecureVault()

    if not vault.vault_path.exists():
        click.echo("No vault found. Run 'securevault init' first.")
        return

    master_password = getpass.getpass("Enter master password: ")
    if not vault.unlock(master_password):
        click.echo("Invalid master password!")
        return

    if not password:
        password = getpass.getpass("Enter password for this entry: ")

    entry = PasswordEntry(
        name=name,
        username=username,
        password=password,
        url=url,
        notes=notes,
        category=category
    )

    if vault.add_entry(entry):
        click.echo(f"Added entry '{name}' successfully!")
    else:
        click.echo("Failed to add entry!")


@main.command()
@click.option('--category', help='Filter by category')
@click.option('--search', help='Search entries')
def list(category, search):
    """List all password entries"""
    vault = SecureVault()

    if not vault.vault_path.exists():
        click.echo("No vault found. Run 'securevault init' first.")
        return

    master_password = getpass.getpass("Enter master password: ")
    if not vault.unlock(master_password):
        click.echo("Invalid master password!")
        return

    if search:
        entries = vault.search_entries(search)
    else:
        entries = vault.get_entries(category)

    if not entries:
        click.echo("No entries found.")
        return

    click.echo(f"\nFound {len(entries)} entries:")
    click.echo("-" * 50)

    for entry in entries:
        click.echo(f"Name: {entry.name}")
        click.echo(f"Username: {entry.username}")
        if entry.url:
            click.echo(f"URL: {entry.url}")
        if entry.category:
            click.echo(f"Category: {entry.category}")
        if entry.notes:
            click.echo(f"Notes: {entry.notes}")
        click.echo("-" * 50)


@main.command()
@click.argument('name')
@click.option('--show-password', is_flag=True, help='Show the password')
def get(name, show_password):
    """Get a specific password entry"""
    vault = SecureVault()

    if not vault.vault_path.exists():
        click.echo("No vault found. Run 'securevault init' first.")
        return

    master_password = getpass.getpass("Enter master password: ")
    if not vault.unlock(master_password):
        click.echo("Invalid master password!")
        return

    entries = vault.search_entries(name)

    if not entries:
        click.echo(f"No entry found for '{name}'")
        return

    if len(entries) > 1:
        click.echo(f"Multiple entries found for '{name}':")
        for i, entry in enumerate(entries, 1):
            click.echo(f"{i}. {entry.name} ({entry.username})")

        try:
            choice = click.prompt("Select entry number", type=int)
            if 1 <= choice <= len(entries):
                entry = entries[choice - 1]
            else:
                click.echo("Invalid selection")
                return
        except:
            click.echo("Invalid input")
            return
    else:
        entry = entries[0]

    click.echo(f"\nEntry: {entry.name}")
    click.echo(f"Username: {entry.username}")

    if show_password:
        click.echo(f"Password: {entry.password}")
    else:
        click.echo("Password: [hidden] (use --show-password to reveal)")

    if entry.url:
        click.echo(f"URL: {entry.url}")
    if entry.category:
        click.echo(f"Category: {entry.category}")
    if entry.notes:
        click.echo(f"Notes: {entry.notes}")


if __name__ == '__main__':
    main()