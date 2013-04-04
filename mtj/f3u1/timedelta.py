from mtj.f3u1.factory import unit_reduction_factory

_day = unit_reduction_factory('day', 86400, plural='days')
_hour = unit_reduction_factory('hour', 3600, 86400, 'hours')
_minute = unit_reduction_factory('minute', 60, 3600, 'minutes')
_second = unit_reduction_factory('second', 1, 60, 'seconds')

def format_timedelta(seconds, resolution=None):
    result = []

    _day(result, seconds)
    _hour(result, seconds)

    # quickie as proof of concept.
    if resolution != 'hour':
        _minute(result, seconds)
        _second(result, seconds)

    result = ', '.join(result)
    if not result:
        # haha
        result = '0 hours'

    return result
