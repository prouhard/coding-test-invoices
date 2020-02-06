class MaximumNumberOfInvoicesReached(Exception):
    """
    Raised when the storage of invoices reaches maximum capacity
    """
    def __init__(self, max_invoices):
        super().__init__(
            f"Maximum capacity of {max_invoices} invoices reached,"
            "consider clearing storage."
        )


class InvalidInvoiceError(Exception):
    """
    Base exception for errors coming from
    invalid invoices passed to `InvoiceStats`.
    """
    pass


class NonPositiveInvoiceError(InvalidInvoiceError):
    """
    Raised when an invoice is not positive.
    """
    def __init__(self):
        super().__init__(
            "Invoices amounts in dollar and cents must be positive numbers."
        )


class TooLargeInvoiceError(InvalidInvoiceError):
    """
    Raised when an invoice is larger than the maximum authorized value.
    """
    def __init__(self, max_invoice_value):
        super().__init__(f"Invoices must be less than {max_invoice_value}.")


class NotAnIntegerInvoiceError(InvalidInvoiceError):
    """
    Raised when an invoice amount is not a valid integer.
    """
    def __init__(self):
        super().__init__(
            f"Invoices amounts in dollars and cents must be valid integers."
        )
