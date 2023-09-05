from django.db import models

# Create your models here.

class ProductData(models.Model):
    name = models.CharField(max_length=255)
    #url = models.URLField(max_length=500)
    url = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #image_url = models.URLField(max_length=500)
    image_url = models.TextField()
    stock = models.TextField()
    review = models.TextField()