class InvalidInvoiceError(Exception):
    """
    Raised when an invoice is not valid.
    """
    def __init__(self, message, code):
        super().__init__(f"[Error]: {message} (code {code})")
        self.code = code


class MaximumNumberOfInvoicesReached(Exception):
    """
    Raised when the storage of invoices reaches maximum capacity
    """
    def __init__(self, max_invoices):
        super().__init__(
            f"Maximum capacity of {max_invoices} invoices reached,"
            "consider clearing storage."
        )
        self.code = 4
