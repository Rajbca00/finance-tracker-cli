import os
import click
import json

def get_accounts() -> list:
    """Get all accounts"""
    if os.path.exists('accounts.json'):
        with open('accounts.json', 'r', encoding="utf-8") as file:
            accounts = file.read()
            click.echo(accounts)
            return json.loads(accounts) if accounts else []
    return []

@click.group()
def main():
    """Finance Tracker command line interface"""

@main.command()
@click.option('--name', type=str, prompt='Account Name')
@click.option('--initial-balance', type=float, prompt='Initial balance')
def create_account(name, initial_balance):
    """Create a new account with the specified name and initial balance"""
    if not name:
        name = click.prompt('Account name')
    accounts = get_accounts()
    if any(account['name'] == name for account in accounts):
        click.echo(f"Account '{name}' already exists")
        return
    account = {
        'name': name,
        'balance': initial_balance,
        'transactions': []
    }
    accounts.append(account)
    with open('accounts.json', 'w', encoding='utf-8') as file:
        json.dump(accounts, file, indent=4)
    click.echo(f"Account '{name}' created with initial balance of {initial_balance}")

@main.command()
@click.option('--name', required=False)
@click.option('--transaction-name', prompt='Transaction name')
@click.option('--amount', type=float, prompt='Transaction amount')
def add_transaction(name, transaction_name, amount):
    """Add a new transaction to the specified account"""
    if not name:
        names = [account['name'] for account in get_accounts()]
        name = click.prompt('Account name', type=click.Choice(names))
    accounts = get_accounts()
    for account in accounts:
        if account['name'] == name:
            account['transactions'].append({
                'name': transaction_name,
                'amount': amount
            })
            account['balance'] -= amount
    with open('accounts.json', 'w', encoding='utf-8') as file:
        json.dump(accounts, file, indent=4)
    click.echo(f"Transaction '{transaction_name}' added to account '{name}' with amount {amount}")

@main.command()
@click.option('--name', required=False)
def print_balance(name):
    """Print the current balance of the specified account"""
    if not name:
        name = click.prompt('Account name')
    accounts = get_accounts()
    for account in accounts:
        if account['name'] == name:
            click.echo(f"Current balance of account '{name}': {account['balance']}")

if __name__ == '__main__':
    main()

