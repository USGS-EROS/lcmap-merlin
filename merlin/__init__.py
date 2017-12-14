from cytoolz import get_in
from cytoolz import partial
from specs import refspec
import chips


def create(x, y, acquired, cfg):

    # snap requested point to a chip
    x, y = get_in(['chip', 'proj-pt'], cfg['snap_fn'](x=x, y=y))

    # get specs
    specmap = cfg['specs_fn'](registry=cfg['registry_fn']())

    # get function that will return chipmap.
    # Don't create state with a realized variable to preserve memory
    chipmap = partial(chips.mapped, x=x, y=y, acquired=acquired, specmap=specmap, chips_fn=chips_fn)

    # calculate locations chip
    locations = chips.locations(x, y, refspec(specmap))
    
    return cfg['format_fn'](x=x,
                            y=y,
                            locations=locations,
                            dates_fn=cfg['dates_fn'],
                            specmap=specmap,
                            chipmap=chipmap()) 
