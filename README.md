# lcmap-merlin
Turns lcmap spatial data into time series like magic.

## Features
* Retrieve chips & chip specs
* Convert chips & chip specs into time series rods
* Many composable functions
* Built with efficiency in mind... leverages Numpy for heavy lifting.
* Tested with cPython 3.5 & 3.6

## Example
This will retrieve pyccd flavored time-series data from an Aardvark instance
running locally on port 5678.
```
>>> import merlin
>>> aardvark = 'http://localhost:5678'
>>> chips = '{}/{}'.format(aardvark, '/landsat/v1/chips')
>>> specs = '{}/{}'.format(aardvark, '/landsat/v1/chip-specs')
>>>
>>> def queries(url):
    return {'reds':     ''.join([url, '?q=tags:red AND sr']),
            'greens':   ''.join([url, '?q=tags:green AND sr']),
            'blues':    ''.join([url, '?q=tags:blue AND sr']),
            'nirs':     ''.join([url, '?q=tags:nir AND sr']),
            'swir1s':   ''.join([url, '?q=tags:swir1 AND sr']),
            'swir2s':   ''.join([url, '?q=tags:swir2 AND sr']),
            'thermals': ''.join([url, '?q=tags:bt AND thermal AND NOT tirs2']),
            'quality':  ''.join([url, '?q=tags:pixelqa'])}

>>> data = merlin.pyccd(point=(-182000, 300400),
                        specs_url=specs,
                        chips_url=chips,
                        acquired='1980-01-01/2015-12-31',
                        queries=queries(specs)
>>> data
>>> (((chip_x, chip_y, x1, y1), {'dates': [],  'reds': [],     'greens': [],
                                 'blues': [],  'nirs1': [],    'swir1s': [],
                                 'swir2s': [], 'thermals': [], 'quality': []}),
     ((chip_x, chip_y, x1, y2), {'dates': [],  'reds': [],     'greens': [],
                                 'blues': [],  'nirs1': [],    'swir1s': [],
                                 'swir2s': [], 'thermals': [], 'quality': []}))
...
```

## Installing

From pypi: ```pip install lcmap-merlin```

## Developing
It is highly recommended to work within a virtual environment.
```bash
$ conda create --name merlin
$ source activate merlin
```

From there, clone this repo and install merlin's dependencies.
```bash
$ git clone git@github.com:usgs-eros/lcmap-merlin
$ cd lcmap-merlin
$ pip install -e .[test]
```

## Testing
```bash
$ pytest
```

Occasionally chip and chip spec test data may need to be updated if the source
specifications change.
Execute ```data.update_specs()``` and ```data.update_chips()``` from a repl.
```
>>> specs_url = 'http://localhost:5678/landsat/v1/chip-specs'
>>> chips_url = 'http://localhost:5678/landsat/v1/chips'
>>>
>>> from test import data
>>> data.update_specs(specs_url=specs_url)
>>> data.update_chips(chips_url=chips_url, specs_url=specs_url)
```
