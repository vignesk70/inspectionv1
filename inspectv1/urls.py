from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

app_name = 'inspectv1'
urlpatterns = [
    #display home page
    path('',views.IndexView.as_view(), name='index'),
    path('add/',views.Add,name='add'),
    path('inspection/',views.ShowInspectionData.as_view(),name='inspectiondata'),
    path('accounts/', include('django.contrib.auth.urls')),
]