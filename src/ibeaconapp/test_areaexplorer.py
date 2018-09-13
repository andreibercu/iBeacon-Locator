from areaexplorer import *

import unittest


class TestAreaExplorer(unittest.TestCase):

    def setUp(self):
        pass
    
    def test_3nodes_1point_intersection(self):
        nodes = {
            'node1': {'x': 2, 'y':8, 'distance':1},
            'node2': {'x': 2, 'y':5, 'distance':2},
            'node3': {'x': 5, 'y':7, 'distance':3},
        }
        explorer = AreaExplorer(nodes)
        location = explorer.run()
        
        self.assertIs(type(location), Point)
        self.assertAlmostEqual(location.x, 2.0)
        self.assertAlmostEqual(location.y, 7.0)
        
    def test_3nodes_common_area(self):
        nodes = {
            'node1': {'x': 2, 'y':8, 'distance':1.5},
            'node2': {'x': 2, 'y':5, 'distance':2.5},
            'node3': {'x': 5, 'y':7, 'distance':3.5},
        }
        
        explorer = AreaExplorer(nodes)
        location = explorer.run()
        
        self.assertIs(type(location), Point)
        self.assertAlmostEqual(location.x, 1.05)
        self.assertAlmostEqual(location.y, 7.05)
        
    def test_3nodes_no_intersection(self):
        nodes = {
            'node1': {'x': 2, 'y':8, 'distance':0.5},
            'node2': {'x': 2, 'y':5, 'distance':1.5},
            'node3': {'x': 5, 'y':7, 'distance':2.5},
        }
        
        explorer = AreaExplorer(nodes)
        location = explorer.run()
        
        self.assertIs(type(location), Point)
        self.assertAlmostEqual(location.x, 2.15)
        self.assertAlmostEqual(location.y, 7.25)

if __name__ == '__main__':
    unittest.main()
