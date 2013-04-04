from mtj.f3u1.factory import OrderedUnitGroup


Time = OrderedUnitGroup(
    {'subject': 'day', 'size': 86400, 'plural': 'days'},
    {'subject': 'hour', 'size': 3600, 'plural': 'hours'},
    {'subject': 'minute', 'size': 60, 'plural': 'minutes'},
    {'subject': 'second', 'size': 1, 'plural': 'seconds'},
)
