from mtj.f3u1.factory import UnitGroup

_plurals = {
    'day': 'days',
    'hour': 'hours',
    'minute': 'minutes',
    'second': 'seconds',
    'mile': 'miles',
    'yard': 'yards',
    'foot': 'feet',
    'inch': 'inches',
    'ton': 'tons',
    'stone': 'stones',
    'pound': 'pounds',
    'ounce': 'ounces',
}

Time = UnitGroup(plurals=_plurals, units={
    'day': 86400,
    'hour': 3600,
    'minute': 60,
    'second': 1,
})

ImperialLength = UnitGroup(plurals=_plurals, units={
    'mile': 63360,
    'yard': 36,
    'foot': 12,
    'inch': 1,
})

ImperialWeight = UnitGroup(plurals=_plurals, units={
    'ton': 35840,
    'stone': 224,
    'pound': 16,
    'ounce': 1,
})
