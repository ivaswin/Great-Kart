from django.contrib import admin
from .models import Products,Variations
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','stock','price','category','modified_date','is_available')
    prepopulated_fields ={ 'slug': ('product_name',)}

class VariationsAdmin(admin.ModelAdmin):
     list_display = ('products','variation_category','variation_value','is_active')
     list_editable =('is_active',)
     list_filter = ('products','variation_category','variation_value','is_active')
    
admin.site.register(Products,ProductAdmin)
admin.site.register(Variations,VariationsAdmin)
