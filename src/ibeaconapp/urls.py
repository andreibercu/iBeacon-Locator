from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy

from views import (
    MapListView,
    MapDetailView,
    MyAccountMapListView,
    MapUpdateView,
    MapCreateView,
    NodeListView,
    NodeDetailView,
    MyAccountNodeListView,
    NodeUpdateView,
    NodeCreateView,
    BeaconListView,
    BeaconDetailView,
    MyAccountBeaconListView,
    BeaconUpdateView,
    BeaconCreateView,
    BeaconLocationView,
    add_measurement,
    experiments_view,
    house_experiments_view,
)

urlpatterns = [
    url(r'^$', 
        BeaconListView.as_view(), name='beacon-list'),
    url(r'^(?P<pk>\d+)/$', 
       BeaconDetailView.as_view(), name='beacon-detail'),
    url(r'^(?P<pk>\d+)/edit/$', 
        BeaconUpdateView.as_view(), name='beacon-edit'),
    url(r'^create/$', 
        BeaconCreateView.as_view(), name='beacon-create'),
    url(r'^(?P<pk>\d+)/location/$', 
        BeaconLocationView.as_view(), name='beacon-location'),

    url(r'^maps/$', 
        MapListView.as_view(), name='map-list'),
    url(r'^maps/(?P<pk>\d+)/$', 
       MapDetailView.as_view(), name='map-detail'),
    url(r'^maps/(?P<pk>\d+)/edit$', 
        MapUpdateView.as_view(), name='map-edit'),
    url(r'^maps/create/$', 
        MapCreateView.as_view(), name='map-create'),

    url(r'^nodes/$', 
        NodeListView.as_view(), name='node-list'),
    url(r'^nodes/(?P<pk>\d+)/$', 
       NodeDetailView.as_view(), name='node-detail'),
    url(r'^nodes/(?P<pk>\d+)/edit$', 
        NodeUpdateView.as_view(), name='node-edit'),
    url(r'^nodes/create/$', 
        NodeCreateView.as_view(), name='node-create'),

    url(r'^experiments/$', 
        experiments_view, name='experiments'),
    url(r'^house-experiments/$', 
        house_experiments_view, name='house-experiments'),
    url(r'^add_measurement/$', add_measurement),
    
    url(r'^myaccount/$',
        RedirectView.as_view(
            url=reverse_lazy('beacons:myaccount-map-list')), 
        name='myaccount'),
    url(r'^myaccount/maps/$', 
        MyAccountMapListView.as_view(), name='myaccount-map-list'),
    url(r'^myaccount/beacons/$', 
        MyAccountBeaconListView.as_view(), name='myaccount-beacon-list'),
    url(r'^myaccount/nodes/$', 
        MyAccountNodeListView.as_view(), name='myaccount-node-list'),

]
