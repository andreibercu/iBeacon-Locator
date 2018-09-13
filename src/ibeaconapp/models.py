# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_image_file_extension, MinValueValidator
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL

def validate_strictpositive(value):
    if value <= 0:
        raise ValidationError("{0} value is not a strict positive number".format(value))


class TrackedModel(models.Model):
    owner          = models.ForeignKey(User)
    created        = models.DateTimeField(auto_now_add=True, editable=False)
    lastmodified   = models.DateTimeField(auto_now=True, editable=False)

class FloorMap(TrackedModel):
    name   = models.CharField(max_length=120, unique=True)
    image  = models.ImageField(
                upload_to='map_images', null=True, blank=True, 
                validators=[validate_image_file_extension])
    nconst = models.FloatField(null=True, blank=True,
                validators=[validate_strictpositive]) # signal loss factor
    length = models.FloatField(validators=[validate_strictpositive]) # meters
    width  = models.FloatField(validators=[validate_strictpositive]) # meters

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('beacons:map-detail', kwargs={'pk': self.pk})
        
class Node(TrackedModel):
    floor_map = models.ForeignKey(FloorMap, 
                    on_delete=models.SET_NULL, null=True, blank=True)
    name      = models.CharField(max_length=120, unique=True)
    x_loc     = models.FloatField(null=True, blank=True, 
                    validators=[MinValueValidator(0)])
    y_loc     = models.FloatField(null=True, blank=True, 
                    validators=[MinValueValidator(0)])
    rssi_1m   = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return reverse('beacons:node-detail', kwargs={'pk': self.pk})

class Beacon(TrackedModel):
    floor_map = models.ForeignKey(FloorMap, 
                on_delete=models.SET_NULL, null=True, blank=True)
    uuid      = models.CharField(max_length=120)
    majorid   = models.CharField(max_length=120)
    minorid   = models.CharField(max_length=120)
    mac_address = models.CharField(max_length=120, blank=True)

    class Meta:
        unique_together = ('uuid', 'majorid', 'minorid')

    def __str__(self):
        return "(UUID: {0}, Major ID: {1}, Minor ID: {2})".format(
            self.uuid, self.majorid, self.minorid)
            
    def get_absolute_url(self):
        return reverse('beacons:beacon-detail', kwargs={'pk': self.pk})

class NodeMeasurement(models.Model):
    timestamp = models.DateTimeField()
    node      = models.ForeignKey(Node, on_delete=models.CASCADE)
    beacon    = models.ForeignKey(Beacon, on_delete=models.CASCADE)
    rssi      = models.FloatField()
    
    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return "(time: {0}, node: {1}, beacon: {2}, rssi value: {3})".format(
            self.timestamp.strftime("%Y-%m-%d %H:%M:%S"), self.node, 
            self.beacon, self.rssi)


