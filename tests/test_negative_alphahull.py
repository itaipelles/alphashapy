import pytest
import numpy as np
from shapely.geometry import Point, MultiPoint
from alphashapy import alphahull_negative_alpha

def test_positive_alpha_assertion():
    pnts = [[0,1],[2,3],[3,4]]
    with pytest.raises(AssertionError):
        alphahull_negative_alpha(pnts, 1)

def test_single_point():
    pnts = [[0,1]]
    for alpha in [-1,-5,-10]:
        alphahull = alphahull_negative_alpha(pnts, alpha)
        assert alphahull.geom_type == "Point"
        assert alphahull.equals(Point(pnts[0]))

def test_2_points():
    pnts = [[0,1],[0,2]]
    for alpha in [-1,-5,-10]:
        alphahull = alphahull_negative_alpha(pnts, alpha)
        assert alphahull.area == 0
        assert alphahull.geom_type == "MultiPoint"
        assert alphahull.equals(MultiPoint(pnts))

def test_3_points():
    pnts = [[0,0],[0,1],[1,0]]
    alpha = -0.1
    alphahull = alphahull_negative_alpha(pnts, alpha)
    # the alphahull should be almost the entire triangle, which has area 0.5
    assert alphahull.area > 0.48
    
    alpha = -2
    alphahull = alphahull_negative_alpha(pnts, alpha)
    # the circles of radius 0.5 are now small enough to enter the triangle and eat it from inside, leaving nothing
    assert alphahull.area < 0.01

def test_4_points_area_decreases():
    pnts = np.random.rand(4,2)
    alphas = [-0.1,-0.2,-0.5,-1,-2]
    convex_hull_area = MultiPoint(pnts).convex_hull.area
    areas = [convex_hull_area] + [alphahull_negative_alpha(pnts, alpha).area for alpha in alphas]
    assert np.all(np.diff(areas)<=0)

def test_100_points_area_decreases():
    pnts = np.random.rand(100,2)
    alphas = [-0.1,-0.2,-0.5,-1,-2,-5,-10,-100]
    convex_hull_area = MultiPoint(pnts).convex_hull.area
    areas = [convex_hull_area] + [alphahull_negative_alpha(pnts, alpha).area for alpha in alphas]
    assert np.all(np.diff(areas)<=0)
    
    
    