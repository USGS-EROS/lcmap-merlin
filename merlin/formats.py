from cytoolz import partial
from merlin import chips
from merlin import functions
from merlin import rods
from merlin import specs


def pyccd(x, y, locations, dates_fn, specmap, chipmap):
    # check dates for symmetry
    # 
    pass


def pyccd_format(x, y, locations, dates_fn, specmap, chipmap):
    """Builds inputs for the pyccd algorithm.

    Args:
        chip_x: x coordinate for chip identifier
        chip_y: y coordinate for chip identifier
        chip_locations: chip shaped 2d array of projection coordinates
        chips_and_specs: {k: [chips],[specs]}
        dates: sequence of chip dates to be included in output

    Returns:
        A tuple of tuples.

    Description:
        The pyccd format requires a key of (chip_x, chip_y, x, y) with a
        dictionary of sorted numpy arrays representing each spectra plus an
        additional sorted dates array.

        >>> pyccd_format(*args)
        (((chip_x, chip_y, x1, y1), {"dates": [],  "reds": [],
                                     "greens": [], "blues": [],
                                     "nirs1": [],  "swir1s": [],
                                     "swir2s": [], "thermals": [],
                                     "quality": []}),
         ((chip_x, chip_y, x1, y2), {"dates": [],  "reds": [],
                                     "greens": [], "blues": [],
                                     "nirs1": [],  "swir1s": [],
                                     "swir2s": [], "thermals": [],
                                     "quality": []}))
        ...
    """

    def process(chipz, ubid_index):
        
        return thread_last(chipz,
                           chips.trim(dates),
                           chips.deduplicate(),
                           sort,
                           chips.to_numpy(ubid_index),
                           mrods.from_chips(),
                           mrods.locate(locations),
                           identify(x, y))

    ubid_index = specs.byubid(merge(specmap.values()))
        
    flipped = partial(f.flip_keys, {k: process(k=k, chipz=v, ubid_index=ubid_index) for k, v in chipmap.items()})

    return add_dates(dates=list(map(mdates.to_ordinal, sort(dates, key=None))), dods=flipped())
    






    rods = add_dates(dates=list(map(mdates.to_ordinal, sort(dates, key=None))),
                     dods=f.flip_keys({k: identify(chip_x, chip_y, mrods.locate(locations, mrods.from_chips(chips.to_numpy(sort(chips.deduplicate(chips.trim(first(v), dates))),
                                                                                                                                                 specs.byubid(specs[k]))))) for k, v in chipmap.items()}))

    return tuple((k, v) for k, v in rods.items())


