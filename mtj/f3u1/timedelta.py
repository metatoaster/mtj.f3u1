from mtj.f3u1.units import Time

def format_timedelta(seconds, resolution='second'):
    result = getattr(Time, resolution)(seconds)
    result = ', '.join(result)

    return result
