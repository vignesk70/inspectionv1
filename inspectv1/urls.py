'''
django urls
'''

from django.urls import path, include
from . import views
# from django.contrib.auth import views as auth_views
# from django.contrib import admin


app_name = 'inspectv1'
urlpatterns = [
    # display home page
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.Add, name='add'),
    path('getsites/', views.GetSites, name='getsites'),
    path('getcategories/', views.GetCategories, name='getcategories'),
    path('inspection/', views.ShowInspectionDataFun, name='inspectiondata'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('listsites/', views.ListSitesForInspector.as_view(), name='listsites'),
    path('getnearestsite/', views.getNearestSite, name='getnearestsite'),
    path('dashboard/', views.ShowDashboard.as_view(), name="dashboard"),
    path('inspectdetail/<int:pk>',
         views.ShowInspectionDetails.as_view(), name='inspectdetail'),
    path('test/', views.TestForm.as_view(), name="test"),
    path('dashboarddetails/<key>',
         views.ShowDashboardDetails.as_view(), name='dashdetails'),
    path('printform/<key>', views.PrintForm.as_view(), name='printform'),
    #     path('runinspection/', views.CreateInspectionForm.as_view(),
    #          name='runinspectiondata'),
    path('displayissuedetail/', views.DisplayIssueDetails, name='issuedetails'),
    path('dashdetails/<int:pk>', views.ShowInspectionDashboardTypeDetails.as_view(), name='dash2detail'),
    path('generatexlsx/',views.GenerateExcelfile.as_view(), name='generatexlsx'),
    path('genexcel/',views.genexcel,name="genexcel"),
    url(r'login_success/$', views.login_success, name='login_success'),
]
