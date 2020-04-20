from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin


app_name = 'inspectv1'
urlpatterns = [
    #display home page
    path('',views.IndexView.as_view(), name='index'),
    path('add/',views.Add,name='add'),
    path('getsites/',views.GetSites,name='getsites'),
    path('getcategories/',views.GetCategories,name='getcategories'),
    #path('inspection/',views.ShowInspectionData.as_view(),name='inspectiondata'),
    path('inspection/',views.ShowInspectionDataFun,name='inspectiondata'),
    path('sites/',views.ShowSiteData,name='sitedata'),
    path('runinspection/',views.CreateInspectionForm.as_view(),name='runinspectiondata'),
    #path('inspection_test/',views.ShowInspectionDataText.as_view(),name='inspectiondataText'),
    path('accounts/', include('django.contrib.auth.urls')),
]