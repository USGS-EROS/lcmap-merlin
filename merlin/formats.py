from cytoolz import partial
from merlin import chips
from merlin import dates
from merlin import functions
from merlin import rods
from merlin import specs


def pyccd(x, y, locations, dates_fn, specmap, chipmap):
    """Builds inputs for the pyccd algorithm.

    Args:
        x: x projection coordinate of chip
        y: y projection coordinate of chip
        locations: chip shaped 2d array of projection coordinates
        dates_fn (fn): returns dates that should be included in time series
        specmap (dict): mapping of keys to specs
        chipmap (dict): mapping of keys to chips

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

    _index   = specs.byubid(merge(specmap.values()))
    _dates   = dates_fn()
    _creator = partial(rods.create, x=x, y=y, dateseq=_dates, locations=locations, ubid_index=_index)
    _flipped = partial(f.flip_keys, {k: _creator(chipseq=v) for k, v in chipmap.items()})
    return add_dates(dates=list(map(dates.to_ordinal, sort(dates, key=None))),
                     dods=flipped())
    
#    return tuple((k, v) for k, v in rods.items())


