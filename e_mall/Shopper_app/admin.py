from django.contrib import admin
from .models.shopper_models import Shoppers,Store
from django.contrib.auth.models import User
# Register your models here.

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('store_name','shopper_name','shop_grade','start_time','province', 'city_choice','attention')

    def shopper_name(self,obj):
        """商家名称"""
        return obj.shopper.username
    shopper_name.short_description = '商家名称'



@admin.register(Shoppers)
class ShoppersAdmin(admin.ModelAdmin):
    list_display = ('shopper',)

