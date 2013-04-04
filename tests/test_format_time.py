from datetime import timedelta
import unittest2 as unittest

from mtj.f3u1.timedelta import format_timedelta


class FormatTimeHourTestCase(unittest.TestCase):
    """
    Unit tests for the original hour-based requirements.
    """

    def test_0000_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=180000, resolution='hour'),
            '2 days, 2 hours')

    def test_0001_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=172800, resolution='hour'),
            '2 days')

    def test_0002_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=111600, resolution='hour'),
            '1 day, 7 hours')

    def test_0003_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=90000, resolution='hour'),
            '1 day, 1 hour')

    def test_0004_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=89999, resolution='hour'),
            '1 day')

    def test_0005_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=86401, resolution='hour'),
            '1 day')

    def test_0006_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=86400, resolution='hour'),
            '1 day')

    def test_0007_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=86399, resolution='hour'),
            '23 hours')

    def test_0008_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=3600, resolution='hour'),
            '1 hour')

    def test_0009_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=0, resolution='hour'),
            '0 hours')

    def test_0010_format_timedelta(self):
        self.assertEqual(format_timedelta(seconds=1, resolution='hour'),
            '0 hours')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FormatTimeHourTestCase))
    return suite
