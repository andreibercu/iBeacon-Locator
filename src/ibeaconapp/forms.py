from django import forms
from django.contrib.auth import get_user_model
from models import FloorMap, Beacon, Node

User = get_user_model()

class MapForm(forms.ModelForm):
    class Meta:
        model = FloorMap
        fields = [
            'name',
            'nconst',
            'length',
            'width',
            'image',
        ]

class BeaconForm(forms.ModelForm):
    class Meta:
        model = Beacon
        fields = [
            'floor_map',
            'uuid',
            'majorid',
            'minorid',
            'mac_address',
        ]

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super(BeaconForm, self).__init__(*args, **kwargs)
        self.fields['floor_map'].queryset = FloorMap.objects.filter(owner=owner)

class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = [
            'floor_map',
            'name',
            'x_loc',
            'y_loc',
            'rssi_1m',
        ]

    def __init__(self, *args, **kwargs):
        owner = kwargs.pop('owner')
        super(NodeForm, self).__init__(*args, **kwargs)
        self.fields['floor_map'].queryset = FloorMap.objects.filter(owner=owner)

class NodeMeasurementForm(forms.Form):
    timestamp = forms.CharField()
    node      = forms.CharField()
    uuid      = forms.CharField()
    majorid   = forms.CharField()
    minorid   = forms.CharField()
    rssi      = forms.FloatField()

