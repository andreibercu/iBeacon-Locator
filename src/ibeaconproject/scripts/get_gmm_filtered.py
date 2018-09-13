from ibeaconapp.models import NodeMeasurement
from ibeaconapp.rssifilters import gmm_filter
import sys

RSSI_COUNT = 200

for node in ('raspberry1', 'raspberry2', 'raspberry3'):
    measurements = NodeMeasurement.objects.filter(node__name=node).order_by('-timestamp')[:RSSI_COUNT]
    if measurements.count() < RSSI_COUNT:
        print "ERROR: {0} doesn't have enough measurements!".format(node)
        continue
    rssi_values = [m.rssi for m in measurements]
    filtered = gmm_filter(rssi_values)
    print node, " - filtered:", filtered, ", count:", measurements.count(), ", first:", list(measurements)[-1].timestamp, ", last:", list(measurements)[0].timestamp



