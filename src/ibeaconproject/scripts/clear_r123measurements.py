from ibeaconapp.models import NodeMeasurement

print "raspberry1 count:", NodeMeasurement.objects.filter(node__name='raspberry1').count()
print "raspberry2 count:", NodeMeasurement.objects.filter(node__name='raspberry2').count()
print "raspberry3 count:", NodeMeasurement.objects.filter(node__name='raspberry3').count()
print 'clearing database ...'
NodeMeasurement.objects.filter(node__name='raspberry1').delete()
NodeMeasurement.objects.filter(node__name='raspberry2').delete()
NodeMeasurement.objects.filter(node__name='raspberry3').delete()
print "raspberry1 count:", NodeMeasurement.objects.filter(node__name='raspberry1').count()
print "raspberry2 count:", NodeMeasurement.objects.filter(node__name='raspberry2').count()
print "raspberry3 count:", NodeMeasurement.objects.filter(node__name='raspberry3').count()

