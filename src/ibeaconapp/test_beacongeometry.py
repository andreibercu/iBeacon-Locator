from beacongeometry import *

import unittest

class TestBeaconGeometry(unittest.TestCase):

    def test_distance_between_points(self):
        # distance_between_points parameters are x1,y1,x2,y2

        self.assertEqual(distance_between_points((1, 1.5), (4, 1.5)), 3)
        self.assertEqual(distance_between_points(
            Point(x=1, y=1.5), Point(x=4, y=1.5)), 3)

        self.assertEqual(distance_between_points((2.5, 2), (2.5, 4.5)), 2.5)
        self.assertEqual(distance_between_points(
            Point(x=2.5, y=2), Point(x=2.5, y=4.5)), 2.5)

        self.assertEqual(distance_between_points((1, 1), (1, 1)), 0)
        self.assertEqual(distance_between_points(
            Point(x=1, y=1), Point(x=1, y=1)), 0)

        self.assertIs(type(distance_between_points((2, 2), (2, 1))), float)
        self.assertIs(type(distance_between_points(
            Point(x=2, y=2), Point(x=2, y=1))), float)

    def test_check_circles_intersect(self):
        # raise if separate circles
        self.assertRaises(BeaconGeometryError, check_circles_intersect, 
            Circle(x=3,y=3,r=2), Circle(x=8,y=3,r=2))
        self.assertRaises(BeaconGeometryError, check_circles_intersect, 
            (3,3,2), (8,3,2))

        # raise if circles are one inside the other
        self.assertRaises(BeaconGeometryError, check_circles_intersect, 
            Circle(x=5,y=5,r=1), Circle(x=4,y=4,r=3))
        self.assertRaises(BeaconGeometryError, check_circles_intersect, 
            (5,5,1), (4,4,3))

        # raise if circles are coincident
        self.assertRaises(BeaconGeometryError, check_circles_intersect, 
            Circle(x=3,y=3,r=1), Circle(x=3,y=3,r=1))
        self.assertRaises(BeaconGeometryError, check_circles_intersect, 
            (3,3,1), (3,3,1))

        # return None if circles intersect in 1 or 2 points
        self.assertIsNone(check_circles_intersect(
            Circle(x=4,y=4,r=1.5), Circle(x=4,y=7,r=1.5)))
        self.assertIsNone(check_circles_intersect(
            (4,4,1.5), (4,7,1.5)))
        self.assertIsNone(check_circles_intersect(
            Circle(x=4,y=4,r=2.5), Circle(x=4,y=7,r=2.5)))
        self.assertIsNone(check_circles_intersect(
            (4,4,2.5), (4,7,2.5)))

    def test_get_intersection_points(self):
        # raise if separate circles
        self.assertRaises(BeaconGeometryError, get_intersection_points, 
            Circle(x=3,y=3,r=2), Circle(x=8,y=3,r=2))
        self.assertRaises(BeaconGeometryError, get_intersection_points, 
            (3,3,2), (8,3,2))

        # raise if circles are one inside the other
        self.assertRaises(BeaconGeometryError, get_intersection_points, 
            Circle(x=5,y=5,r=1), Circle(x=4,y=4,r=3))
        self.assertRaises(BeaconGeometryError, get_intersection_points, 
            (5,5,1), (4,4,3))

        # raise if circles are coincident
        self.assertRaises(BeaconGeometryError, get_intersection_points, 
            Circle(x=3,y=3,r=1), Circle(x=3,y=3,r=1))
        self.assertRaises(BeaconGeometryError, get_intersection_points, 
            (3,3,1), (3,3,1))

        # return set of 2 (possible identical) points if circles intersect
        (x1,y1), (x2,y2) = get_intersection_points((4,4,1.5), (4,7,1.5))
        (x3,y3), (x4,y4) = get_intersection_points(
                            Circle(x=4,y=4,r=1.5), 
                            Circle(x=4,y=7,r=1.5))
        self.assertEqual(set([(x3,y3), (x4,y4)]), set([(x1,y1), (x2,y2)]))
        self.assertEqual((x1,y1), (x2,y2))
        self.assertAlmostEqual(x1, 4)
        self.assertAlmostEqual(y1, 5.5)
        
        (x1,y1), (x2,y2) = get_intersection_points((4,4,2.5), (4,7,2.5))
        (x3,y3), (x4,y4) = get_intersection_points(
                            Circle(x=4,y=4,r=2.5), 
                            Circle(x=4,y=7,r=2.5))
        self.assertEqual(set([(x3,y3), (x4,y4)]), set([(x1,y1), (x2,y2)]))
        self.assertAlmostEqual(x1, 2)
        self.assertAlmostEqual(y1, 5.5)
        self.assertAlmostEqual(x2, 6)
        self.assertAlmostEqual(y2, 5.5)
        
        (x1,y1), (x2,y2) = get_intersection_points((5,3,4), (12,3,3))
        (x3,y3), (x4,y4) = get_intersection_points(
                            Circle(x=5,y=3,r=4), 
                            Circle(x=12,y=3,r=3))
        self.assertEqual(set([(x3,y3), (x4,y4)]), set([(x1,y1), (x2,y2)]))
        self.assertEqual((x1,y1), (x2,y2))
        self.assertAlmostEqual(x1, 9)
        self.assertAlmostEqual(y1, 3)
        
        (x1,y1), (x2,y2) = get_intersection_points((5,5,5), (12,5,4))
        (x3,y3), (x4,y4) = get_intersection_points(
                            Circle(x=5,y=5,r=5), 
                            Circle(x=12,y=5,r=4))
        self.assertEqual(set([(x3,y3), (x4,y4)]), set([(x1,y1), (x2,y2)]))
        self.assertAlmostEqual(x1, 9.143, places=3)
        self.assertAlmostEqual(y1, 7.799, places=3)
        self.assertAlmostEqual(x2, 9.143, places=3)
        self.assertAlmostEqual(y2, 2.201, places=3)

        (x1,y1), (x2,y2) = get_intersection_points((6,6,3), (10,9,2))
        (x3,y3), (x4,y4) = get_intersection_points(
                            Circle(x=6,y=6,r=3), 
                            Circle(x=10,y=9,r=2))
        self.assertEqual(set([(x3,y3), (x4,y4)]), set([(x1,y1), (x2,y2)]))
        self.assertEqual((x1,y1), (x2,y2))
        self.assertAlmostEqual(x2, 8.4)
        self.assertAlmostEqual(y2, 7.8)

        (x1,y1), (x2,y2) = get_intersection_points((6,6,4), (10,9,3))
        (x3,y3), (x4,y4) = get_intersection_points(
                            Circle(x=6,y=6,r=4), 
                            Circle(x=10,y=9,r=3))
        self.assertEqual(set([(x3,y3), (x4,y4)]), set([(x1,y1), (x2,y2)]))
        self.assertAlmostEqual(x1, 7.12)
        self.assertAlmostEqual(y1, 9.84)
        self.assertAlmostEqual(x2, 10)
        self.assertAlmostEqual(y2, 6)

    def test_get_point_in_circle(self):
        # given 2 points and a circle, should return the point inside the circle
        self.assertEqual(get_point_in_circle((4,4),(10,10),(3,3,3)), (4,4))
        self.assertEqual(get_point_in_circle((10,10),(4,4),(3,3,3)), (4,4))

        self.assertEqual(get_point_in_circle(
            Point(x=4, y=4), Point(x=10, y=10), Circle(x=3, y=3, r=3)),
            Point(x=4, y=4))
        self.assertEqual(get_point_in_circle(
            Point(x=10, y=10), Point(x=4, y=4), Circle(x=3, y=3, r=3)),
            Point(x=4, y=4))

        # raise if neither of the points are inside the given circle
        self.assertRaises(BeaconGeometryError, get_point_in_circle, 
            (3,2), (4,5), (10,10,2))
        self.assertRaises(BeaconGeometryError, get_point_in_circle, 
            Point(x=3,y=2), Point(x=4,y=5), Circle(x=10,y=11,r=2))

    def test_get_centralpoint(self):
        p = get_centralpoint((4,5), (7,6), (3,9))
        self.assertEqual(p, Point(14.0/3, 20.0/3))

        p = get_centralpoint(Point(x=4,y=5), Point(x=7,y=6), Point(x=3,y=9))
        self.assertEqual(p, Point(14.0/3, 20.0/3))

    # def test_get_centroid_center(self):
        # # 3 circles intersect in 1 point
        # p, _ = get_centroid_center([(2,8,1), (2,5,2), (5,7,3)])
        # self.assertIs(type(p), Point)
        # self.assertEqual(p.x, 2.0)
        # self.assertEqual(p.y, 7.0)

        # # 3 circles share an area delimited by 3 intersection points
        # p, _ = get_centroid_center([(2,8,1.5), (2,5,2.5), (5,7,3.5)])
        # self.assertIs(type(p), Point)
        # self.assertAlmostEqual(p.x, 2.101, places=3)
        # self.assertAlmostEqual(p.y, 7.066, places=3)

if __name__ == '__main__':
    unittest.main()
