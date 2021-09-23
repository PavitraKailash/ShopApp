from django.contrib import admin
from .models import *

admin.site.register(ProductDetails)
admin.site.register(Customers)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)