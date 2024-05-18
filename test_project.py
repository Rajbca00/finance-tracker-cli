import os
from click.testing import CliRunner
import click
from click import Context
import json
from project import main, create_account, add_transaction, print_balance, get_accounts

def test_create_account():
    """Test the create_account() command"""
    if os.path.exists('accounts.json'):
        os.remove('accounts.json')
    runner = CliRunner()
    result = runner.invoke(main, ['create-account', '--name', 'Test Account', '--initial-balance', '100.00'])
    assert result.exit_code == 0

    result = runner.invoke(main, ['create-account', '--name', 'Test Account', '--initial-balance', '100.00'])
    assert result.exit_code == 0
    assert "already exists" in result.output

def test_add_transaction():
    """Test the add_transaction() command"""
    runner = CliRunner()
    result = runner.invoke(main, ['add-transaction', '--name', 'Test Account', '--transaction-name', 'Test Transaction', '--amount', '100.00'])
    assert result.exit_code == 0

def test_print_balance():
    """Test the print_balance() command"""
    runner = CliRunner()
    result = runner.invoke(main, ['print-balance', '--name', 'Test Account'])
    assert result.exit_code == 0


