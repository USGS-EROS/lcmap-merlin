from cytoolz import first
from cytoolz import second
from merlin import chips
from merlin import chip_specs


def chips_and_specs(point, specs_fn, chips_url, chips_fn, acquired, query):
    """Returns chips and specs for a given chip spec query
    :param point: A tuple of (x, y) which is within the extents of a chip
    :param specs_fn:  Function that accepts a url query and returns chip specs
    :param chips_url: URL to the chips host:port/context
    :param chips_fn:  Function that accepts x, y, acquired, url, ubids and
                      returns chips.
    :param acquired: Date range string as start/end, ISO 8601 date format
    :param query:  URL query to retrieve chip specs
    :return: Tuple of sequences: ([chips], [specs])
    """
    specs = specs_fn(query)
    chips = chips_fn(x=first(point),
                     y=second(point),
                     acquired=acquired,
                     url=chips_url,
                     ubids=chip_specs.ubids(specs))
    return (chips, specs)


def locate(point, spec):
    """Returns chip_x, chip_y and all chip locations given a point and spec
    :param point: sequence of x,y
    :point spec: chip spec
    :return: (chip_x, chip_y, chip_locations)
    """
    chip_x, chip_y = chips.snap(*point, chip_spec=spec)
    chip_locations = chips.locations(chip_x, chip_y, spec)
    return (chip_x, chip_y, chip_locations)
