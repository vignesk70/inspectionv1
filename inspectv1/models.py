from django.db import models
from django.conf import settings



# Create your models here.
class InspectionCategory(models.Model):
    category = models.CharField("Category", max_length=200)
    sequence = models.IntegerField("Sequence")
    

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['sequence',]

    def __str__(self):
        return self.category

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})   
 
class ItemInCategory(models.Model):
    FIELDTYPE = ( ('checkbox','CheckBox'),
    ('text','Textfield'),('number','NumberField'),('date','DateField'))

    '''ERRORTYPE = [ ('Statutory','Statutory'),
    ('Safety','Safety'),('Engineering','Engineering'),('Operations','Operations')]'''

    ERRORTYPE = [ ('CHECKBOX','Statutory'),
    ('TEXTFIELD','Safety'),('NUMBER','Engineering'),('DATEFIELD','Operations')]
    category = models.ForeignKey("InspectionCategory", verbose_name="Category", on_delete=models.CASCADE, related_name='items', default=3)
    items = models.CharField("Item", max_length=200)
    throw_error = models.BooleanField("Throw error if True")
    sequence = models.IntegerField("Sequence")
    fieldtype = models.CharField(max_length=20, choices=FIELDTYPE) 
    #errortype= models.CharField(max_length=20,choices=ERRORTYPE)
    
    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"
        ordering = ['sequence',]

    def __str__(self):
        return self.items

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"pk": self.pk})


class Sites(models.Model):
    site_no = models.IntegerField("Site Number")
    name = models.CharField("Site name", max_length=100)
    latitude = models.FloatField("Latitude")
    longitude = models.FloatField("Longitude")
    state =  models.CharField("State", max_length=50)
    postcode = models.CharField("Postcode", max_length=20)
    address = models.CharField("Address", max_length=300)
    

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("site_detail", kwargs={"pk": self.pk})

class Shyam(models.Model):
    
    sno = models.CharField("Site no", max_length=100,default=" ")
    items = models.CharField("items", max_length=100,default=" ")
    field_value = models.CharField("value", max_length=100,default=" ")
    items = models.CharField("items", max_length=100,default=" ")
    status=models.CharField("checked", max_length=100,default=" ")

class InspectionDetails(models.Model):
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    com_lev = models.CharField("Competancy Level", max_length=200)
    com_cert = models.CharField("Competancy Certificate", max_length=200)
    signature= models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100)
    
    class Meta:
        verbose_name = "Inspectordetail"
        verbose_name_plural = "Inspectordetails"
        

    def __str__(self):
        return self.com_lev



    
