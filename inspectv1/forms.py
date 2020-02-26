from django import forms
from django.forms import ModelForm
from .models import *
from django.forms.models import inlineformset_factory

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = InspectionCategory
        fields = ("category",)

CategoryItemsFormSet = inlineformset_factory(InspectionCategory,ItemInCategory, fields=("items",))


class RunInspection(forms.ModelForm):

    class Meta:
      model = InspectedItem
      fields = [ 'category_id', 'site_id', 'user_id', 'item_id', 'item_value', 'item_image' ]

class InspectionData(forms.ModelForm):

		class Meta:
			model = InspectItem
			fields = ['inspector_name','category_name','site_name']
			widgets = {
				'inspector_name' : forms.TextInput(attrs={'size':50}),
				'category_name' : forms.TextInput(attrs={'size':50}),
				'site_name' : forms.TextInput(attrs={'size':5})
			}

"""class ProfileForm(forms.Form):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #interests = ProfileInterest.objects.filter(
        #    profile=self.instance
        #)
        for i in range(3):
            field_name = 'interest_%s' % (i,)
            self.fields[field_name] = forms.CharField(required=False)
            try:
                self.initial[field_name] = "test_" #interests[i].interest
            except IndexError:
                self.initial[field_name] = ""
        # create an extra blank field
        field_name = 'interest_%s' % (i + 1,)
        self.fields[field_name] = forms.CharField(required=False)

    def clean(self):
        interests = set()
        i = 0
        field_name = 'interest_%s' % (i,)
        while self.cleaned_data.get(field_name):
           interest = self.cleaned_data[field_name]
           if interest in interests:
               self.add_error(field_name, 'Duplicate')
           else:
               interests.add(interest)
           i += 1
           field_name = 'interest_%s' % (i,)
           self.cleaned_data["interests"] = interests

    def save(self):
        profile = self.instance
        profile.first_name = self.cleaned_data["first_name"]
        profile.last_name = self.cleaned_data["last_name"]

        profile.interest_set.all().delete()
        for interest in self.cleaned_data["interests"]:
           ProfileInterest.objects.create(
               profile=profile,
               interest=interest,
           ) """





'''class ImageForm(forms.ModelForm):
    class Meta:
        model= Image
        fields= ["name", "imagefile"]'''