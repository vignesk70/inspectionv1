from django.urls import path
from . import views

app_name = 'inspectv1'
urlpatterns = [
    #display home page
    path('',views.IndexView.as_view(), name='index'),
]