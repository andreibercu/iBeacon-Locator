from collections import namedtuple
import numpy as np
import math

Point = namedtuple('Point', 'x y')

class AreaExplorer(object):

    def __init__(self, nodes, epsilon=1.0, step=0.05, 
                 x_limit=None, y_limit=None):
        self.nodes = nodes
        self.step = step
        self.x_limit = x_limit
        self.y_limit = y_limit

        weights = {}
        for name, values in nodes.items():
            weights[name] = 1.0 / (values['distance'] ** epsilon)
        self.weights = weights

    def run(self):
        x_min, x_max, y_min, y_max = self.area_delimiters()

        estimate = (x_min, y_min)
        minsum = self.nodes_sum(estimate)
        for location in [(float(x), float(y)) \
                for x in np.arange(x_min, x_max, self.step) \
                for y in np.arange(y_min, y_max, self.step)]:
            crt_sum = self.nodes_sum(location)
            if crt_sum < minsum:
                estimate = location
                minsum = crt_sum

        return Point(x=estimate[0], y=estimate[1])

    def area_delimiters(self):
        x_min = min([n['x'] - n['distance'] for n in self.nodes.values()])
        x_min = max(x_min, 0)

        x_max = max([n['x'] + n['distance'] for n in self.nodes.values()])
        x_max = min(x_max, self.x_limit) if self.x_limit else x_max

        y_min = min([n['y'] - n['distance'] for n in self.nodes.values()])
        y_min = max(y_min, 0)

        y_max = max([n['y'] + n['distance'] for n in self.nodes.values()])
        y_max = min(y_max, self.y_limit) if self.y_limit else y_max

        return x_min, x_max, y_min, y_max   

    def nodes_sum(self, location):
        s = 0
        for name, values in self.nodes.items():
            node_center = (values['x'], values['y'])
            d = self.distance(location, node_center) - values['distance']
            s += self.weights[name] * (d**2)

        return s

    @staticmethod
    def distance(p1, p2):
        """ returns the distance between 2 points """
        (x1,y1), (x2,y2) = p1, p2

        dx = float(x1) - float(x2)
        dy = float(y1) - float(y2)
        d = math.sqrt( dx**2 + dy**2 )

        return d
