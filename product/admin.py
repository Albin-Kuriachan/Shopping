from django.contrib import admin
from .models import *

admin.site.register(Category)

class QuantityeInline(admin.TabularInline):
    model = Quantity
    extra = 0

@admin.register(ProductDetails)
class ProductDetailsAdmin(admin.ModelAdmin):
    inlines = [QuantityeInline]
    list_display = ('id','product_name', 'display','total_quantity','image')
    # list_filter = ('display', 'category')
    search_fields = ('product_name', 'description')
    ordering = ('product_name',)
    filter_horizontal = ('category',)