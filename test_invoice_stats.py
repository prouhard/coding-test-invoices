import unittest

from errors import InvalidInvoiceError, MaximumNumberOfInvoicesReached
from invoice import Invoice
from invoice_stats import InvoiceStats


class TestInvoiceStats(unittest.TestCase):

    def test_add_invoice_ok(self):
        """
        It should add an invoice to the `InvoiceStats` storage.
        """
        valid_invoice = Invoice(10_000, 0)
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoice(valid_invoice)

        self.assertListEqual(invoice_stats._invoices, [valid_invoice])

    def test_add_invoice_float_raise_invalid_invoice_error(self):
        """
        Invoice's dollars is not an integer.
        It should raise a `InvalidInvoiceError` error.
        """
        nan_invoice = Invoice(1.1, 0)
        invoice_stats = InvoiceStats()

        with self.assertRaises(InvalidInvoiceError) as context:
            invoice_stats.add_invoice(nan_invoice)

        self.assertEqual(context.exception.code, 1)

    def test_add_invoice_negative_raise_invalid_invoice_error(self):
        """
        Invoice's dollars amount is negative.
        It should raise a `InvalidInvoiceError` error.
        """
        negative_invoice = Invoice(-1, 0)
        invoice_stats = InvoiceStats()

        with self.assertRaises(InvalidInvoiceError) as context:
            invoice_stats.add_invoice(negative_invoice)

        self.assertEqual(context.exception.code, 2)

    def test_add_invoice_too_large_raise_invalid_invoice_error(self):
        """
        Invoice's amount is greater than maximum allowed value.
        It should raise a `InvalidInvoiceError` error.
        """
        too_large_invoice = Invoice(200_000_000, 1)
        invoice_stats = InvoiceStats()

        with self.assertRaises(InvalidInvoiceError) as context:
            invoice_stats.add_invoice(too_large_invoice)

        self.assertEqual(context.exception.code, 3)

    def test_add_invoice_raise_maximum_number_of_invoices_reached(self):
        """
        We shrink the `_MAX_INVOICES` value to 0
        It should raise a `MaximumNumberOfInvoicesReached` error.
        """
        invoice = Invoice(10_000, 0)
        invoice_stats = InvoiceStats()
        invoice_stats._MAX_INVOICES = 0

        with self.assertRaises(MaximumNumberOfInvoicesReached) as context:
            invoice_stats.add_invoice(invoice)

        self.assertEqual(context.exception.code, 4)

    def test_add_invoices_ok(self):
        """
        It should add each invoice to the `InvoiceStats` storage.
        """
        invoices = [
            Invoice(1000, 1),
            Invoice(10_000, 2),
            Invoice(100_000, 10)
        ]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)

        self.assertListEqual(invoice_stats._invoices, invoices)

    def test_get_median_rounded_down(self):
        """
        It should compute the median of the added invoices.
        Half a cent should round down.
        Here, the raw median is 5.115, so `get_median` should return 5.11.
        """
        invoices = [
            Invoice(1, 23),
            Invoice(3, 45),
            Invoice(6, 78),
            Invoice(7, 89)
        ]
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
        invoices = invoices = [
            Invoice(1, 23),
            Invoice(3, 45),
            Invoice(6, 78),
            Invoice(7, 88)
        ]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)
        mean = invoice_stats.get_mean()

        self.assertEqual(mean, 4.83)

    def test_get_median_not_rounded(self):
        """
        It should compute the median of the added invoices.
        Here, the raw median is 4.56, so `get_median` should return 4.56.
        """
        invoices = [
            Invoice(1, 23),
            Invoice(3, 45),
            Invoice(4, 56),
            Invoice(6, 78),
            Invoice(7, 89)
        ]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)
        median = invoice_stats.get_median()

        self.assertEqual(median, 4.56)

    def test_get_mean_rounded_up(self):
        """
        It should compute the mean of the added invoices.
        Here, the raw mean is 4.8375, so `get_mean` should return 4.84.
        """
        invoices = [
            Invoice(1, 23),
            Invoice(3, 45),
            Invoice(6, 78),
            Invoice(7, 89)
        ]
        invoice_stats = InvoiceStats()
        invoice_stats.add_invoices(invoices)
        mean = invoice_stats.get_mean()

        self.assertEqual(mean, 4.84)
