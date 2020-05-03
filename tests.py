"""Tests for Ledger."""

import unittest

from exceptions import AccountError
from ledger import Ledger, Accounts, Account, Transaction


class TestTransaction(unittest.TestCase):
    def test_create_transaction(self):
        transaction = Transaction("2020-01-22", "john", "mary", 20)
        self.assertEqual(str(transaction), "2020-01-22, john, mary, 20")


class TestAccounts(unittest.TestCase):
    def test_create_accounts(self):
        accounts = Accounts()
        account = accounts.get_account("john")
        self.assertEqual(account.name, "john")
        self.assertEqual(account.balance, 0)


class TestAccount(unittest.TestCase):
    def test_create_account_john(self):
        account_name = "john"
        account = Account(account_name)
        self.assertEqual(account.name, account_name)
        self.assertFalse(account.transactions)
        self.assertFalse(account.balances)
        self.assertEqual(account.balance, 0)

    def test_get_balance_with_one_transaction(self):
        account_name = "john"
        account = Account(account_name)
        payer = "john"
        payee = "mary"
        account = Account(account_name)
        transaction = Transaction("2020-01-22", payer, payee, 20)
        account.add_transaction(transaction)
        self.assertEqual(account.balance, -20)

        # Balance on date of transaction should be -20
        self.assertEqual(account.get_balance("2020-01-22"), -20)

        # Balance after date of transaction should be -20
        self.assertEqual(account.get_balance("2020-01-25"), -20)

        # Balance before first transaction - assume open and 0
        self.assertEqual(account.get_balance("2015-01-21"), 0)

    def test_get_balance_with_two_transactions(self):
        account_name = "john"
        account = Account(account_name)
        payer = "john"
        payee = "mary"
        account = Account(account_name)
        transaction = Transaction("2020-01-22", payer, payee, 20)
        account.add_transaction(transaction)
        transaction = Transaction("2020-01-25", payer, payee, 20)
        account.add_transaction(transaction)

        self.assertEqual(account.get_balance("2020-01-22"), -20)

        # Check balance between transactions is as expected
        self.assertEqual(account.get_balance("2020-01-23"), -20)

        #  Check final balance as expected
        self.assertEqual(account.get_balance("2020-01-25"), -40)

    def test_get_balance_with_five_transactions(self):
        account_name = "john"
        account = Account(account_name)
        payer = "john"
        payee = "mary"
        account = Account(account_name)
        transaction = Transaction("2020-01-01", payer, payee, 20)
        account.add_transaction(transaction)
        transaction = Transaction("2020-01-03", payer, payee, 20)
        account.add_transaction(transaction)
        transaction = Transaction("2020-01-05", payer, payee, 20)
        account.add_transaction(transaction)
        transaction = Transaction("2020-01-22", payer, payee, 20)
        account.add_transaction(transaction)
        transaction = Transaction("2020-01-30", payer, payee, 20)
        account.add_transaction(transaction)

        self.assertEqual(account.get_balance("2020-01-02"), -20)
        self.assertEqual(account.get_balance("2020-01-05"), -60)
        self.assertEqual(account.get_balance("2020-01-06"), -60)
        self.assertEqual(account.get_balance("2020-01-07"), -60)
        self.assertEqual(account.get_balance("2020-01-21"), -60)
        self.assertEqual(account.get_balance("2020-01-22"), -80)
        self.assertEqual(account.get_balance("2020-01-23"), -80)
        self.assertEqual(account.get_balance("2020-01-29"), -80)
        self.assertEqual(account.get_balance("2020-01-30"), -100)
        self.assertEqual(account.get_balance("2020-01-31"), -100)

    def test_add_invalid_name_transaction(self):
        account_name = "john"
        account = Account(account_name)
        payer = "mary"
        payee = "insurance"
        account = Account(account_name)
        transaction = Transaction("2020-01-22", payer, payee, 20)

        with self.assertRaises(AccountError):
            account.add_transaction(transaction)


class TestLedger(unittest.TestCase):
    def test_create_ledger(self):
        l = Ledger("transactions.csv")
        self.assertEqual(l.filename, "transactions.csv")


if __name__ == "__main__":
    unittest.main()
