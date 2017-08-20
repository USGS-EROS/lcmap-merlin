from dateutil import parser
import re


def to_ordinal(datestring):
    """Extract an ordinal date from a date string
    :param datestring: String with date value
    :return: An ordinal date
    """
    return parser.parse(datestring).toordinal()


def startdate(acquired):
    """Returns the startdate from an acquired date string
    :param acquired: / seperated date range in iso8601 format
    :return: Start date as string
    """
    return acquired.split('/')[0]


def enddate(acquired):
    """Returns the enddate from an acquired date string
    :param acquired: / seperated date range in iso8601 format
    :return: End date as string
    """
    return acquired.split('/')[1]


def is_acquired(acquired):
    """Is the date string a / seperated date range in iso8601 format?
    :param acquired: A date string
    :return: Boolean
    """
    # 1980-01-01/2015-12-31
    regex = '^[0-9]{4}-[0-9]{2}-[0-9]{2}\/[0-9]{4}-[0-9]{2}-[0-9]{2}$'
    return bool(re.match(regex, acquired))


def checked(chips):
    """Ensures a complete set of chips exist for a chip stack when compared to
    all dates for all chip stacks.
    :param chips: dict of spectra: chip sequence
    :returns: Sequence of datestrings or Exception
    """
    #dates = list(map(fchips.dates, chips.values()))
    #intersect = f.intersection(dates)
    #union = set(f.flatten(dates))

    #intersect = f.intersection(map(fchips.dates, [c for c in chips.values()]))
    #union = set(map(fchips.dates, [v for k, v in chips.values()]))

    cdates = list(map(lambda c: c['acquired'], chips))
    cdateset = set(cdates)
    dateset  = set(unioned_dates)
    datelength = len(unioned_dates)
    chiplength = len(chips)

    if sorted(dates) == sorted(cdates) and datelength == chiplength:
        return tuple(chips)
    else:
        extras = cdateset - dateset
        missing = dateset - cdateset
        ubids = set(map(lambda c: c['ubid'], chips))
        msg = ("Inconsistent chip set for ubids:{} "
               "Dates count:{} Chips count:{} "
               "Extra dates:{} Missing dates:{}".format(ubids,
                                                        datelength,
                                                        chiplength,
                                                        extras,
                                                        missing))
        logger.error(msg)
        raise Exception(msg)
