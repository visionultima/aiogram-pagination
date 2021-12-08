from ..utils.custom_notation import CustomNotation


class Counter:
    def __init__(self):
        self.count = CustomNotation('0')

    def increment(self):
        self.count = CustomNotation(
            self.count.convert_from_decimal_notation(
                self.count.convert_to_decimal_notation() + 1
            )
        )

    def nullify(self):
        self.count = CustomNotation('0')
