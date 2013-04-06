from datetime import timedelta
import unittest2 as unittest

from mtj.f3u1.factory import units_factory, UnitGroup


class FactoryTestCase(unittest.TestCase):
    """
    Unit tests for the units_factory function.
    """

    def test_factory_construct_fail(self):
        self.assertRaises(AssertionError, units_factory, 'fail', 1, object())

    def test_factory_normal(self):
        unit = units_factory('unit', 1)
        self.assertEqual(unit(0), ['0 unit'])
        unit = units_factory('unit', 1, plural='units')
        self.assertEqual(unit(0), ['0 units'])
        self.assertEqual(unit(1), ['1 unit'])

    def test_factory_chained(self):
        ten = units_factory('ten', 10, plural='tens')
        unit = units_factory('unit', 1, higher_unit=ten, plural='units')
        self.assertEqual(unit(0), ['0 units'])
        self.assertEqual(unit(9), ['9 units'])
        self.assertEqual(ten(9), ['0 tens'])
        self.assertEqual(unit(10), ['1 ten'])
        self.assertEqual(ten(10), ['1 ten'])
        self.assertEqual(unit(11), ['1 ten', '1 unit'])
        self.assertEqual(unit(20), ['2 tens'])

    def test_factory_base_omissible(self):
        # this really means blank value on empty.
        unit = units_factory('unit', 1, omissible=True)
        self.assertEqual(unit(0), [])
        self.assertEqual(unit(1), ['1 unit'])
        ten = units_factory('ten', 10, omissible=True)
        unit = units_factory('unit', 1, higher_unit=ten, omissible=True)
        self.assertEqual(ten(9), [])
        self.assertEqual(ten(10), ['1 ten'])

    def test_factory_higher_omissible(self):
        unit = units_factory('unit', 1, force_render=True)
        self.assertEqual(unit(0), ['0 unit'])
        self.assertEqual(unit(1), ['1 unit'])
        hundred = units_factory('hundred', 100, force_render=True)
        ten = units_factory('ten', 10, higher_unit=hundred,
            force_render=True)
        unit = units_factory('unit', 1, higher_unit=ten,
            force_render=True)

        self.assertEqual(ten(9), ['0 hundred', '0 ten'])
        self.assertEqual(unit(0), ['0 hundred', '0 ten', '0 unit'])
        self.assertEqual(unit(9), ['0 hundred', '0 ten', '9 unit'])

        self.assertEqual(unit(10), ['0 hundred', '1 ten', '0 unit'])
        self.assertEqual(ten(10), ['0 hundred', '1 ten'])

    def test_factory_higher_irregular(self):
        gross = units_factory('gross', 144)
        hundred = units_factory('hundred', 100, higher_unit=gross)
        dozen = units_factory('dozen', 12, higher_unit=hundred)
        ten = units_factory('ten', 10, higher_unit=dozen)
        unit = units_factory('unit', 1, higher_unit=ten)

        self.assertEqual(unit(9), ['9 unit'])
        self.assertEqual(unit(10), ['1 ten'])
        self.assertEqual(unit(12), ['1 dozen'])
        self.assertEqual(unit(23), ['1 dozen', '1 ten', '1 unit'])
        self.assertEqual(unit(24), ['2 dozen'])
        self.assertEqual(unit(26), ['2 dozen', '2 unit'])
        self.assertEqual(unit(99), ['8 dozen', '3 unit'])
        self.assertEqual(unit(100), ['1 hundred'])
        self.assertEqual(unit(111), ['1 hundred', '1 ten', '1 unit'])
        self.assertEqual(unit(112), ['1 hundred', '1 dozen'])
        self.assertEqual(unit(143), ['1 hundred', '3 dozen', '7 unit'])
        self.assertEqual(unit(144), ['1 gross'])
        self.assertEqual(unit(150), ['1 gross', '6 unit'])
        self.assertEqual(unit(155), ['1 gross', '1 ten', '1 unit'])
        self.assertEqual(unit(156), ['1 gross', '1 dozen'])
        self.assertEqual(unit(287),
            ['1 gross', '1 hundred', '3 dozen', '7 unit'])
        self.assertEqual(unit(288), ['2 gross'])


class UnitGroupTestCase(unittest.TestCase):
    """
    Unit tests for the UnitGroup class.
    """

    def test_construction(self):
        timeug = UnitGroup(base_unit='second',
            ratios={
                'week': 604800,
                'day': 86400,
                'hour': 3600,
                'minute': 60,
            },
            plurals={
                'week': 'weeks',
                'day': 'days',
                'minute': 'minutes',
                'hour': 'hours',
                'second': 'seconds',
            }
        )
        self.assertEqual(timeug.units['hour'](86461), ['1 day'])
        self.assertEqual(timeug.units['hours'](90061), ['1 day', '1 hour'])
        self.assertEqual(timeug.units['week'](90061), ['0 weeks'])
        self.assertEqual(timeug.units['second'](1940464),
            ['3 weeks', '1 day', '11 hours', '1 minute', '4 seconds'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FactoryTestCase))
    return suite
