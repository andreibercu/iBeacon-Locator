# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import FloorMap, Node, Beacon, NodeMeasurement


class FloorMapAdmin(admin.ModelAdmin):
    list_display = ('name', 'nconst', 'length', 'width', 'owner', 'created', 'lastmodified')

class BeaconAdmin(admin.ModelAdmin):
    list_display = ('minorid', 'majorid', 'uuid', 'mac_address', 'floor_map', 'owner', 'created', 'lastmodified')

class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor_map', 'x_loc', 'y_loc', 'rssi_1m', 'owner', 'created', 'lastmodified')

class NodeMeasurementAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'node', 'beacon', 'rssi')

admin.site.register(FloorMap, FloorMapAdmin)
admin.site.register(Node, NodeAdmin)
admin.site.register(Beacon, BeaconAdmin)
admin.site.register(NodeMeasurement, NodeMeasurementAdmin)

