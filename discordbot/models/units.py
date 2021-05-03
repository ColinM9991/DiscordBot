class PressureUnit:
    def __init__(self, value: float):
        self.__value = value

    @property
    def value(self):
        return self.__value


class Pascal(PressureUnit):
    def __init__(self, value: float):
        super().__init__(value)

    @staticmethod
    def from_hectopascal(hecto_pascal: float):
        return Pascal(hecto_pascal * 100)

    def to_torr(self):
        return Torr.from_pascal(self)


class Torr(PressureUnit):
    def __init__(self, value: float):
        super().__init__(value)

    @staticmethod
    def from_pascal(pascal: Pascal):
        return Torr(pascal.value * 0.00750062)

    def to_inch_of_mercury(self):
        return InchOfMercury.from_torr(self)


class InchOfMercury(PressureUnit):
    def __init__(self, value: float):
        super().__init__(value)

    @staticmethod
    def from_torr(torr: Torr):
        return InchOfMercury(torr.value * 0.0393701)
