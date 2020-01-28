from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from inspectv1.models import *

# Create your views here.
class IndexView(TemplateView):
    template_name = "inspectv1/index.html"

    
class ShowInspectionData(ListView):
    template_name = "inspectv1/updateinspection.html"
   # model=ItemInCategory

    #fields = ['category','items']
    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()
    