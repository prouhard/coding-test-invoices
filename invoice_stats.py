from statistics import mean, median
from typing import List

import math

from errors import (
    InvalidAmountInvoiceError,
    MaximumNumberOfInvoicesReached,
    NonPositiveInvoiceError,
    NotANumberInvoiceError,
    TooLargeInvoiceError,
)


class InvoiceStats:

    # Maximum number of invoices to be stored
    _MAX_INVOICES: int = 20_000_000

    # Maximum allowed value for an invoice
    _MAX_INVOICE_VALUE: float = 200_000_000.0

    # Instance-level storage of the added invoices.
    _invoices: List[float]

    # Tracking of the storage's length to avoid computing it
    # each time an invoice is added
    _current_invoices_size: int

    def __init__(self):
        """
        Initialize the storage and length counter
        """
        self.clear()

    def add_invoices(self, invoices: List[float]) -> None:
        """
        Add a list of invoices, in dollars and cents

        Arguments:
            - `invoices`: a list of invoices

        Examples:
            - [10.20, 10_000]
            - [500.00]
        """

        for invoice in invoices:
            self.add_invoice(invoice)

    def add_invoice(self, invoice: float) -> None:
        """
        Add a single invoice, in dollars and cents

        Arguments:
            - `invoice`: an invoice

        Examples:
            - 10.20
            - 10_000
        """

        self._raise_for_max_invoices_reached()
        self._raise_for_invalid_invoice(invoice)
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

        raw_median = median(self._invoices)

        # If `raw_median` has more than 2 decimals, it is the mean
        # of 2 invoices, which have at most 2 decimals each, so
        # the 3rd digit represents half a cent, which we truncate.

        return self._truncate_to_two_decimals(raw_median)

    def get_mean(self) -> float:
        """
        Find the mean value of the invoices, to the nearest cent.
        Half a cent should round down.
        """

        raw_mean = mean(self._invoices)
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

    def _raise_for_invalid_invoice(self, invoice: float) -> None:
        """
        Check that the invoice amount is (or raise):
            - a valid number (`NotANumberInvoiceError`)
            - nonnegative (`InvalidAmountInvoiceError`)
            - at most a 2-decimals float (`NonPositiveInvoiceError`)
            - less than the maximum value (`TooLargeInvoiceError`)
        """

        # Check that invoice is a valid number
        if not isinstance(invoice, (int, float)) or not math.isfinite(invoice):
            raise NotANumberInvoiceError

        # Check that invoice is positive
        if invoice <= 0.0:
            raise NonPositiveInvoiceError

        # Check that invoice is at most a 2-decimals float
        if self._truncate_to_two_decimals(invoice) != invoice:
            raise InvalidAmountInvoiceError

        # Check that invoice is less than the maximum allowed value
        if invoice >= self._MAX_INVOICE_VALUE:
            raise TooLargeInvoiceError(self._MAX_INVOICE_VALUE)

    @staticmethod
    def _truncate_to_two_decimals(invoice: float) -> float:
        """
        Truncates the incoming invoice to two decimals

        Argument:
            - `invoice`: the invoice to truncate

        Examples:
            - 23.456 -> 23.45
            - 23.45 -> 23.45
            - 23 -> 23
        """

        return math.floor(invoice * 100) / 100
