import unittest

from errors import (
    InvalidAmountInvoiceError,
    MaximumNumberOfInvoicesReached,
    NonPositiveInvoiceError,
    NotANumberInvoiceError,
    TooLargeInvoiceError,
)
from invoice_stats import InvoiceStats


class TestInvoiceStats(unittest.TestCase):

    def test_add_invoice_ok(self):
        """
        It should add an invoice to the `InvoiceStats` storage.
        """
        valid_invoice = 10_000.00
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoice(valid_invoice)

        self.assertListEqual(invoice_stats._invoices, [valid_invoice])

    def test_add_invoice_negative_raise_non_positive_invoice_error(self):
        """
        It should raise a `NonPositiveInvoiceError` error.
        """
        negative_invoice = -1.00
        invoice_stats = InvoiceStats()

        with self.assertRaises(NonPositiveInvoiceError):
            invoice_stats.add_invoice(negative_invoice)

    def test_add_invoice_nan_large_raise_nan_invoice_error(self):
        """
        It should raise a `NotANumberInvoiceError` error.
        """
        nan_invoice = float('nan')
        invoice_stats = InvoiceStats()

        with self.assertRaises(NotANumberInvoiceError):
            invoice_stats.add_invoice(nan_invoice)

    def test_add_invoice_three_digits_raise_invalid_amount_invoice_error(self):
        """
        It should raise a `InvalidAmountInvoiceError` error.
        """
        three_digits_invoice = 1.234
        invoice_stats = InvoiceStats()

        with self.assertRaises(InvalidAmountInvoiceError):
            invoice_stats.add_invoice(three_digits_invoice)

    def test_add_invoice_too_large_raise_too_large_invoice_error(self):
        """
        It should raise a `TooLargeInvoiceError` error.
        """
        too_large_invoice = 200_000_001.00
        invoice_stats = InvoiceStats()

        with self.assertRaises(TooLargeInvoiceError):
            invoice_stats.add_invoice(too_large_invoice)

    def test_add_invoice_raise_maximum_number_of_invoices_reached(self):
        """
        We shrink the `_MAX_INVOICES` value to 0
        It should raise a `MaximumNumberOfInvoicesReached` error.
        """
        invoice = 10_000.00
        invoice_stats = InvoiceStats()
        invoice_stats._MAX_INVOICES = 0

        with self.assertRaises(MaximumNumberOfInvoicesReached):
            invoice_stats.add_invoice(invoice)

    def test_add_invoices_ok(self):
        """
        It should add each invoice to the `InvoiceStats` storage.
        """
        invoices = [1000, 10_000.0, 100_000.00]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)

        self.assertListEqual(invoice_stats._invoices, invoices)

    def test_get_median_rounded_down(self):
        """
        It should compute the median of the added invoices.
        Half a cent should round down.
        Here, the raw median is 5.115, so `get_median` should return 5.11.
        """
        invoices = [1.23, 3.45, 6.78, 7.89]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)
        median = invoice_stats.get_median()

        self.assertEqual(median, 5.11)

    def test_get_mean_rounded_down(self):
        """
        It should compute the mean of the added invoices.
        Half a cent should round down.
        Here, the raw mean is 4.835, so `get_mean` should return 4.83.
        """
        invoices = [1.23, 3.45, 6.78, 7.88]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)
        mean = invoice_stats.get_mean()

        self.assertEqual(mean, 4.83)

    def test_get_median_not_rounded(self):
        """
        It should compute the median of the added invoices.
        Here, the raw median is 4.56, so `get_median` should return 4.56.
        """
        invoices = [1.23, 3.45, 4.56, 6.78, 7.89]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)
        median = invoice_stats.get_median()

        self.assertEqual(median, 4.56)

    def test_get_mean_rounded_up(self):
        """
        It should compute the mean of the added invoices.
        Here, the raw mean is 4.8375, so `get_mean` should return 4.84.
        """
        invoices = [1.23, 3.45, 6.78, 7.89]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)
        mean = invoice_stats.get_mean()

        self.assertEqual(mean, 4.84)
