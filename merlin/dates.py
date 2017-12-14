from cytoolz import first
from dateutil import parser
from merlin import chips
import re


def to_ordinal(datestring):
    """Extract an ordinal date from a date string

    Args:
        datestring (str): date value

    Returns:
        int: ordinal date
    """

    return parser.parse(datestring).toordinal()


def startdate(acquired):
    """Returns the startdate from an acquired date string

    Args:
        acquired (str): / separated date range in iso8601 format

    Returns:
        str: Start date
    """

    return acquired.split('/')[0]


def enddate(acquired):
    """Returns the enddate from an acquired date string

    Args:
        acquired (str): / separated date range in iso8601 format

    Returns:
        str: End date
    """

    return acquired.split('/')[1]


def is_acquired(acquired):
    """Is the date string a / separated date range in iso8601 format?

    Args:
        acquired: A date string

    Returns;
        bool: True or False
    """

    # 1980-01-01/2015-12-31
    regex = '^[0-9]{4}-[0-9]{2}-[0-9]{2}\/[0-9]{4}-[0-9]{2}-[0-9]{2}$'
    return bool(re.match(regex, acquired))


def mapped(chipmap):
    """Transform a dict of chips into a dict of datestrings

    Args:
        chipmap (dict): {k: [chips]}

    Returns:
        dict:  {k: [datestring2, datestring1, datestring3]}
    """

    return {k: chips.dates(v) for k, v in cas.items()}
