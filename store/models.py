from django.db import models
from category.models import Category
from django.urls import reverse
# Create your models here.

class Products(models.Model):
    product_name    = models.CharField(max_length=200,unique=True)
    slug            = models.CharField(max_length=200,unique=True)
    description     = models.TextField(max_length=500,blank=True)
    price           = models.IntegerField()
    image           = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField()
    category        = models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_name
    
    def get_url(self):
        return reverse('products_details',args=[self.category.slug, self.slug])
    
class VariationsManager(models.Manager):
    def colors(self):
        return super(VariationsManager,self).filter(variation_category ='color',is_active=True)
    
    def size(self):
        return super(VariationsManager,self).filter(variation_category ='size',is_active = True)

variation_category_choice =(
    ('color','color'),
    ('size','size'),
)

class Variations(models.Model):
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices= variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField()
    date_created = models.DateTimeField(auto_now=True) 

    objects = VariationsManager()

    def __str__(self):
        return self.variation_value

