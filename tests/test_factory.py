from datetime import timedelta
import unittest2 as unittest

from mtj.f3u1.factory import units_factory, UnitGroup
from mtj.f3u1.units import _plurals


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

    def setUp(self):
        self.time_ratios = {
            'week': 604800,
            'day': 86400,
            'hour': 3600,
            'minute': 60,
        }
        self.plurals = {'week': 'weeks', 'month': 'months'}
        self.plurals.update(_plurals)

    def test_construction(self):
        timeug = UnitGroup(base_unit='second', ratios=self.time_ratios,
            plurals=self.plurals,
        )
        self.assertEqual(timeug.units['hour'](86461), ['1 day'])
        self.assertEqual(timeug.units['hours'](90061), ['1 day', '1 hour'])
        self.assertEqual(timeug.units['week'](90061), ['0 weeks'])
        self.assertEqual(timeug.units['second'](1940464),
            ['3 weeks', '1 day', '11 hours', '1 minute', '4 seconds'])

    def test_construction_baseunit_redefinition_omitted(self):
        ug = UnitGroup(base_unit='second', ratios={
                'hour': 3600,
                'second': 60,
            },
            plurals=self.plurals,
        )
        self.assertEqual(ug.units['second'](71), ['71 seconds'])

        # To show the difference
        ug = UnitGroup(base_unit='nope', ratios={
                'hour': 3600,
                'second': 60,
            },
            plurals=self.plurals,
        )
        self.assertEqual(ug.units['nope'](71), ['1 second', '11 nope'])

    def test_respecify_new_ratio(self):
        timeug = UnitGroup(base_unit='second', ratios=self.time_ratios,
            plurals=self.plurals,
        )
        # original
        self.assertEqual(timeug.units['second'](9954862),
            ['16 weeks', '3 days', '5 hours', '14 minutes', '22 seconds'])
        self.assertEqual(timeug.units['second'](2592000),
            ['4 weeks', '2 days'])
        self.assertEqual(timeug.units['second'](3196800),
            ['5 weeks', '2 days'])
        self.assertEqual(timeug.units['second'](7775940),
            ['12 weeks', '5 days', '23 hours', '59 minutes'])

        monthug = timeug.respecify({'month': 2592000})
        self.assertEqual(monthug.units['second'](2592000),
            ['1 month'])
        self.assertEqual(monthug.units['second'](3196800),
            ['1 month', '1 week'])
        self.assertEqual(monthug.units['second'](7775940),
            ['2 months', '4 weeks', '1 day', '23 hours', '59 minutes'])

    def test_respecify_new_ratio_keep(self):
        timeug = UnitGroup(base_unit='second', ratios=self.time_ratios,
            plurals=self.plurals,
        )
        # can't filter base units out.
        monthug = timeug.respecify({'month': 2592000}, keep_only=['month'])
        self.assertEqual(monthug.units['second'](2592000),
            ['1 month'])
        self.assertEqual(monthug.units['second'](3196800),
            ['1 month', '604800 seconds'])

    def test_respecify_drop(self):
        timeug = UnitGroup(base_unit='second', ratios=self.time_ratios,
            plurals=self.plurals,
        )
        # can't drop base units.
        monthug = timeug.respecify({'month': 2592000}, drop=['week', 'second'])
        self.assertEqual(sorted(monthug.ratios.keys()),
            ['day', 'hour', 'minute', 'month', 'second'])
        self.assertEqual(monthug.units['second'](2592000),
            ['1 month'])
        self.assertEqual(monthug.units['second'](3196801),
            ['1 month', '7 days', '1 second'])

    def test_respecify_new_ratio_and_drop(self):
        timeug = UnitGroup(base_unit='second', ratios=self.time_ratios,
            plurals=self.plurals,
        )
        # can't filter base units out.
        monthug = timeug.respecify({'month': 2592000}, keep_only=['month'],
            drop=['month'])
        self.assertEqual(sorted(monthug.ratios.keys()), ['second'])
        self.assertEqual(monthug.units['second'](2592000),
            ['2592000 seconds'])


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(FactoryTestCase))
    suite.addTest(unittest.makeSuite(UnitGroupTestCase))
    return suite
