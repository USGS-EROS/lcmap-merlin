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

    return requests.get('{}/{}'.format(host, resource))


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

    return requests.get('{}/{}'.format(host, resource), {'x': first(point), 'y': second(point)})

   
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

    return request.get(url, {'x': first(point), 'y': second(point)})
