from csv import writer
from math import sqrt
from scipy.stats import uniform

import random

"""Position utility module

This module contains position related functions

"""

def equidistant_coords(n:int, map_size:int) -> list:
    """Generate equidistant coordinate on a square map

    Placing equidistan coord on a square map to 
    covert the whole area.

    Args:
        n (int): Number of coordinate to generate
        map_size (int): Map area in km^2

    Return:
        list(tuple(float,float)): list of coordinates (x,y)
    """
    n_by_side = int(sqrt(n))
    map_length = sqrt(map_size)*1000
    equi_dist = map_length/n_by_side
    points = []
    for x_point in range(n_by_side):
        for y_point in range(n_by_side):
            points.append(((0.5+x_point)*equi_dist,
                           (0.5+y_point)*equi_dist))
    return points

def random_coord(n:int, map_size:int) -> list:
    """Generate random coordinate on a square map

    Generated coordinate on a square map using 
    a uniform distribution.

    Args:
        n (int): Number of coordinate to generate
        map_size (int): Map area in km^2

    Return:
        list(tuple(float,float)): list of coordinates (x,y)
    """
    # map_length = sqrt(map_size)*1000
    # x = uniform.rvs(size=n, scale=map_length)
    # y = uniform.rvs(size=n, scale=map_length)
    n_by_side = int(sqrt(n))
    points = []
    for x in range(n_by_side):
        for y in range(n_by_side):
            points.append((random.uniform(0, sqrt(map_size) * 1000), random.uniform(0, sqrt(map_size) * 1000)))
    return points

    # return list(zip(x,y))

def get_distance(coord1:tuple, coord2:tuple):
    """Caculate L2 distance between two points

    Args:
        cood1 (tuple(float,float)): First coodinate (x,y)
        cood2 (tuple(float,float)): Second coodinate (x,y)

    Return:
        float: L2 distance in meters
    """
    L2 = sqrt((coord2[1] - coord1[1])**2 + (coord2[0] - coord1[0]) ** 2)


    return L2

    #
    # x_diff = coord1[0]-coord2[0]
    # y_diff = coord1[1]-coord2[1]
    # return sqrt(x_diff**2+y_diff**2)
    #
