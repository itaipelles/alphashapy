import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Point, LineString, MultiPoint
from shapely import unary_union

def alphahull_negative_alpha(points,alpha):
    '''
    Constructs the alpha hull of the given points.
    
    :param points: A sequence of points, any array-like with shape (N,2)
    :param alpha: Any negative number
    :return: The alpha hull
    :rtype: shapely.Geometry
    '''
    assert(alpha<0)
    if len(points) == 1:
        return Point(points[0])
    S = MultiPoint(points)
    if len(points) == 2:
        return S
        
    r = -1/alpha
    vd_c_s = Voronoi(points)
    circles = []
    center = vd_c_s.points.mean(axis=0)
    for pq_indices, voronoi_vertices_orig in zip(vd_c_s.ridge_points, vd_c_s.ridge_vertices):
        voronoi_vertices = np.asarray(voronoi_vertices_orig)
        for i in range(len(voronoi_vertices)):
            x = vd_c_s.vertices[voronoi_vertices[i]][0]
            y = vd_c_s.vertices[voronoi_vertices[i]][1]
            if x*x+y*y>1e10:
                voronoi_vertices[i]=-1
        p = Point(vd_c_s.points[pq_indices[0]])
        q = Point(vd_c_s.points[pq_indices[1]])
        
        if np.all(voronoi_vertices<0):
            # print('weird voronoi line from infinity to infinity!?',voronoi_vertices_orig, voronoi_vertices)
            continue
        
        is_semiinfinite = False
        if np.any(voronoi_vertices<0):
            # line to infitiy
            is_semiinfinite = True
            # print('infinity')
            voronoi_v_1 = vd_c_s.vertices[voronoi_vertices[voronoi_vertices >= 0][0]]  # finite end Voronoi vertex
            tangent = vd_c_s.points[pq_indices[1]] - vd_c_s.points[pq_indices[0]]  # tangent
            tangent /= np.linalg.norm(tangent)
            normal = np.array([-tangent[1], tangent[0]])  # normal

            midpoint = vd_c_s.points[pq_indices].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, normal)) * normal
            voronoi_v_2 = Point(voronoi_v_1 + direction*5)
            voronoi_v_1 = Point(voronoi_v_1)
        else:
            voronoi_v_1 = Point(vd_c_s.vertices[voronoi_vertices[0]])
            voronoi_v_2 = Point(vd_c_s.vertices[voronoi_vertices[1]])
        
        d = voronoi_v_1.distance(p)
        if d >= r:
            circles.append(voronoi_v_1.buffer(d))
            # print('1',square_01.intersection(circles[-1]).area)
        d = voronoi_v_2.distance(p) if not is_semiinfinite else 0
        if not is_semiinfinite and d >= r:
            circles.append(voronoi_v_2.buffer(d))
            # print('2',square_01.intersection(circles[-1]).area)
            
        voronoi_line = LineString([voronoi_v_1, voronoi_v_2])
        circle_around_p = p.buffer(r).boundary
        intersection = circle_around_p.intersection(voronoi_line)
        # if len(circles) and square_01.intersection(circles[-1]).area>0.5:
        #     print('huge circle',pq_indices, voronoi_vertices, p,q,voronoi_v_1, voronoi_v_2)
        #     break
        if intersection.geom_type=='Point':
            # Single point
            circles.append(intersection.buffer(intersection.distance(p)))
            # print('3',square_01.intersection(circles[-1]).area)
        elif intersection.geom_type=='LineString':
            if intersection.is_empty:
                continue
            else:
                # non empty line?
                print('non empty line??')
        elif intersection.geom_type=='MultiPoint':
            for intersection_point in intersection.geoms:
                circles.append(intersection_point.buffer(intersection_point.distance(p)))
                # print('4',square_01.intersection(circles[-1]).area)
        else:
            print("new type", intersection.geom_type)

    return S.convex_hull.difference(unary_union(circles))