from sys import maxint

def unit_reduction_factory(subject, low, high=maxint, plural=None):
    if plural is None:
        plural = subject

    def _method(result, value, minimal=None):
        derived = int(value % high / low)
        if value < low or derived == 0:
            return
        result.append('%d %s' % (derived, derived == 1 and subject or plural))

    _method.__name__ = subject
    return _method
