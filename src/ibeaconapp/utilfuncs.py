
from areaexplorer import AreaExplorer as AE
import math

distance = AE.distance

def x2(x1, y1, d, y2):
    x1, y1, d, y2 = float(x1), float(y1), float(d), float(y2)
    aux = math.sqrt((d+y1-y2)*(d-y1+y2))
    return x1 - aux, x1 + aux

def y2(x1, y1, d, x2):
    x1, y1, d, x2 = float(x1), float(y1), float(d), float(x2)
    aux = math.sqrt((d+x1-x2)*(d-x1+x2))
    return y1 - aux, y1 + aux

node1 = (0.0,5.0)
node2 = (0.0,0.0)
node3 = (5.0,0.0)
node4 = (5.0,5.0)

rssi = {
    1: -45.8,
    2: -48.7,
    3: -50.9,
    4: -52.4,
    5: -55.1,
    6: -55.2,
    7: -55.3,
    8: -55.4,
    9: -55.5,
    10: -55.6,
}

def get_rssi(d):
    under = rssi[int(d)]
    over = rssi[int(d) + 1]
    rssi_diff = over - under
    
    d_diff = d-int(d)
    perc = d_diff 
    
    result = under + perc * rssi_diff
    return result

def get_distance(rssi, n=1.2, rssi_1m=-45.8):
    d = 10 ** ( (rssi_1m - rssi) / (10*float(n)) )
    return d

n_dict = {
    1: 1.2,
    2: 1.4,
    3: 1.6,
    4: 1.8,
}

rssi_1m_dict = {
    1: -47,
    2: -46,
    3: -45,
    4: -44,
}

#print "x\ty\td1\trssi1\td2\trssi2\td3\trssi3\tloc.x\tloc.y\terror"
#print "x,y,d1,rssi1,d2,rssi2,d3,rssi3,loc.x,loc.y,error"
print "expected_x,expected_y,measured_x,measured_y"
for x,y in [(float(x),float(y)) for x in range(1,5) for y in range(1,5)]:
    d1 = round(distance((x,y), node1), 2)
    d2 = round(distance((x,y), node2), 2)
    d3 = round(distance((x,y), node3), 2)
    d4 = round(distance((x,y), node4), 2)

    rssi1 = get_rssi(d1)
    rssi2 = get_rssi(d2)
    rssi3 = get_rssi(d3)
    rssi4 = get_rssi(d4)

    dr1 = get_distance(rssi1, n=1.2, rssi_1m=-45.8)
    dr2 = get_distance(rssi2, n=1.2, rssi_1m=-45.8)
    dr3 = get_distance(rssi3, n=1.2, rssi_1m=-45.8)
    dr4 = get_distance(rssi4, n=1.2, rssi_1m=-45.8)

    nodes = {}
    nodes["1"] = {
        'x': 0.0,
        'y': 5.0,
        'distance': dr1,
    }
    nodes["2"] = {
        'x': 0.0,
        'y': 0.0,
        'distance': dr2,
    }
    nodes["3"] = {
        'x': 5.0,
        'y': 0.0,
        'distance': dr3,
    }
    # nodes["4"] = {
        # 'x': 5.0,
        # 'y': 5.0,
        # 'distance': dr4,
    # }

    explorer = AE(nodes, epsilon=1.5, step=0.05,
                  x_limit=10, y_limit=10)
    location = explorer.run()
    
    error = distance((x,y), location)
            
    # print "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}"\
        # .format(
            # x,y,
            # round(d1,2), round(rssi1, 2),
            # round(d2,2), round(rssi2, 2),
            # round(d3,2), round(rssi3, 2),
            # round(location.x,2), round(location.y,2),
            # round(error, 2))
    print "{0},{1},{2},{3}".format(
            x, y, round(location.x,2), round(location.y,2))
            