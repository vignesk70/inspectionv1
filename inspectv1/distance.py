
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
slat = 3.0213
slon = 101.8062


sites = Sites.objects.all()
site_dict = {}
a_dict = [None]*3
for site in sites:
    dist = distance(slat, slon, site.latitude, site.longitude)
    #print('{}-{:.2f}'.format(site.id, dist))
    site_dict[site.site_no]=dist
    x = site_dict
    sorted_x = sorted(x.items(), key=lambda kv: kv[1])

# print(sorted_x[:3]) #return closest 3 sites. the values from here are to be passed to UI for selection by the inspector


countarr = 0
for siteloc in sorted_x[:3]:
    # print(siteloc[0])
    data = sites.filter(site_no__contains=siteloc[0])
    sitevalue = str(site.site_no) + '-' + str(site.name)
    b_dict = [None] * 3
    b_dict[0] = site.site_no
    b_dict[1] = site.name
    b_dict[2] = sitevalue
    a_dict[countarr] = b_dict
    #a_dict[1] = sitevalue
    countarr += 1
    
print(a_dict)
