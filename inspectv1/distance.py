
import os,sys
sys.path.append('/Users/vignes/Documents/Development/inspection')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "inspection.settings")
import django
django.setup()
from math import radians, sin, cos, acos
from inspectv1.models import *
import operator


def distance(slat, slon, elat, elon):
    slat = radians(float(slat))
    slon = radians(float(slon))
    elat = radians(float(elat))
    elon = radians(float(elon))
    dist = 6371.01 * acos(sin(slat) * sin(elat) + cos(slat) * cos(elat) * cos(slon - elon))
    return dist

slat = 3.081848  #these values  to come from browser geolocation
slon = 101.630661


sites = Sites.objects.all()
site_dict = {}
for site in sites:
    dist = distance(slat, slon, site.latitude, site.longitude)
    #print('{}-{:.2f}'.format(site.id, dist))
    site_dict[site.name]=dist
    x = site_dict
    sorted_x = sorted(x.items(), key=lambda kv: kv[1])
print(sorted_x[:3]) #return closest 3 sites. the values from here are to be passed to UI for selection by the inspector

