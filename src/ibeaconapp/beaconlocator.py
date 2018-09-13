from areaexplorer import AreaExplorer

class BeaconLocatorError(Exception):
    pass
        
class BeaconLocator(object):

    def __init__(self, floor_map, rssi_filter, measurements, limit_pernode=5):   
        #self.rssi_1m = beacon.rssi_1m
        self.map = floor_map

        # a function that can filter rssi values
        self.rssi_filter = rssi_filter

        # remove nodes with less than x measurements
        for node in measurements.keys():
            if not measurements[node] or \
               len(measurements[node]) < limit_pernode:
                measurements.pop(node)

        # raise exception if not enough measurements to compute location
        if len(measurements.keys()) < 3:
            raise BeaconLocatorError(
                ("The beacon was detected more than {0} times by {1} "
                 "nodes. For a precise localization the beacon has to be "
                 "detected by at least 3 nodes!").format(
                 limit_pernode, len(measurements.keys())))

        # raise exception if any node doesn't have x,y coordinates
        for node in measurements.keys():
            if node.x_loc is None or node.y_loc is None:
                raise BeaconLocatorError(("The node '{0}' doesn't have "
                    "the x,y coordinates specified!").format(node))

        self.measurements = measurements

    def locate(self):
        nodes = self.compute_distances()
        
        explorer = AreaExplorer(nodes, epsilon=1.5, step=0.05,
                x_limit=self.map.length, y_limit=self.map.width)
        location = explorer.run()

        return location, nodes

    def compute_distances(self):
        """ get distances between the beacon and each node based on the rssi values """
        nodes = {}
        for node in self.measurements.keys():
            nodes[node.name] = {
                'x': node.x_loc,
                'y': node.y_loc,
                'distance': self.distance_from_node(node)
            }
            
        return nodes

    def distance_from_node(self, node):
        rssi = self.rssi_filter(self.measurements[node])
        #rssi_1m = self.rssi_1m
        rssi_1m = node.rssi_1m
        n = self.map.nconst
        
        d = 10 ** ( (rssi_1m - rssi) / (10*float(n)) )
        
        return d
