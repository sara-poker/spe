from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.setup.models import *
from config import settings


class Isp(models.Model):
    class Meta:
        verbose_name = 'ارائه دهنده خدمات'
        verbose_name_plural = 'ارائه دهندگان خدمات'

    CLOUD_CHOICE = (
        ('True', 'True'),
        ('False', 'False')
    )

    name = models.CharField(verbose_name='اسم', blank=True, null=True, max_length=80)
    url = models.CharField(max_length=30, verbose_name='آدرس', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='کشور', related_name='country', on_delete=models.PROTECT,
                                blank=True, null=True)
    cloud = models.CharField(max_length=18, verbose_name='وضعیت', choices=CLOUD_CHOICE, blank=True, null=True)

    def __str__(self):
        return self.name


class Operator(models.Model):
    class Meta:
        verbose_name = 'اپراتور'
        verbose_name_plural = 'اپراتورها'

    name = models.CharField(max_length=80, verbose_name='اسم')
    url = models.URLField(max_length=200, verbose_name='آدرس وب‌سایت', blank=True, null=True)
    isp = models.CharField(max_length=200, verbose_name='ارائه دهنده خدمات', blank=True, null=True)
    org = models.CharField(max_length=100, verbose_name='سازمان', blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='کشور', on_delete=models.PROTECT, blank=True, null=True)
    as_number = models.CharField(max_length=50, verbose_name='AS')
    asname = models.CharField(max_length=100, verbose_name='AS Name')

    def __str__(self):
        return self.name


class ServerTest(models.Model):
    class Meta:
        verbose_name = 'سرور تست'
        verbose_name_plural = 'سرور های تست'

    name = models.CharField(max_length=80, verbose_name='اسم', unique=True)
    url = models.URLField(max_length=200, verbose_name='آدرس وب‌سایت', blank=True, null=True, unique=True)
    isp = models.ForeignKey(Isp, verbose_name='ارائه دهنده خدمات', on_delete=models.PROTECT, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='کشور', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name


class NetworkInfo(models.Model):
    ip = models.GenericIPAddressField(verbose_name='IP', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='شهر', blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='کشور', blank=True, null=True)
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT, verbose_name='اپراتور', blank=True, null=True)

    def __str__(self):
        return f"{self.ip} - {self.city}"


class DeviceInfo(models.Model):
    os = models.CharField(max_length=100, verbose_name='سیستم‌عامل', blank=True, null=True)
    os_version = models.CharField(max_length=50, verbose_name='نسخه سیستم‌عامل', blank=True, null=True)
    machine = models.CharField(max_length=100, verbose_name='پردازنده / دستگاه', blank=True, null=True)
    browser = models.CharField(max_length=100, verbose_name='مرورگر', blank=True, null=True)
    network_kind = models.CharField(
        max_length=50,
        verbose_name='نوع اتصال',
        blank=True, null=True
    )
    mac_address = models.CharField(
        max_length=17,
        verbose_name='MAC آدرس',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.os} - {self.browser} - {self.network_kind}"


class SpeedTest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='کاربر')
    network_info = models.ForeignKey(NetworkInfo, on_delete=models.PROTECT, verbose_name='اطلاعات شبکه')
    device_info = models.ForeignKey(DeviceInfo, on_delete=models.PROTECT, verbose_name='اطلاعات دستگاه')

    ping_avg = models.FloatField(verbose_name='پینگ (ms)', blank=True, null=True)
    jitter = models.FloatField(verbose_name='جیتر (ms)', blank=True, null=True)
    packet_loss = models.FloatField(verbose_name='درصد از دست رفتن پکت', blank=True, null=True)

    speed_mbps = models.FloatField(verbose_name='سرعت دانلود (Mbps)', blank=True, null=True)
    speed_MBps = models.FloatField(verbose_name='سرعت دانلود (MB/s)', blank=True, null=True)
    loaded_size = models.FloatField(verbose_name='اندازه فایل دانلود شده (MB)', blank=True, null=True)
    load_time = models.FloatField(verbose_name='زمان دانلود (ثانیه)', blank=True, null=True)

    upload_speed_mbps = models.FloatField(verbose_name='سرعت آپلود (Mbps)', blank=True, null=True)
    upload_time = models.FloatField(verbose_name='زمان آپلود (ثانیه)', blank=True, null=True)
    upload_file_size = models.FloatField(verbose_name='حجم فایل آپلودی (MB)', blank=True, null=True)

    latency = models.FloatField(verbose_name='لَتِنسی', blank=True, null=True)
    test_state = models.CharField(max_length=20, choices=[('success', 'موفق'), ('fail', 'ناموفق')],
                                  verbose_name='وضعیت تست', blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ تست', blank=True, null=True)

    def __str__(self):
        return f"تست توسط {self.user.name} در {self.date}"
