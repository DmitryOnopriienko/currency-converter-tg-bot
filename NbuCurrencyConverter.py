from Currency import NbuCurrency


class NbuCurrencyConverter:

    def __init__(self):
        self.base_cc: NbuCurrency = None
        self.base_amount = 0
        self.cc_to: NbuCurrency = None

    def __str__(self):
        return f"{self.base_amount:.2f} {self.base_cc.cc} ({self.base_cc.name}):\n" \
               f"{self.converted_amount:.2f} {self.cc_to.cc} ({self.cc_to.name})"

    @property
    def base_cc(self):
        return self._base_cc

    @base_cc.setter
    def base_cc(self, value: NbuCurrency):
        self._base_cc = value

    @property
    def cc_to(self):
        return self._cc_to

    @cc_to.setter
    def cc_to(self, value: NbuCurrency):
        self._cc_to = value

    @property
    def base_amount(self):
        return self._base_amount

    @base_amount.setter
    def base_amount(self, value):
        self._base_amount = value

    @property
    def converted_amount(self):
        if not self.base_amount or not self.cc_to or not self.base_cc:
            raise ValueError("All fields must be set before converting (base_amount, cc_to, base_cc)")
        amount_in_uah = self.base_amount * self.base_cc.price
        return amount_in_uah / self.cc_to.price


# nbuCurrency1 = NbuCurrency("EUR", "Euro", 45.00)
# nbuCurrency2 = NbuCurrency("USD", "US Dollar", 38.00)
# converter = NbuCurrencyConverter()
# converter.base_cc = nbuCurrency1
# converter.cc_to = nbuCurrency2
# converter.base_amount = 10
# print(converter)
