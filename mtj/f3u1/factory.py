from sys import maxint

def units_factory(subject, size, higher_unit=None, plural=None,
        omissible=False, force_render=False):
    """
    A function that returns a function that will format a number with its
    units.

    Parameters:

    subject
        The name of the unit to be displayed
    size
        The size of this unit in relation to the base unit.
    higher_unit
        A function generated using this method that represents the next
        higher unit of measurement for this unit type.
    plural
        The plural form of the name of this unit.
    omissible
        Whether this output is omissible if the size is 0.
        Default is False.
    force_render
        Whether to forcibly render all units regardless of size.
        Default is False.
    """

    assert higher_unit is None or callable(higher_unit)

    if plural is None:
        plural = subject

    def unit_method(value, omissible=omissible):
        if higher_unit:
            result = higher_unit(value, omissible=True)
            higher_size = higher_unit.size
        else:
            result = []
            higher_size = maxint

        remainder = value % higher_size
        derived = int(remainder / size)
        if (force_render or (value >= size and derived != 0) or
                not (omissible or result)):
            result.append('%d %s' % (derived,
                derived == 1 and subject or plural))
        return result

    unit_method.__name__ = subject
    unit_method.size = size
    return unit_method


class UnitGroupAttr(object):
    def __init__(self, unit_group):
        for k, v in unit_group.units.iteritems():
            setattr(self, k, v)


class UnitGroup(object):
    """
    Instances of this class is constructed using a list of definitions
    for a set of related, regular units (in decreasing order) and
    constructs an object with parameters with the name of the units,
    that when invoked, will return a human readable string down to that
    particular unit's size.

    See the accompanied units module for more examples.
    """

    def __init__(self, base_unit, ratios, plurals=None):
        self.base_unit = base_unit

        self.ratios = {}
        self.ratios.update(ratios)
        self.ratios[base_unit] = 1

        self.plurals = plurals or {}

        self.units = {}
        self.initialize()

    def initialize(self):
        self.units = {}
        builddef = sorted(self.ratios.items(),
            cmp=lambda x, y: cmp(y[1], x[1]))

        last = None
        for subject, size in builddef:
            plural = self.plurals.get(subject, subject)
            last = units_factory(subject, size=size, higher_unit=last,
                plural=plural)
            self.units[subject] = last
            self.units[plural] = last

    def as_attrs(self):
        return UnitGroupAttr(self)

    # TODO make this callable, or heck, another factory that will return
    # an object that will let user have a more friendlier way to
    # fine-tune their desired input (specifying all the units) and then
    # control the output to be some kind of string.
