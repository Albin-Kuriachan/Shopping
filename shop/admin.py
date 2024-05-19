from django.contrib import admin
from .models import *

admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Payment)
admin.site.register(Review)
# admin.site.register(User_Data)

class Cartline(admin.TabularInline):
    model = Cart
    extra = 0

@admin.register(User_Data)
class CandidateProfileAdmin(admin.ModelAdmin):
    inlines = [Cartline]
