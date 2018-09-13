# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import csv
import os

from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from views import BeaconLocationView as BLV
from models import Node, Beacon, NodeMeasurement, FloorMap
from beaconlocator import BeaconLocator, BeaconLocatorError
from rssifilters import gmm_filter
from areaexplorer import Point

from django.contrib.auth import get_user_model
User = get_user_model()


class BeaconListViewTests(TestCase):
    def test_nobeacons(self):
        response = self.client.get(reverse('beacons:beacon-list'))
        self.assertQuerysetEqual(response.context['object_list'], [])

    def test_2beacons(self):
        # create a user
        user = User.objects.create_user(
                'john', 'lennon@thebeatles.com', 'johnpassword')
        Beacon.objects.create(
                uuid="xxxx-xxx-xxx", majorid="10", 
                minorid="1", owner=user)
        Beacon.objects.create(
                uuid="xxxx-xxx-xxx", majorid="10", 
                minorid="2", owner=user)
        response = self.client.get(reverse('beacons:beacon-list'))
        self.assertQuerysetEqual(response.context['object_list'], [
            '<Beacon: (UUID: xxxx-xxx-xxx, Major ID: 10, Minor ID: 1)>',
            '<Beacon: (UUID: xxxx-xxx-xxx, Major ID: 10, Minor ID: 2)>'], 
            ordered=False)


class BeaconLocationTests(TestCase):
    def setUp(self):
        # create a user
        user = User.objects.create_user(
                'john', 'lennon@thebeatles.com', 'johnpassword')
    
        # create a map
        map = FloorMap(name="test map", length=10, width=10, 
                       nconst=1.1, owner=user)
        map.save()

        # create nodes attached to the map
        # # expected location point x=2, y=7
        Node.objects.create(name="node1", floor_map=map, rssi_1m=-45.8,
                            x_loc=2, y_loc=8, owner=user)
        Node.objects.create(name="node2", floor_map=map, rssi_1m=-45.8, 
                            x_loc=2, y_loc=5, owner=user)
        Node.objects.create(name="node3", floor_map=map, rssi_1m=-45.8,
                            x_loc=5, y_loc=7, owner=user)

        # create a beacon
        beacon = Beacon(uuid='00001803-494C-4F47-4943-544543480000', 
                    majorid='1', minorid='2', floor_map=map, owner=user)
        beacon.save()
        self.beacon = beacon

        # create measurements using the above beacon/nodes/map
        csvpath = os.path.join(os.path.dirname(__file__), 
            'test_resources', 'custom-measurements-20180306.csv')
        with open(csvpath, 'r') as f:
            csv_reader = csv.reader(f)
            for line in csv_reader:
                measurement = self.get_measurement_fromline(line)
                measurement.save()
    
    @staticmethod
    def get_measurement_fromline(line):
        timestamp = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
        tz = timezone.get_current_timezone()
        timestamp = tz.localize(timestamp)
        node = get_object_or_404(Node, name=line[1])
        beacon = get_object_or_404(
                    Beacon, uuid=line[2], majorid=line[3], minorid=line[4])
        rssi_value = int(line[5])
        
        return NodeMeasurement(
            timestamp=timestamp, node=node, beacon=beacon, rssi=rssi_value)

    def test_BeaconLocationView(self):
        settings.RSSI_COUNT=200
        response = self.client.get(reverse('beacons:beacon-location', 
                            kwargs={'pk': self.beacon.pk}))

        location = response.context['location']
        print "Estimated beacon location (expected x=2, y=7): x={0}, y={1}"\
            .format(round(location.x, 2), round(location.y, 2))
        
        self.assertIs(type(location), Point)
        self.assertIs(type(location.x), float)
        self.assertIs(type(location.y), float)

        if location.x < 2 or location.x > 2.3 or \
           location.y < 6.80 or location.y > 7.10:
            raise ValueError(
                "Expected beacon location x=2.0, y=7.0, got x={0}, y={1}"\
                .format(round(location.x, 2), round(location.y, 2)))

    def load_measurements(self):
        nodes = BLV.nodes_on_map(self.beacon.floor_map)
        _measurements = BLV.node_measurements_fromdb(nodes, self.beacon.pk)
        measurements = BLV.measurements_for_beaconlocator(_measurements)
        
        return measurements
        
    def test_beaconlocator_lessthan3nodes(self):
        # raise exception if the measurements dict has less than 3 nodes
        measurements = self.load_measurements()
        measurements.pop(get_object_or_404(Node, name="node1"))
        
        self.assertRaises(BeaconLocatorError, BeaconLocator, 
            self.beacon, gmm_filter, measurements.copy())
        
    def test_beaconlocator_notenough_rssivalues(self):
        # raise exception if the measurements dict has less than 3 nodes 
        # with more than x rssi values
        measurements = self.load_measurements()
        node1 = get_object_or_404(Node, name="node1")
        measurements[node1] = [1,2,3,4]
        
        self.assertRaises(BeaconLocatorError, BeaconLocator, 
            self.beacon, gmm_filter, measurements.copy(), limit_pernode=5)
            
    def test_beaconlocator_nonodecoords(self):
        # raise exception if any node doesn't have x,y coordinates
        node1 = get_object_or_404(Node, name="node1")
        node1.x_loc = None
        node1.save()

        floor_map = self.beacon.floor_map
        nodes = floor_map.node_set.all() if floor_map else []
        _measurements = BLV.node_measurements_fromdb(nodes, self.beacon.pk)
        measurements = BLV.measurements_for_beaconlocator(_measurements)
        
        self.assertRaises(BeaconLocatorError, BeaconLocator, 
            self.beacon, gmm_filter, measurements.copy())
        