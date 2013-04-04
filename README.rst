Introduction
============

Once upon a time, the quest for a method to format seconds into a human
readable string was given to a hero.  Braving through the nets of Inter,
our hero stumbled upon place after places, such as State of Active, the
Exchange of Stacks, and even some other Hubs of Gits.  Some giants were
found, like Tens of Tens Lines Long of Repetition, others were touching
strange, unrelated things and looking complicated.  Those that spoke in
other unworldly incantations were of no use.  In the end, our hero gave
up, and constructed this monstrosity from the corpses of fairies::

    def format_timedelta(delta_t):
        hours = delta_t.seconds / 3600
        days = delta_t.days
        seconds = delta_t.seconds

        # Don't ask.  Read the test; be happy you don't have to write this.
        # (WTB something simple like str(delta_t) with more control.)
        # (Maybe I should just do this in javascript?)
        return '%(day)s%(hour)s' % {
            'day': days and '%(days)d day%(dayp)s%(comma)s' % {
                    'days': days,
                    'dayp': days != 1 and 's' or '',
                    'comma': seconds > 3599 and ', ' or '',
                } or '',
            'hour': (hours > 0 or days == 0 and hours == 0)
                and '%(hours)d hour%(hourp)s' % {
                    'hours': hours,
                    'hourp': hours != 1 and 's' or '',
                } or '',
        }

(OOC: It was actually tested; see earliest commits).

Then the realization hit our hero: sometimes a dworf want to micromanage
the resolution in minutes, and then the middle management dino will come
back and stamp on all the things and make the resolution to be no lesser
than a weeks in the name of opsec.  These arbitrary changes to this tiny
simple thing resulted in many gnashing of teeth and also many nightmares
that never seem to end.  Many cries of F7U12 was thrown about.

After countless nanoseconds of meditation, our hero destroyed 4 of those
F's and 11 of those U's towards the direction of the unseen horizon, the
solution was discovered, and it is one that transcends beyond time.

What?
=====

F3U1 - Factory For Formatting Units.  Or Factory of Functions for
Formatting Units.  Or Formatting Functions from Functions for Units.
They all kind of work, doesn't really matter to me.

This is a module for formatting units that provides methods to render
most commonly found non-metric measurement units into a human readable
string.  These functions are constructed in a way that minimizes calls
to string formatting functions, and is constructed using a function that
is generic to this specific use case.  The target is to cover the most
basic cases in the name of simplicity, and leave the difficult/advanced
cases to other libraries that might do the same thing.
