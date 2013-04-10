from datetime import timedelta
import unittest2 as unittest

from mtj.f3u1.units import Time


class TimeUnitTestCase(unittest.TestCase):
    """
    Unit tests for the original hour-based requirements.
    """

    def test_zeros(self):
        self.assertEqual(Time.second(0), [('second', 0)])
        self.assertEqual(Time.second(0), [('second', 0)])
        self.assertEqual(Time.minute(0), [('minute', 0)])
        self.assertEqual(Time.minute(0), [('minute', 0)])
        self.assertEqual(Time.hour(0), [('hour', 0)])
        self.assertEqual(Time.hour(0), [('hour', 0)])
        self.assertEqual(Time.day(0), [('day', 0)])
        self.assertEqual(Time.day(0), [('day', 0)])
        # Duplicates abound but whatever.

    def test_singular(self):
        self.assertEqual(Time.second(1), [('second', 1)])
        self.assertEqual(Time.second(1), [('second', 1)])

    def test_plural(self):
        self.assertEqual(Time.second(2), [('second', 2)])

    def test_almost_next(self):
        self.assertEqual(Time.second(59), [('second', 59)])
        self.assertEqual(Time.minute(59), [('minute', 0)])

    def test_minute(self):
        self.assertEqual(Time.second(60), [('minute', 1)])
        self.assertEqual(Time.minute(60), [('minute', 1)])

    def test_minute_plusone(self):
        self.assertEqual(Time.second(61), [('minute', 1), ('second', 1)])
        self.assertEqual(Time.minute(61), [('minute', 1)])

    def test_day_minusone(self):
        self.assertEqual(Time.second(86399),
            [('hour', 23), ('minute', 59), ('second', 59)])
        self.assertEqual(Time.minute(86399), [('hour', 23), ('minute', 59)])
        self.assertEqual(Time.hour(86399), [('hour', 23)])
        self.assertEqual(Time.day(86399), [('day', 0)])

    def test_day(self):
        self.assertEqual(Time.second(86400), [('day', 1)])
        self.assertEqual(Time.minute(86400), [('day', 1)])
        self.assertEqual(Time.hour(86400), [('day', 1)])
        self.assertEqual(Time.day(86400), [('day', 1)])

    def test_day_pluseone(self):
        self.assertEqual(Time.second(86401), [('day', 1), ('second', 1)])
        self.assertEqual(Time.minute(86401), [('day', 1)])
        self.assertEqual(Time.hour(86401), [('day', 1)])
        self.assertEqual(Time.day(86401), [('day', 1)])

    def test_day_pluseoneminute(self):
        self.assertEqual(Time.second(86460), [('day', 1), ('minute', 1)])
        self.assertEqual(Time.minute(86460), [('day', 1), ('minute', 1)])
        self.assertEqual(Time.hour(86460), [('day', 1)])
        self.assertEqual(Time.day(86460), [('day', 1)])

    def test_day_pluseonehour(self):
        self.assertEqual(Time.second(90000), [('day', 1), ('hour', 1)])
        self.assertEqual(Time.minute(90000), [('day', 1), ('hour', 1)])
        self.assertEqual(Time.hour(90000), [('day', 1), ('hour', 1)])
        self.assertEqual(Time.day(90000), [('day', 1)])

    def test_more(self):
        self.assertEqual(Time.second(901101),
            [('day', 10), ('hour', 10), ('minute', 18), ('second', 21)])
        self.assertEqual(Time.minute(901101),
            [('day', 10), ('hour', 10), ('minute', 18)])
        self.assertEqual(Time.hour(901101), [('day', 10), ('hour', 10)])
        self.assertEqual(Time.day(901101), [('day', 10)])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TimeUnitTestCase))
    return suite
