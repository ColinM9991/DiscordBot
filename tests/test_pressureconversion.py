import unittest

from models.units import Pascal


class PressureConversionTests(unittest.TestCase):
    """ Converting an hPa value of 993 to Pascal, Torr and inHg should convert to the expected values """

    def __init__(self, method_name):
        super().__init__(method_name)

        hectopascal = 993

        self.pascal = Pascal.from_hectopascal(hectopascal)
        self.torr = self.pascal.to_torr()
        self.inch_of_mercury = self.torr.to_inch_of_mercury()

    def test_from_hectopascal(self):
        self.assertEqual(99300, self.pascal.value)

    def test_to_torr(self):
        self.assertEqual(744.811566, round(self.torr.value, 6))

    def test_to_inch_of_mercury(self):
        self.assertEqual(29.32, round(self.inch_of_mercury.value, 2))
