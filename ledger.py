"""This module contains classes for the Ledger program."""
import csv

from datetime import datetime, timedelta

from exceptions import AccountError


class Transaction:
    """A transaction between the payer and the payee"""

    def __init__(self, date, payer, payee, amount):
        self.date = date
        self.payer = payer
        self.payee = payee
        self.amount = amount

    def __str__(self):
        return f"{self.date}, {self.payer}, {self.payee}, {self.amount}"


class Account:
    """A party's account"""

    def __init__(self, name):
        self.name = name
        self.transactions = []
        self.balance = 0
        self.balances = {}
        self.first_transaction_date = None
        self.last_transaction_date = None

    def __str__(self):
        return f"name: {self.name}, balance: {self.balance}"

    def add_transaction(self, transaction):
        if not self.first_transaction_date:
            self.first_transaction_date = datetime.strptime(
                transaction.date, "%Y-%m-%d"
            )

        self.transactions.append(transaction)
        if self.name == transaction.payer:
            self.balance -= transaction.amount
        elif self.name == transaction.payee:
            self.balance += transaction.amount
        else:
            raise AccountError("No transaction names match this account.")

        self.last_transaction_date = datetime.strptime(transaction.date, "%Y-%m-%d")
        self.balances[transaction.date] = self.balance

    def get_balance(self, date):
        """Return the balance for the date provided"""

        #
        # If the date is on or after the latest
        # transaction, then return the latest balance.
        #
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        if date_obj >= self.last_transaction_date:
            return self.balance

        #
        # If the date is before the first transaction, then assume account
        # is opened and had zero balance
        #
        if date_obj < self.first_transaction_date:
            return 0

        # Look up the balance for transaction before this date
        one_day = timedelta(days=1)
        while date not in self.balances and date_obj > self.first_transaction_date:
            date_obj = date_obj - one_day
            date = date_obj.strftime("%Y-%m-%d")

        balance = self.balances.get(date)
        return balance


class Accounts:
    """The accounts read from the ledger file"""

    def __init__(self):
        self.accounts = {}

    def get_account(self, name):
        if not self.accounts.get(name):
            self.accounts[name] = Account(name)
        return self.accounts[name]

    def __iter__(self):
        return iter(self.accounts.items())


class Ledger:
    """Responsible for reading and processing the ledger file"""

    DATE = 0
    PAYER = 1
    PAYEE = 2
    AMOUNT = 3

    def __init__(self, filename):
        self.accounts = Accounts()
        self.filename = filename

        with open(self.filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            for row in csv_reader:
                date = row[Ledger.DATE]
                payer = row[Ledger.PAYER]
                payee = row[Ledger.PAYEE]
                amount = float(row[Ledger.AMOUNT])

                transaction = Transaction(date, payer, payee, amount)
                payer_account = self.accounts.get_account(payer)
                payee_account = self.accounts.get_account(payee)
                payer_account.add_transaction(transaction)
                payee_account.add_transaction(transaction)


if __name__ == "__main__":
    ledger = Ledger("transactions.csv")

    for account_name, account in ledger.accounts:
        print()
        print(account_name)
        print("-" * len(account_name))
        for account_transaction in account.transactions:
            print(
                account_transaction, account.get_balance(account_transaction.date),
            )
