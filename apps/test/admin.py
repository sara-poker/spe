from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *



class IspAdmin(admin.ModelAdmin):
    list_per_page = 30


class ServerTestAdmin(admin.ModelAdmin):
    list_per_page = 30


class NetworkInfoAdmin(admin.ModelAdmin):
    list_per_page = 30


class DeviceInfoAdmin(admin.ModelAdmin):
    list_per_page = 30


class SpeedTestAdmin(admin.ModelAdmin):
    list_per_page = 30


admin.site.register(Isp, IspAdmin)
admin.site.register(ServerTest, ServerTestAdmin)
admin.site.register(NetworkInfo, NetworkInfoAdmin)
admin.site.register(DeviceInfo, DeviceInfoAdmin)
admin.site.register(SpeedTest, SpeedTestAdmin)
