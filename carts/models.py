from django.db import models
from store.models import Products,Variations
from accounts.models import Accounts

# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey(Accounts,on_delete = models.CASCADE, null= True)
    product=models.ForeignKey(Products,on_delete = models.CASCADE)
    variations =models.ManyToManyField(Variations,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,null=True)
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField()

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product



