from errors import InvalidInvoiceError


class Invoice:

    # Maximum allowed amount for an invoice
    _MAX_INVOICE_AMOUNT: int = 200_000_000

    # Instance attributes
    dollars: int
    cents: int

    def __init__(self, dollars: int, cents: int):
        self.dollars = dollars
        self.cents = cents

    def as_amount(self) -> float:
        """
        Converts itself into a valid amount
        """
        return self.dollars + self.cents / 100

    def raise_for_invalid_amounts(self) -> None:
        """
        Check that the invoice amounts in dollars and cents are:
            - valid integers
            - nonnegative
            - less than the maximum value

        Else, raise `InvalidInvoiceError`
        """

        # Check that invoice amounts are valid integers
        if (
            not isinstance(self.dollars, int) or
            not isinstance(self.cents, int)
        ):
            raise InvalidInvoiceError(
                "Dollars and cents must be integer values",
                code=1
            )

        # Check that the total invoice is positive
        if self.cents < 0 or self.as_amount() <= 0:
            raise InvalidInvoiceError(
                "Dollars and cents cannot have negative values",
                code=2
            )

        # Check that the total invoice is less than the maximum allowed value
        if self.as_amount() >= self._MAX_INVOICE_AMOUNT:
            raise InvalidInvoiceError(
                f"Invoices cannot be greate thant {self._MAX_INVOICE_AMOUNT}",
                code=3
            )
