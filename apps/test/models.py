from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from apps.setup.models import *


class Isp(models.Model):
    class Meta:
        verbose_name = 'ارائه دهنده خدمات'
        verbose_name_plural = 'ارائه دهندگان خدمات'

    CLOUD_CHOICE = (
        ('True', 'True'),
        ('False', 'False')
    )


    name = models.CharField(verbose_name='اسم', blank=True, null=True,max_length=80)
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

    name = models.CharField(max_length=80, verbose_name='اسم')
    url = models.URLField(max_length=200, verbose_name='آدرس وب‌سایت', blank=True, null=True)
    isp = models.ForeignKey(Isp, verbose_name='ارائه دهنده خدمات',on_delete=models.PROTECT, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='کشور', on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name
