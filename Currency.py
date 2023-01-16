class Privat24Currency:

    def __init__(self, ccy: str, buy_price: float = -1, sale_price: float = -1):
        self.ccy = ccy
        self.buy_price = buy_price
        self.sale_price = sale_price

    def __str__(self):
        return f"{self.ccy}\n" \
               f"Купівля: {self.buy_price:.2f}\n" \
               f"Продаж: {self.sale_price:.2f}"

    @property
    def ccy(self):
        return self._ccy

    @ccy.setter
    def ccy(self, value):
        if not isinstance(value, str):
            raise TypeError("ccy must be a string")
        self._ccy = value

    @property
    def buy_price(self):
        return self._buy_price

    @buy_price.setter
    def buy_price(self, value):
        # if not isinstance(value, int | float):
        #     raise TypeError("buy price must be a float or int")
        self._buy_price = float(value)

    @property
    def sale_price(self):
        return self._sale_price

    @sale_price.setter
    def sale_price(self, value):
        # if not isinstance(value, int | float):
        #     raise TypeError("sale price must be a float or int")
        self._sale_price = float(value)


class NbuCurrency:

    def __init__(self, cc, name=None, price=None):
        self.cc = cc
        self.name = name
        self.price = price

    @property
    def cc(self):
        return self._cc

    @cc.setter
    def cc(self, value):
        self._cc = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
