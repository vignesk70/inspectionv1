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
    FIELDTYPE = ( ('checkbox','CheckBox'),
    ('text','Textfield'),('number','NumberField'),('date','DateField'))
    site_no = models.IntegerField("Site Number")
    name = models.CharField("Site name", max_length=100)
    latitude = models.FloatField("Latitude")
    longitude = models.FloatField("Longitude")
    state =  models.CharField("State", max_length=50)
    postcode = models.CharField("Postcode", max_length=20)
    address = models.CharField("Address", max_length=300)
    subsdiary = models.CharField("Subsdiary",max_length=300,choices=FIELDTYPE)
    capacity=models.CharField("Capacity",max_length=300,default=' ')
    incomer=models.CharField("Incomer",max_length=300,default=' ')
    msbyear=models.CharField("Msb Year",max_length=300,default=' ')
    stoffice=models.CharField("ST Office",max_length=300,default=' ')

    

    class Meta:
        verbose_name = "Site"
        verbose_name_plural = "Sites"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("site_detail", kwargs={"pk": self.pk})


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

class Inspected_Item(models.Model):

    #Cat= models.ForeignKey("InspectionCategory", on_delete=models.CASCADE, default=0)
    S_id=models.IntegerField("Site Id",default='0')
    Ins_id=models.IntegerField("Inspector Id",default='0')
    #c_id=models.IntegerField("Category Id",default='0')
    item_id=models.IntegerField("Item Id",default='0')

    field_value = models.CharField("value", max_length=100,default=" ")
    items = models.CharField("items", max_length=100,default=" ")
    status=models.CharField("checked", max_length=100,default=" ")

    '''class Meta:
        verbose_name = "Inspeced_Item"
        verbose_name_plural = "Inspected_Items"'''

    '''def __str__(self):
        return self.S_id,self.Ins_id,self.item_id,self.field_value'''

    def __str__(self):
        template = '{0.S_id} {0.Ins_id} {0.item_id}'
        return template.format(self)



    



    
