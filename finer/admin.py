from django.contrib import admin

from .models import User, Product , ShippingAddress , Cart , Order,OrderItem ,Feedback

admin.site.register(User)
admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Feedback)
