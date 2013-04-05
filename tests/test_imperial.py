from datetime import timedelta
import unittest2 as unittest

from mtj.f3u1.units import ImperialLength, ImperialWeight
from mtj.f3u1.timedelta import format_timedelta


class ImperialUnitsTestCase(unittest.TestCase):
    """
    Imperial units.
    """

    def test_length(self):
        self.assertEqual(ImperialLength.inch(14), ['1 foot', '2 inches'])
        self.assertEqual(ImperialLength.inch(25), ['2 feet', '1 inch'])
        self.assertEqual(ImperialLength.inch(63390),
            ['1 mile', '2 feet', '6 inches'])

    def test_weight(self):
        self.assertEqual(ImperialWeight.ounce(223), ['13 pounds', '15 ounces'])
        self.assertEqual(ImperialWeight.ounce(225), ['1 stone', '1 ounce'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ImperialUnitsTestCase))
    return suite
