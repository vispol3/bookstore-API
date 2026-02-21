from django.contrib import admin

from .models import OrderItemModel, OrderModel

# Register your models here.
admin.site.register(OrderModel)
admin.site.register(OrderItemModel)
