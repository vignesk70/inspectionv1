from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = InspectionCategory
        fields = ("category",)

CategoryItemsFormSet = inlineformset_factory(InspectionCategory,ItemInCategory, fields=("items",))
