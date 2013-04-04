from sys import maxint

def units_factory(subject, size, higher_unit=None, plural=None):

    assert higher_unit is None or callable(higher_unit)

    if plural is None:
        plural = subject

    def _method(value, omissible=False):
        if higher_unit:
            result = higher_unit(value, omissible=True)
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

    _method.__name__ = subject
    _method.size = size
    return _method


class OrderedUnitGroup(object):

    def __init__(self, *a):
        last = None
        for kw in a:
            last = units_factory(higher_unit=last, **kw)
            setattr(self, kw['subject'], last)
