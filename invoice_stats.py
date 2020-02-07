from typing import List

import math
import statistics

from errors import MaximumNumberOfInvoicesReached
from invoice import Invoice


class InvoiceStats:

    # Maximum number of invoices to be stored
    _MAX_INVOICES: int = 20_000_000

    # Instance-level storage of the added invoices.
    _invoices: List[Invoice]

    # Tracking of the storage's length to avoid computing it
    # each time an invoice is added
    _current_invoices_size: int

    def __init__(self):
        """
        Initialize the storage and length counter
        """
        self.clear()

    def add_invoices(self, invoices: List[Invoice]) -> None:
        """
        Add a list of invoices, in dollars and cents

        Arguments:
            - `invoices`: a list of invoices

        Examples:
            - [Invoice(10, 20), Invoice(10, 0)]
            - [Invoice(500, 0)]
        """

        for invoice in invoices:
            self.add_invoice(invoice)

    def add_invoice(self, invoice: Invoice) -> None:
        """
        Add a single invoice, a tuple of dollars and cents

        Arguments:
            - `invoice`: an invoice

        Examples:
            - Invoice(dollars=10_000, cents=0)
            - Invoice(10, 20)
        """

        self._raise_for_max_invoices_reached()
        invoice.raise_for_invalid_amounts()

        self._invoices.append(invoice)
        self._current_invoices_size += 1

    def clear(self) -> None:
        """
        Remove all stored invoice data and reset length counter
        """

        self._invoices = []
        self._current_invoices_size = 0

    def get_median(self) -> float:
        """
        Find the median value (https://en.wikipedia.org/wiki/Median)
        of the added invoices, to the nearest cent.
        Half a cent should round down.
        """

        raw_median = statistics.median(
            (
                invoice.as_amount()
                for invoice in self._invoices
            )
        )

        # If `raw_median` has more than 2 decimals, it is the mean
        # of 2 invoices, which have at most 2 decimals each, so
        # the 3rd digit represents half a cent, which we truncate.

        return self._truncate_to_two_decimals(raw_median)

    def get_mean(self) -> float:
        """
        Find the mean value of the invoices, to the nearest cent.
        Half a cent should round down.
        """

        raw_mean = statistics.mean(
            (
                invoice.as_amount()
                for invoice in self._invoices
            )
        )
        truncated_mean = self._truncate_to_two_decimals(raw_mean)

        # Check if we are in the first half of the cent
        # If so, return rounded down (or truncated here) value
        if raw_mean <= truncated_mean + 0.005:
            return truncated_mean

        # Else, return rounded up value
        return round(raw_mean, 2)

    def _raise_for_max_invoices_reached(self) -> None:
        """
        Check that the maximum capacity of the storage is not reached

        Raise:
            - `MaximumNumberOfInvoicesReached`
        """

        if self._current_invoices_size >= self._MAX_INVOICES:
            raise MaximumNumberOfInvoicesReached(self._MAX_INVOICES)

    @staticmethod
    def _truncate_to_two_decimals(number: float) -> float:
        """
        Truncates the incoming number to two decimals

        Argument:
            - `number`: the number to truncate

        Examples:
            - 23.456 -> 23.45
            - 23.45 -> 23.45
            - 23 -> 23
        """

        return math.floor(number * 100) / 100
