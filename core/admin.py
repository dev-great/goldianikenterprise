from django.contrib import admin
from .models import ContactUs, Meal, ShippingAddress, Order, OrderItem, Subscriber, Tag, Testimonial


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'id')
    search_fields = ('name', 'id')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'id')
    search_fields = ('first_name', 'last_name', 'city', 'id')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_on')
    search_fields = ('id', 'user__email', 'status')
    list_filter = ('status', 'created_on')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'meal', 'quantity', 'subtotal', 'created_on')
    search_fields = ('order__id', 'meal__name', 'order__user__email')
    list_filter = ('created_on',)


admin.site.register(Tag)
admin.site.register(Testimonial)
admin.site.register(Subscriber)
admin.site.register(ContactUs)
