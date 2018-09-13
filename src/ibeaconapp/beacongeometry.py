from collections import namedtuple
import math
import re

Circle = namedtuple('Circle', 'x y r')
Point = namedtuple('Point', 'x y')

class BeaconGeometryError(Exception):
    pass

def get_centroid_center(circles):
    """ given 3 circles, returns the center point of their common area.
        if the circles don't have a common area, enlarge/narrow them 
        until they do. """
        
    print "input:", circles
    if len(circles) != 3:
        raise BeaconGeometryError((
            "More or less than 3 circles given. This function computes "
            "the center point of the common area of 3 circles"))
            
    area_delimiters = []
    for i1, i2, i3 in [(0,1,2), (0,2,1), (1,2,0)]:
        try:
            p1, p2 = get_intersection_points(circles[i1], circles[i2])
            p = get_point_in_circle(p1, p2, circles[i3])
            area_delimiters.append(p)
        except BeaconGeometryError as e:
            #todo: log str(e)
            print e
            if re.match(r'The circles .* are separate', str(e)):
                return dealw_separate_circles(circles)
            elif re.match(r'The first circle .* within the second', str(e)):
                return dealw_contained_circles(circles, i1, i2)
            elif re.match(r'The second circle .* within the first', str(e)):
                return dealw_contained_circles(circles, i2, i1)
            elif re.match(r'Neither point .* within the circle', str(e)):
                return dealw_separate_circles(circles)
            elif re.match(r'Both points .* within the circle', str(e)):
                return dealw_large_circle(circles, i3)
            else:
                raise e

    p1, p2, p3 = area_delimiters
    (x,y) = get_centralpoint(p1, p2, p3)

    return Point(x=x, y=y), circles

def dealw_separate_circles(circles):
    for i in range(len(circles)):
        circles[i] = enlarge_circle(circles[i])
    return get_centroid_center(circles)

def dealw_contained_circles(circles, index1, index2):
    """ treat the case when the circle at index1 is contained within 
        the circle at index2. actions: narrow the larger circle, 
        enlarge the smaller one and try to get the center point of the 
        3 circles common area again. """

    circles[index1] = enlarge_circle(circles[index1])
    circles[index2] = narrow_circle(circles[index2])
    return get_centroid_center(circles)

def dealw_large_circle(circles, index):
    for i in range(len(circles)):
        if i == index:
            circles[i] = narrow_circle(circles[i])
        else:
            circles[i] = enlarge_circle(circles[i])
    return get_centroid_center(circles)

def get_intersection_points(circle1, circle2):
    check_circles_intersect(circle1, circle2)

    # math equations from:
    # http://www.ambrsoft.com/TrigoCalc/Circles2/circle2intersection/CircleCircleIntersection.htm
    (a, b, r0) = circle1
    (c, d, r1) = circle2
    a, b, r0 = float(a), float(b), float(r0)
    c, d, r1 = float(c), float(d), float(r1)

    D = distance_between_points((a, b), (c, d))

    # area - area of the triangle formed by the two circle centers and 
    # one of the intersection point. The sides of this triangle are 
    # S, r0 and r1 , the area is calculated by Heron' s formula
    area = 0.25 * math.sqrt( (D+r0+r1)*(D+r0-r1)*(D-r0+r1)*(-D+r0+r1) )
    
    x_part1 = (a+c)/2 + (c-a)*(r0**2 - r1**2)/(2*D**2)
    x_part2 = 2*area*(b-d)/(D**2)
    
    x1 = x_part1 + x_part2
    x2 = x_part1 - x_part2
    
    y_part1 = (b+d)/2 + (d-b)*(r0**2 - r1**2)/(2*D**2)
    y_part2 = 2*area*(a-c)/(D**2)
    
    y1 = y_part1 - y_part2
    y2 = y_part1 + y_part2

    return [Point(x=x1, y=y1), Point(x=x2, y=y2)]
    
def check_circles_intersect(circle1, circle2):
    """ Raise Exception if the 2 circles don't intersect """

    (x1, y1, r1) = circle1
    (x2, y2, r2) = circle2

    d = distance_between_points((x1,y1), (x2,y2))

    if d > r1 + r2:
        raise BeaconGeometryError("The circles {0} and {1} are separate!"\
            .format(circle1, circle2))
    elif d < math.fabs(r1 - r2) and r1 < r2:
        raise BeaconGeometryError(
            "The first circle {0} is contained within the second circle {1}!"\
            .format(circle1, circle2))
    elif d < math.fabs(r1 - r2) and r1 > r2:
        raise BeaconGeometryError(
            "The second circle {0} is contained within the first circle {1}!"\
            .format(circle2, circle1))
    elif d == 0 and r1 == r2:
        raise BeaconGeometryError("Circles {0} and {1} are coincident!"\
            .format(circle1, circle2))

def distance_between_points(p1, p2):
    (x1,y1), (x2,y2) = p1, p2

    dx = float(x1) - float(x2)
    dy = float(y1) - float(y2)
    d = math.sqrt( dx**2 + dy**2 )

    return d
         
def get_point_in_circle(p1, p2, circle):
    if is_point_in_circle(p1, circle) and \
       is_point_in_circle(p2, circle):
        raise BeaconGeometryError(
            "Both points - {0} and {1} - are contained within the circle {2}"\
            .format(p1, p2, circle))
    elif not is_point_in_circle(p1, circle) and \
         not is_point_in_circle(p2, circle):
        raise BeaconGeometryError(
            "Neither point - {0} or {1} - is contained within the circle {2}"\
            .format(p1, p2, circle))
    elif is_point_in_circle(p1, circle):
        return p1
    else:
        return p2

def is_point_in_circle(point, circle):
    (px, py) = point
    (cx, cy, cr) = circle

    d = distance_between_points((px,py), (cx,cy))

    return True if d <= cr else False

def enlarge_allcircles(circles):
    for i in range(len(circles)):
        circles[i] = enlarge_circle(circles[i])
    return circles
    
def enlarge_circle(circle):
    (x, y, r) = circle
    return Circle(x=x, y=y, r=1.05 * r)
    
def narrow_circle(circle):
    (x, y, r) = circle
    return Circle(x=x, y=y, r=0.95 * r)
    
def get_centralpoint(p1, p2, p3):
    (x1,y1), (x2,y2), (x3,y3) = p1, p2, p3

    x = (float(x1) + float(x2) + float(x3)) / 3
    y = (float(y1) + float(y2) + float(y3)) / 3

    return Point(x=x, y=y)
