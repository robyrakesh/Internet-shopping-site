from django.contrib import admin
from django.contrib import messages
from .models import Product, Category, Client, Order

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'getCategory', 'price', 'stock', 'available')

    def add_refills(self, request, queryset):
        for obj in queryset:
            r = obj.refill()
            if(r == 1):
                messages.add_message(request, messages.INFO, 'Product Refilled Successfully!')
            else:
                messages.add_message(request, messages.INFO, 'The stock must be between 0 to 1000!')
        queryset.update()

    add_refills.short_description = "Refill"

    actions = [add_refills]


class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'city', 'interested_in')


# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('name')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Client, ClientAdmin)
admin.site.register(Order)
