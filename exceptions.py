"""This module contains custom exceptions for the Ledger program."""


class Error(Exception):
    """ Base Exception Class """

    pass


class AccountError(Error):
    """ An error raised by the Account class """

    pass
