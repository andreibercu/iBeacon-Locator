# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse_lazy
from models import Node, Beacon, NodeMeasurement, FloorMap
from forms import MapForm, BeaconForm, NodeForm, NodeMeasurementForm

from datetime import datetime
from beaconlocator import BeaconLocator, BeaconLocatorError
from areaexplorer import AreaExplorer as AE
from rssifilters import gmm_filter
import json
import copy
import csv
import os

class BeaconListView(ListView):
    queryset = Beacon.objects.all()
    template_name = 'ibeaconapp/beacon_list.html'

class BeaconDetailView(DetailView):
    queryset = Beacon.objects.all()
    template_name = 'ibeaconapp/beacon_detail.html'

class MyAccountBeaconListView(LoginRequiredMixin, ListView):
    template_name = 'ibeaconapp/myaccount_beacon_list.html'
    
    def get_queryset(self):
        return Beacon.objects.filter(owner=self.request.user)
    
class BeaconCreateView(LoginRequiredMixin, CreateView):
    form_class = BeaconForm
    template_name = 'form.html'
    success_url = reverse_lazy('beacons:myaccount-beacon-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(BeaconCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(BeaconCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(BeaconCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Beacon'
        return context

class BeaconUpdateView(LoginRequiredMixin, UpdateView):
    form_class = BeaconForm
    template_name = 'form.html'
    success_url = reverse_lazy('beacons:myaccount-beacon-list')

    def get_queryset(self):
        return Beacon.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super(BeaconUpdateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(BeaconUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Beacon'
        return context

class BeaconLocationView(TemplateView):
    template_name = 'ibeaconapp/beacon_location.html'

    def get_context_data(self, *args, **kwargs):
        beacon = get_object_or_404(Beacon, pk=self.kwargs.get("pk"))
        nodes = self.nodes_on_map(beacon.floor_map)

        _measurements = self.node_measurements_fromdb(nodes, beacon.pk)

        measurements = self.measurements_for_beaconlocator(_measurements)
        location, locator_nodes = self.locate_beacon(
                            beacon.floor_map, copy.deepcopy(measurements))

        measurements_info = self.measurements_for_template(
                            _measurements, locator_nodes)
        useless_nodes = self.not_used_nodes(nodes, locator_nodes)

        context = {
            'beacon': beacon,
            'floor_map': beacon.floor_map,
            'locator_nodes_json': json.dumps(locator_nodes),
            'locator_nodes': locator_nodes,
            'measurements': measurements_info,
            'useless_nodes_json': json.dumps(useless_nodes),
            'location': location,
        }

        return context

    @staticmethod
    def nodes_on_map(floor_map):
        """ get nodes on the map """
        nodes = floor_map.node_set.all() if floor_map else []
        nodes = [node for node in nodes \
                    if node.x_loc is not None \
                    and node.y_loc is not None]

        return nodes

    @staticmethod
    def node_measurements_fromdb(nodes, beacon_id):
        """ get the last measurements from each node on the map """
        _measurements = {}
        for n in nodes:
            _measurements[n] = NodeMeasurement.objects\
                    .filter(beacon__id=beacon_id, node=n)\
                    .order_by('-timestamp')[:settings.RSSI_COUNT]

        return _measurements

    @staticmethod
    def measurements_for_template(measurements, locator_nodes):
        """ create a measurements dict for useful template information """
        measurements_info = {}
        for node, values in measurements.items():
            measurements_info[node.name] = {
                'node_x_loc': round(node.x_loc, 2),
                'node_y_loc': round(node.y_loc, 2),
                'rssi_1m': round(node.rssi_1m, 2),
                'count': values.count(),
                'first': list(values)[-1].timestamp if values else None,
                'last': list(values)[0].timestamp if values else None,
                'distance': None,
            }
            try:
                measurements_info[node.name]['distance'] = \
                    round(locator_nodes[node.name]['distance'], 2)
            except KeyError:
                pass

        return measurements_info

    @staticmethod
    def measurements_for_beaconlocator(measurements):
        """ create a measurements dict for the BeaconLocator """
        _measurements = {}
        for node,values in [(n,vs) for (n,vs) in measurements.items() if vs]:
            _measurements[node] = [float(m.rssi) for m in values]

        return _measurements

    @staticmethod
    def locate_beacon(floor_map, measurements):
        """ calculate beacon location using the BeaconLocator """
        location = None
        locator_nodes = {}
        try:
            locator = BeaconLocator(floor_map, gmm_filter, measurements)
            location, locator_nodes = locator.locate()
        except BeaconLocatorError as e:
            #todo: show the error in the page template
            print e

        return location, locator_nodes

    @staticmethod
    def not_used_nodes(nodes, locator_nodes):
        """ nodes not used in the beacon location calculation process 
            for useful template information """
        useless_nodes = {}
        for node in [node for node in nodes if node.name not in locator_nodes]:
            useless_nodes[node.name] = {
                'x': node.x_loc,
                'y': node.y_loc,
            }

        return useless_nodes

class MapListView(ListView):
    queryset = FloorMap.objects.all()
    template_name = 'ibeaconapp/map_list.html'

class MapDetailView(DetailView):
    # todo
        # get nodes attached to the map and their location
        # get beacons attached to the map and their location
        # show all nodes and beacons on the map
    queryset = FloorMap.objects.all()
    template_name = 'ibeaconapp/map_detail.html'

class MyAccountMapListView(LoginRequiredMixin, ListView):
    template_name = 'ibeaconapp/myaccount_map_list.html'
    
    def get_queryset(self):
        return FloorMap.objects.filter(owner=self.request.user)

class MapCreateView(LoginRequiredMixin, CreateView):
    form_class = MapForm
    template_name = 'form.html'
    success_url = reverse_lazy('beacons:myaccount-map-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(MapCreateView, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(MapCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Floor Map'
        return context

class MapUpdateView(LoginRequiredMixin, UpdateView):
    form_class = MapForm
    template_name = 'form.html'
    success_url = reverse_lazy('beacons:myaccount-map-list')

    def get_queryset(self):
        return FloorMap.objects.filter(owner=self.request.user)

    def get_context_data(self, *args, **kwargs):
        context = super(MapUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Floor Map'
        return context

class NodeListView(ListView):
    queryset = Node.objects.all()
    template_name = 'ibeaconapp/node_list.html'

class NodeDetailView(DetailView):
    queryset = Node.objects.all()
    template_name = 'ibeaconapp/node_detail.html'
    
class MyAccountNodeListView(LoginRequiredMixin, ListView):
    template_name = 'ibeaconapp/myaccount_node_list.html'
    
    def get_queryset(self):
        return Node.objects.filter(owner=self.request.user)

class NodeCreateView(LoginRequiredMixin, CreateView):
    form_class = NodeForm
    template_name = 'form.html'
    success_url = reverse_lazy('beacons:myaccount-node-list')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.owner = self.request.user
        return super(NodeCreateView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(NodeCreateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(NodeCreateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Add Node'
        return context

class NodeUpdateView(LoginRequiredMixin, UpdateView):
    form_class = NodeForm
    template_name = 'form.html'
    success_url = reverse_lazy('beacons:myaccount-node-list')

    def get_queryset(self):
        return Node.objects.filter(owner=self.request.user)

    def get_form_kwargs(self):
        kwargs = super(NodeUpdateView, self).get_form_kwargs()
        kwargs['owner'] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(NodeUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Node'
        return context

@csrf_exempt
def add_measurement(request):
    # todo: check node - node name, password - is allowed to write to the db
    # todo: check timestamp <= datetime.now()

    form = NodeMeasurementForm(request.POST or None)

    if form.is_valid():
        timestamp_str = form.cleaned_data.get('timestamp')
        timestamp  = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        timestamp  = timezone.get_current_timezone().localize(timestamp)

        node_name  = form.cleaned_data.get("node")
        uuid       = form.cleaned_data.get("uuid")
        majorid    = form.cleaned_data.get("majorid")
        minorid    = form.cleaned_data.get("minorid")
        rssi_value = form.cleaned_data.get('rssi')

        node   = get_object_or_404(Node, name=node_name)
        beacon = get_object_or_404(
                    Beacon, uuid=uuid, majorid=majorid, minorid=minorid)

        NodeMeasurement.objects.create(
                timestamp=timestamp, node=node, 
                beacon=beacon, rssi=rssi_value)
        print "Saved measurement from {0} with timestamp: {1}".format(node_name, str(timestamp))

        message = json.dumps({'Success': True})
        return HttpResponse(message)

    if form.errors:
        raise Exception("Could not add measurement! Errors: " + \
                            str(form.errors))

def experiments_view(request):
    experiments_3nodes = []
    errors_3nodes = []
    csvpath = os.path.join(os.path.dirname(__file__), 'expected-vs-actual-3nodes.csv')
    load_experiments_fromcsv(csvpath, experiments_3nodes, errors_3nodes)
            
    experiments_4nodes = []
    errors_4nodes = []
    csvpath = os.path.join(os.path.dirname(__file__), 'expected-vs-actual-4nodes.csv')
    load_experiments_fromcsv(csvpath, experiments_4nodes, errors_4nodes)

    map_3nodes = {'width': 5, 'height': 5}
    map_4nodes = {'width': 5, 'height': 5}

    context = {
        'experiments_3nodes': experiments_3nodes,
        'experiments_3nodes_json': json.dumps(experiments_3nodes),
        'avg_error_3nodes': sum(errors_3nodes) / len(errors_3nodes),
        'map_3nodes': map_3nodes,
        'map_3nodes_json': json.dumps(map_3nodes),

        'experiments_4nodes': experiments_4nodes,
        'experiments_4nodes_json': json.dumps(experiments_4nodes),
        'avg_error_4nodes': sum(errors_4nodes) / len(errors_4nodes),
        'map_4nodes': map_4nodes,
        'map_4nodes_json': json.dumps(map_4nodes),
    }

    return render(request, 'ibeaconapp/experiments.html', context)

def load_experiments_fromcsv(csvpath, experiments, errors):
    with open(csvpath, 'r') as f:
       csv_reader = csv.reader(f)
       for line in csv_reader:
           error = AE.distance((line[0],line[1]), (line[2],line[3]))
           errors.append(error)
           experiments.append({
               'expected': {'x':line[0], 'y':line[1]},
               'actual': {'x':line[2], 'y':line[3]},
               'error': AE.distance((line[0],line[1]), (line[2],line[3])),
           })

def house_experiments_view(request):
    floor_map = get_object_or_404(FloorMap, pk=38)
    context = {
        'floor_map': floor_map, 
    }
    return render(request, 'ibeaconapp/house_experiments.html', context)

