import string


class CustomNotation(str):

    symbols = f'{string.digits}{string.ascii_letters}'

    @property
    def base(self):
        return len(self.symbols)

    def convert_to_decimal_notation(self):
        return sum([self.symbols.index(i) * self.base ** j for j, i in enumerate(self[::-1])])

    def convert_from_decimal_notation(self, decimal_number: int):
        x, y = decimal_number // self.base, self.symbols[decimal_number % self.base]
        return y if x == 0 else f'{self.convert_from_decimal_notation(x)}{y}'
