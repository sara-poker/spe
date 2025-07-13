from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, name, password=None, **extra_fields):
        if not username:
            raise ValueError('Username باید وارد شود')
        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser باید is_staff=True داشته باشد.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser باید is_superuser=True داشته باشد.')

        return self.create_user(username, name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    username = models.CharField(max_length=150, unique=True)
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Country(models.Model):
    class Meta:
        verbose_name = 'کشور'
        verbose_name_plural = 'کشور ها'

    name = models.CharField(verbose_name='اسم',max_length=50)
    persian_name = models.CharField(max_length=60, verbose_name='اسم فارسی', blank=True, null=True)
    country_id = models.CharField(max_length=3, verbose_name='آیدی_کشور', blank=True, null=True)
    continent = models.CharField(max_length=13, verbose_name='قاره', blank=True, null=True)
    population = models.IntegerField(verbose_name='جمعیت', blank=True, null=True)

    def __str__(self):
        return self.name
