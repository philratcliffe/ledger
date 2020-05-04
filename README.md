
# Ledger
A program, written in Python3, to keep track of financial transactions between
different parties — people and organisations. These parties are identified by
a simple string such as "john" or "supermarket". Each record in the ledger is
in the format: transaction date, payer, payee, amount.

The ledger of transactions looks like this:

```
2015-01-16,john,mary,125.00
2015-01-17,john,supermarket,20.00
2015-01-17,mary,insurance,100.00
```

## Requirements
Python 3 

## Using from the REPL
Below is an example of using the program from the REPL.
```pycon
>>> from ledger import Ledger
>>> l = Ledger('transactions.csv') 
>>> for name, _ in l.accounts:
>>>     print(name)
...
john
mary
supermarket
insurance
bob
alice
eve
>>> account=l.accounts.get_account('john')
>>> account.get_balance('2015-01-16')
-125
``` 

## Example
A simple example program can be run from the command line,
```bash
$ python ledger.py 
```

## Tests
To run the tests,
```bash
$ cd tests
$ python tests.py 
```


