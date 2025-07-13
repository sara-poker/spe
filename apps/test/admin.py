from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *

class OperatorAdmin(admin.ModelAdmin):
    list_per_page = 30

class IspAdmin(admin.ModelAdmin):
    list_per_page = 30


admin.site.register(Operator, OperatorAdmin)
admin.site.register(Isp, IspAdmin)
