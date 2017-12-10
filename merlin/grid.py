'''
# Grid Spec

This document explains the concept of a Grid Spec and provides a basic usage example.

## What is a Grid Spec?

A grid spec is a set of values that relate two different coordinate systems. For example, a grid spec can
provide values used to convert any CONUS ARD projection system coordinate to the corresponding CONUS ARD Tile
ID (e.g. H04V07).

The properties of a grid spec are:

* rx: x-axis reflection
* ry: y-axis reflection
* sx: x-axis scaling
* sy: y-axis scaling
* tx: x-axis translation
* ty: y-axis translation

_Please Note: a grid spec can be represented many ways, but must always use the same values for key names._

## Example

The USGS ARD CONUS Tile Grid provides identifiers for large areas, called tiles, over the conterminous United States. This grid uses a coordinate system similar to the coordinate system for computer screens. The origin of the grid is located somewhere in the Pacific Northwest and proceeds in intervals of 150,000 meters per grid unit from north to south and west to east.

It can be represented using the following JSON:

```
{ "rx":  1.0,
  "ry": -1.0,
  "sx":  150000.0,
  "sy":  150000.0,
  "tx":  2565585.0,
  "ty":  3314805.0 }
```

These values represent reflection, scaling, and translation values along the x- and y- axis.

### Reflection

The USGS ARD CONUS Tile Grid increases along the y-axis as one moves from north to south, thus the y-axis
reflection value is -1.0. The x-axis of the tile grid increases from west to east, so an x-axis reflection
value of 1.0 is specified.

### Scale

The scale of the grid is 150,000 projection untis per grid unit. 150,000 / 1 = 150,000 

### Translation

The origin of the tile grid in the original projection is (-2565585, 3314805). These quantities are removed (subtracted) from the original point during translation. Consequently, the value used for _x-axis translation is positive_. The value for the y-axis remains a positive value.


## Usage

Matrix mathematics libraries are the easiest way to use a grid spec; they provide a more readable alternative
to lengthy arithmetic operations. Furthermore, an inverted matrix containing grid spec values can be used to
transform grid coordinates back to standard coordinates.

_Although you don't have to be an expert in linear algebra to work with a grid spec, you must perform the
proper matrix operations provided by supporting libraries. Some libraries provide similarly named functions
for multiplying matrices and multiplying a matrix by a scalar value._

### Basic Steps

1. Create a transformation matrix (RST).
2. Create a matrix (i.e. homogeneous coordinates) for your point (p).
3. Use matrix multiplication (`RST * p`) to obtain grid coordinates.

### Detailed Example

First, build a transformation matrix from the grid-spec:

```
RST = [[rx/sx      0   tx/sx]
       [    0  ry/sy   ty/sy]
       [    0      0       1]]
```

Second, represent a point using homogeneous coordinates:

```
p = [[x]
     [y]
     [1]]
```

Finally, perform matrix multiplication to obtain the grid point as homogeneous coordinates.

```
g = RST * p ;; be certain to use matrix multiplication
```

In order to find the corresponding point of a grid coordinate in a projection coordinate system, multiply the
inverse of the original matrix with a homogeneous grid coordinate.

```
p = inv(RST) * g ;; really, make sure you're using matrix multiplication
```


## Additional Notes

1. A grid spec and affine transformation are related. However, the structure of a grid spec is not itself an
   affine transformation matrix, so a different term is used instead.
2. In the future, two well-known text (WKT) properties may be added to a grid spec to provide guidance on how
   it should be used. This can be used to prevent using a grid spec in the wrong context. At this point, it's
   not needed.
3. In the future, a rotation property may be added to a grid spec. However, this is not needed, and would only
   add to the cognitive load of people that have to use them.
'''

from cytoolz import first
from cytoolz import second
from cytoolz import memoize
import requests


@memoize
def basis(host, resource='/grid'):
    '''Return the grid basis defined at the url.

    Args:
        host (str): Grid spec host:port
        resource (str): Grid resource path

    Returns:
        sequence: [{"name": "tile",
                    "proj": null,
                    "rx": 1,
                    "ry": -1,
                    "sx": 150000,
                    "sy": 150000,
                    "tx": 2565585,
                    "ty": 3314805},
                   {"name": "chip",
                    "proj": null,
                    "rx": 1,
                    "ry": -1,
                    "sx": 3000,
                    "sy": 3000,
                    "tx": 2565585,
                    "ty": 3314805}]
    '''

    return requests.get(url='{}/{}'.format(host, resource))


@memoize
def find(point, host, resource='/grid/find'):
    '''
    Return grid specifications for a point.

    Args:
        point (tuple): (x, y)
        host (str): Grid find host:port
        resource (str): Grid find resource path

    Returns:
        dict:   {"tile": {"proj-pt": [1784415,2114805], "grid-pt": [29,8]},
                 "chip": {"proj-pt": [1832415,2036805], "grid-pt": [1466,426]}}
    '''

    return requests.get(url='{}/{}'.format(host, resource),
                        params={'x': first(point), 'y': second(point)})

   
@memoize
def near(point, host, resource='/grid/near'):
    '''
    Return grids near the specified point.

    Args:
        point (tuple): (x, y)
        host (str): Grid near host:port
        resource (str): Grid near resource path
        
    Returns:
        dict: {
            "tile": [
                {"proj-pt": [1634415,1964805], "grid-pt": [28,9]},
                {"proj-pt": [1634415,2114805], "grid-pt": [28,8]},
                {"proj-pt": [1634415,2264805], "grid-pt": [28,7]},
                {"proj-pt": [1784415,1964805], "grid-pt": [29,9]},
                {"proj-pt": [1784415,2114805], "grid-pt": [29,8]},
                {"proj-pt": [1784415,2264805], "grid-pt": [29,7]},
                {"proj-pt": [1934415,1964805], "grid-pt": [30,9]},
                {"proj-pt": [1934415,2114805], "grid-pt": [30,8]},
                {"proj-pt": [1934415,2264805], "grid-pt": [30,7]}],
            "chip": [
                {"proj-pt": [1829415,2033805], "grid-pt": [1465,427]},
                {"proj-pt": [1829415,2036805], "grid-pt": [1465,426]},
                {"proj-pt": [1829415,2039805], "grid-pt": [1465,425]},
                {"proj-pt": [1832415,2033805], "grid-pt": [1466,427]},
                {"proj-pt": [1832415,2036805], "grid-pt": [1466,426]},
                {"proj-pt": [1832415,2039805], "grid-pt": [1466,425]},
                {"proj-pt": [1835415,2033805], "grid-pt": [1467,427]},
                {"proj-pt": [1835415,2036805], "grid-pt": [1467,426]},
                {"proj-pt": [1835415,2039805], "grid-pt": [1467,425]}]} 
    '''

    return request.get(url='{}/{}'.format(host, resource),
                       params={'x': first(point), 'y': second(point)})
