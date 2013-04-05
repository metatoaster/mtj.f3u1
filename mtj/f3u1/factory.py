from sys import maxint

def units_factory(subject, size, higher_unit=None, plural=None,
        omissible=False, higher_omissible=True):
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
    higher_omissible
        Whether the higher order value is omissible.
        Default is True.
    """

    assert higher_unit is None or callable(higher_unit)

    if plural is None:
        plural = subject

    def unit_method(value, omissible=omissible):
        if higher_unit:
            result = higher_unit(value, omissible=higher_omissible)
            higher_size = higher_unit.size
        else:
            result = []
            higher_size = maxint

        remainder = value % higher_size
        derived = int(remainder / size)
        if (value < size or derived == 0) and (omissible or result):
            return result

        result.append('%d %s' % (derived, derived == 1 and subject or plural))
        return result

    unit_method.__name__ = subject
    unit_method.size = size
    return unit_method


class OrderedUnitGroup(object):
    """
    Instances of this class is constructed using a list of definitions
    for a set of related units (in order to make sense) and constructs
    an object with parameters with the name of the units, that when
    invoked, will return a human readable string down to that particular
    unit's size.

    See the accompanied units module for more examples.
    """

    def __init__(self, *a):
        last = None
        for kw in a:
            last = units_factory(higher_unit=last, **kw)
            setattr(self, kw['subject'], last)
            setattr(self, kw['plural'], last)
