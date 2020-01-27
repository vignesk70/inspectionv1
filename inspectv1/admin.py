from django.contrib import admin
from .models import *
admin.AdminSite.site_header='Inspect'
# Register your models here.
admin.site.register(InspectionCategory)
admin.site.register(ItemInCategory)
admin.site.register(Sites)