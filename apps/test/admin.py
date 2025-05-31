from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_per_page = 30


class OperatorAdmin(admin.ModelAdmin):
    list_per_page = 30


class CountryAdmin(admin.ModelAdmin):
    list_per_page = 30


class IspAdmin(admin.ModelAdmin):
    list_per_page = 30


admin.site.register(Operator, OperatorAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Isp, IspAdmin)
