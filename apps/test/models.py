from django.db import models
from django.db.models import Avg

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

from apps.setup.models import *

from config import settings


class Isp(models.Model):
    class Meta:
        verbose_name = 'اپراتور'
        verbose_name_plural = 'اپراتورها'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['country']),
        ]

    name = models.CharField(max_length=80)
    url = models.CharField(max_length=200, blank=True, null=True)
    org = models.CharField(max_length=100, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True)
    as_number = models.CharField(max_length=50)
    asname = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class ServerTest(models.Model):
    class Meta:
        verbose_name = 'سرور تست'
        verbose_name_plural = 'سرور های تست'
        indexes = [
            models.Index(fields=['isp']),
            models.Index(fields=['country']),
        ]

    class ServerStatus(models.IntegerChoices):
        INACTIVE = 0, 'غیرفعال'
        ACTIVE = 1, 'فعال'

    name = models.CharField(max_length=80, unique=True)
    url = models.CharField(max_length=200, blank=True, null=True, unique=True)
    ip = models.GenericIPAddressField(unique=True)

    isp = models.ForeignKey(Isp, on_delete=models.PROTECT, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True)

    is_active = models.PositiveSmallIntegerField(
        choices=ServerStatus.choices,
        default=ServerStatus.ACTIVE
    )

    def __str__(self):
        return self.name


class NetworkInfo(models.Model):
    class Meta:
        verbose_name = 'اطلاعات شبکه'
        verbose_name_plural = 'اطلاعات شبکه ها'
        indexes = [
            models.Index(fields=['province']),
            models.Index(fields=['city']),
            models.Index(fields=['isp']),
            models.Index(fields=['country']),
            models.Index(fields=['province', 'isp']),
        ]

    city = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)

    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank=True, null=True)
    isp = models.ForeignKey(Isp, on_delete=models.PROTECT, blank=True, null=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.isp} - {self.city}"


class DeviceInfo(models.Model):
    class Meta:
        verbose_name = 'اطلاعات سیستم'
        verbose_name_plural = 'اطلاعات سیستم ها'
        indexes = [
            models.Index(fields=['user']),
        ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    device = models.CharField(max_length=100, blank=True, null=True)
    os = models.CharField(max_length=100, blank=True, null=True)
    os_version = models.CharField(max_length=50, blank=True, null=True)
    cpu = models.CharField(max_length=100, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)

    network_kind = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.os} - {self.browser}"


class Protocol(models.Model):
    class Meta:
        verbose_name = 'پروتکل'
        verbose_name_plural = 'پروتکل ها'
        indexes = [
            models.Index(fields=['protocol']),
            models.Index(fields=['version']),
        ]

    transport = models.CharField(max_length=100, blank=True, null=True)
    protocol = models.CharField(max_length=100, blank=True, null=True)
    version = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.protocol} {self.version}"



class SpeedTest(models.Model):
    class Meta:
        verbose_name = 'تست سرعت'
        verbose_name_plural = 'تست های سرعت'

        indexes = [
            # ----------- پایه -----------
            models.Index(fields=['date']),
            models.Index(fields=['test_state']),
            models.Index(fields=['protocol']),

            # ----------- کوئری‌های پرتکرار -----------
            models.Index(fields=['server_test', '-date']),
            models.Index(fields=['protocol', '-date']),
            models.Index(fields=['test_state', '-date']),

            models.Index(fields=['speed_mbps', '-date']),

            # ----------- فیلترهای ترکیبی سنگین -----------
            models.Index(fields=['network_info', '-date']),
            models.Index(fields=['device_info', '-date']),

            # ----------- برای join + filter -----------
            models.Index(fields=['network_info', 'test_state']),
            models.Index(fields=['server_test', 'test_state']),
            models.Index(fields=['protocol', 'test_state']),

            # ----------- range queries (speed/ping) -----------
            models.Index(fields=['speed_mbps']),
            models.Index(fields=['ping_avg']),
            models.Index(fields=['jitter']),
        ]

    class TestState(models.IntegerChoices):
        FAIL = 0, 'ناموفق'
        SUCCESS = 1, 'موفق'

    ip = models.GenericIPAddressField(blank=True, null=True)
    protocol = models.ForeignKey(Protocol, on_delete=models.PROTECT)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    network_info = models.ForeignKey(NetworkInfo, on_delete=models.PROTECT)
    device_info = models.ForeignKey(DeviceInfo, on_delete=models.PROTECT)
    server_test = models.ForeignKey(ServerTest, on_delete=models.PROTECT, null=True, blank=True)

    # metrics
    ping_avg = models.FloatField(blank=True, null=True)
    jitter = models.FloatField(blank=True, null=True)
    packet_loss = models.FloatField(blank=True, null=True)

    speed_mbps = models.FloatField(blank=True, null=True)
    load_time = models.FloatField(blank=True, null=True)

    upload_speed_mbps = models.FloatField(blank=True, null=True)
    upload_time = models.FloatField(blank=True, null=True)

    latency = models.FloatField(blank=True, null=True)

    test_state = models.PositiveSmallIntegerField(
        choices=TestState.choices,
        default=TestState.FAIL
    )

    date = models.DateTimeField(
        default=timezone.now,
        db_index=True
    )

    def __str__(self):
        return f"{self.user_id} - {self.date}"

    @classmethod
    def get_average_speed(cls, **filters):
        return cls.objects.filter(**filters).aggregate(
            avg_download=Avg('speed_mbps'),
            avg_upload=Avg('upload_speed_mbps')
        )
