## Coding Test - InvoiceStats

Invoices are agreements to transfer money between companies. We need a python class to aggregate and gather basic stats on the invoices we process. Your task is to write this class.

Write a python class, `InvoiceStats`, along with suitable tests, which supports the following methods:
- `add_invoices` - add a list of invoices, in dollars and cents
- `add_invoice` - add a single invoice, in dollars and cents.
- `clear` - remove all stored invoice data.
- `get_median` - find the median value (https://en.wikipedia.org/wiki/Median) of the added invoices, to the nearest cent. Half a cent should round down.
- `get_mean` - find the mean value of the invoices, to the nearest cent. Half a cent should round down.

**Constraints:**
- Valid invoice values v are 0 < v < $200,000,000.00 and must be a whole number of dollars and cents.
- Adding non valid invoice value(s) should raise an exception.
- You may decide what data type(s) to use to best represent the invoice amounts.
- Maximum number of invoices is 20,000,000
- Assume the machine the code is running on will not crash, so no need to persist data.
- You may use (non standard) third party libraries. If so, please include details of them, including why you used them.
- Your code will be judged on scalability, clarity, readability, accuracy, test coverage, performance and robustness


## Files

- `errors.py`: user-defined errors to raise when facing invalid invoices
- `invoice.py`: custom `Invoice` class to represent invoices
- `invoice_stats.py`: implementation of the `InvoiceStats` class
- `test_invoice_stats.py`: unit tests


## Test locally

Every package used is from the standard library, to run the tests just launch (tested with python==3.7.2):
`python3 -m unittest test_invoice_stats.py`