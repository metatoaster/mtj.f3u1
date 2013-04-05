from mtj.f3u1.factory import UnitGroup


Time = UnitGroup(
    {'subject': 'day', 'size': 86400, 'plural': 'days'},
    {'subject': 'hour', 'size': 3600, 'plural': 'hours'},
    {'subject': 'minute', 'size': 60, 'plural': 'minutes'},
    {'subject': 'second', 'size': 1, 'plural': 'seconds'},
)

ImperialLength = UnitGroup(
    {'subject': 'mile', 'size': 63360, 'plural': 'miles'},
    {'subject': 'yard', 'size': 36, 'plural': 'yards'},
    {'subject': 'foot', 'size': 12, 'plural': 'feet'},
    {'subject': 'inch', 'size': 1, 'plural': 'inches'},
)

ImperialWeight = UnitGroup(
    {'subject': 'ton', 'size': 35840, 'plural': 'tons'},
    {'subject': 'stone', 'size': 224, 'plural': 'stones'},
    {'subject': 'pound', 'size': 16, 'plural': 'pounds'},
    {'subject': 'ounce', 'size': 1, 'plural': 'ounces'},
)
