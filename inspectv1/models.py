from django.db import models

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
    FIELDTYPE = [ ('CHECKBOX','CheckBox'),
    ('TEXTFIELD','Textfield'),('NUMERICFIELD','Numerical'),('DATEFIELD','Date')]
    category = models.ForeignKey("InspectionCategory", verbose_name="Category", on_delete=models.CASCADE, related_name='items')
    items = models.CharField("Item", max_length=200)
    throw_error = models.BooleanField("Throw error if True")
    sequence = models.IntegerField("Sequence")
    fieldtype = models.CharField(max_length=20, choices=FIELDTYPE) 

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
