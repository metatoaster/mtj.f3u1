from datetime import timedelta
import unittest2 as unittest

from mtj.f3u1.units import Time
from mtj.f3u1.timedelta import format_timedelta


class TimeUnitTestCase(unittest.TestCase):
    """
    Unit tests for the original hour-based requirements.
    """

    def assertJoinedEqual(self, first, second):
        self.assertEqual(', '.join(first), second)

    def test_zeros(self):
        self.assertJoinedEqual(Time.second(0), '0 seconds')
        self.assertJoinedEqual(Time.seconds(0), '0 seconds')
        self.assertJoinedEqual(Time.minute(0), '0 minutes')
        self.assertJoinedEqual(Time.minutes(0), '0 minutes')
        self.assertJoinedEqual(Time.hour(0), '0 hours')
        self.assertJoinedEqual(Time.hours(0), '0 hours')
        self.assertJoinedEqual(Time.day(0), '0 days')
        self.assertJoinedEqual(Time.days(0), '0 days')
        # Duplicates abound but whatever.

    def test_singular(self):
        self.assertJoinedEqual(Time.second(1), '1 second')
        self.assertJoinedEqual(Time.seconds(1), '1 second')

    def test_plural(self):
        self.assertJoinedEqual(Time.second(2), '2 seconds')

    def test_almost_next(self):
        self.assertJoinedEqual(Time.second(59), '59 seconds')
        self.assertJoinedEqual(Time.minute(59), '0 minutes')

    def test_minute(self):
        self.assertJoinedEqual(Time.second(60), '1 minute')
        self.assertJoinedEqual(Time.minute(60), '1 minute')

    def test_minute_plusone(self):
        self.assertJoinedEqual(Time.second(61), '1 minute, 1 second')
        self.assertJoinedEqual(Time.minute(61), '1 minute')

    def test_day_minusone(self):
        self.assertJoinedEqual(Time.second(86399),
            '23 hours, 59 minutes, 59 seconds')
        self.assertJoinedEqual(Time.minute(86399), '23 hours, 59 minutes')
        self.assertJoinedEqual(Time.hour(86399), '23 hours')
        self.assertJoinedEqual(Time.day(86399), '0 days')

    def test_day(self):
        self.assertJoinedEqual(Time.second(86400), '1 day')
        self.assertJoinedEqual(Time.minute(86400), '1 day')
        self.assertJoinedEqual(Time.hour(86400), '1 day')
        self.assertJoinedEqual(Time.day(86400), '1 day')

    def test_day_pluseone(self):
        self.assertJoinedEqual(Time.second(86401), '1 day, 1 second')
        self.assertJoinedEqual(Time.minute(86401), '1 day')
        self.assertJoinedEqual(Time.hour(86401), '1 day')
        self.assertJoinedEqual(Time.day(86401), '1 day')

    def test_day_pluseoneminute(self):
        self.assertJoinedEqual(Time.second(86460), '1 day, 1 minute')
        self.assertJoinedEqual(Time.minute(86460), '1 day, 1 minute')
        self.assertJoinedEqual(Time.hour(86460), '1 day')
        self.assertJoinedEqual(Time.day(86460), '1 day')

    def test_day_pluseonehour(self):
        self.assertJoinedEqual(Time.second(90000), '1 day, 1 hour')
        self.assertJoinedEqual(Time.minute(90000), '1 day, 1 hour')
        self.assertJoinedEqual(Time.hour(90000), '1 day, 1 hour')
        self.assertJoinedEqual(Time.day(90000), '1 day')

    def test_more(self):
        self.assertJoinedEqual(Time.second(901101),
            '10 days, 10 hours, 18 minutes, 21 seconds')
        self.assertJoinedEqual(Time.minute(901101),
            '10 days, 10 hours, 18 minutes')
        self.assertJoinedEqual(Time.hour(901101), '10 days, 10 hours')
        self.assertJoinedEqual(Time.day(901101), '10 days')


class FormatTimedeltaTestCase(unittest.TestCase):
    """
    Unit tests for the original format_timedelta method.

    Just really to show that the string based acquisition works.
    """

    def test_nothing(self):
        self.assertEqual(format_timedelta(seconds=0), '0 seconds')

    def test_hour(self):
        self.assertEqual(format_timedelta(seconds=180061, resolution='hour'),
            '2 days, 2 hours')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TimeUnitTestCase))
    suite.addTest(unittest.makeSuite(FormatTimedeltaTestCase))
    return suite
