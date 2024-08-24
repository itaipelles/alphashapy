import pytest
import numpy as np
from shapely.geometry import Point, MultiPoint
from alphashapy.negative_alphahull import alphahull_negative_alpha

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
    #TODO: implement
    pass

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
    
    
    