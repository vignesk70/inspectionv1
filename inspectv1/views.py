from django.shortcuts import render
from django.views.generic import TemplateView, ListView, UpdateView, CreateView
from .models import *
from django.http import HttpResponse
from .forms import *

# Create your views here.
class IndexView(TemplateView):
    template_name = "inspectv1/index.html"

    
class ShowInspectionData(ListView):
    template_name = "inspectv1/updateinspection.html"
   # model=ItemInCategory

    #fields = ['category','items']
    context_object_name = 'category'
    queryset = InspectionCategory.objects.all()
    
def Add(req):
    print("IN ADD")
    #form=InspectionForm()
    if req.method=='POST':
        form=Test(req.POST)
        if form.is_valid():
            form.save(commit=true)
    return HttpResponse("Do something")