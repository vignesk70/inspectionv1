from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin


app_name = 'inspectv1'
urlpatterns = [
    # display home page
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.Add, name='add'),
    path('getsites/', views.GetSites, name='getsites'),
    path('getcategories/', views.GetCategories, name='getcategories'),
    path('inspection/', views.ShowInspectionDataFun, name='inspectiondata'),
    path('sites/', views.ShowSiteData, name='sitedata'),
    path('runinspection/', views.CreateInspectionForm.as_view(),
         name='runinspectiondata'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('listsites/', views.ListSitesForInspector.as_view(), name='listsites'),
    path('getnearestsite/', views.getNearestSite, name='getnearestsite'),
    path('dashboard/', views.ShowDashboard.as_view(), name="dashboard"),
    path('inspectdetail/<int:pk>',
         views.ShowInspectionDetails.as_view(), name='inspectdetail'),
    path('test/', views.TestForm.as_view(), name="test"),
    path('dashboarddetails/<key>',
         views.ShowDashboardDetails.as_view(), name='dashdetails'),

]
