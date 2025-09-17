from django.conf import settings
from django.core.cache import cache
from django.db.models import Exists, OuterRef

from apps.test.models import SpeedTest, Isp

import json
import requests

from web_project.template_helpers.theme import TemplateHelper

API_BASE = settings.BASE_URL


def get_isp_pk():
    pk = cache.get("isp_pk")
    if pk is not None:
        return pk

    resp = SpeedTest.objects.filter(network_info__isp=OuterRef('pk'))

    isp_qs = Isp.objects.annotate(
        has_test=Exists(resp)
    ).filter(has_test=True).order_by('id')

    # data[0] الان یک شیء Isp است، پس با attribute دسترسی بده
    pk = isp_qs[0].id if isp_qs.exists() else None
    print(">", pk)

    cache.set("isp_pk", pk, 60 * 60 * 24)  # کش ۲ ساعته
    return pk


def get_isp_server_test_pk():
    resp = SpeedTest.objects.filter(server_test__isp=OuterRef('pk'))

    isp_qs = Isp.objects.annotate(
        has_test=Exists(resp)
    ).filter(has_test=True).order_by('id')

    pk = isp_qs[0].id if isp_qs.exists() else None
    print(">", pk)

    cache.set("isp_server_pk", pk, 60 * 60 * 24)
    return pk


menu_file = {
    "menu": [
        {
            "name": "پیشخوان",
            "icon": "menu-icon tf-icons ti ti-layout-dashboard",
            "slug": "dashboard",
            "submenu": [
                {
                    "url": "index",
                    "name": "نمای کلی",
                    "slug": "dashboard-analytics"
                }
            ]
        },
        {
            "name": "تست سرعت",
            "icon": "menu-icon tf-icons ti ti-gauge",
            "slug": "dashboard",
            "submenu": [
                {
                    "url": "speed_test",
                    "name": "تست سرعت",
                    "slug": "speed_test"
                },
                {
                    "url": "tests_table",
                    "name": "لیست تست ها",
                    "slug": "tests_table",
                }
            ]
        },
        {
            "name": "گزارشات",
            "icon": "menu-icon tf-icons ti ti-report-analytics",
            "slug": "setting",
            "submenu": [
                {
                    "url": "province",
                    "name": "استان ها",
                    "slug": "province",
                    "pk": "Tehran"
                },
                {
                    "url": "isp",
                    "name": "اپراتور ها",
                    "slug": "isp",
                    "pk": get_isp_pk()
                },
                {
                    "url": "isp_server_test",
                    "name": "اپراتور سرور های تست",
                    "slug": "isp_server_test",
                    "pk": get_isp_server_test_pk()
                }

            ]
        },
        {
            "name": "تنظیمات",
            "icon": "menu-icon tf-icons ti ti-settings",
            "slug": "setting",
            "submenu": [
                {
                    "url": "profile",
                    "name": "پروفایل",
                    "slug": "profile",
                },
                {
                    "url": "usersTable",
                    "name": "جدول کاربران",
                    "slug": "users_table"
                },
                {
                    "url": "serverTest",
                    "name": "مدیریت سرور های تست",
                    "slug": "server-test"
                },
            ]
        },
        {
            "name": "پشتیبانی",
            "icon": "menu-icon tf-icons ti ti-help",
            "slug": "support",
            "submenu": [
                {
                    "url": "support",
                    "name": "ارسال تیکت",
                    "slug": "support"
                },
                {
                    "url": "notification",
                    "name": "اعلان ها",
                    "slug": "notification"
                }
            ]
        }
    ]
}

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in web_project/__init__.py
"""


class TemplateBootstrapLayoutVertical:
    def init(context):
        context.update(
            {
                "layout": "vertical",
                "content_navbar": True,
                "is_navbar": True,
                "is_menu": True,
                "is_footer": True,
                "navbar_detached": True,
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)

        TemplateBootstrapLayoutVertical.init_menu_data(context)

        return context

    def init_menu_data(context):
        # Load the menu data from the JSON
        menu_data = menu_file

        # Updated context with menu_data
        context.update({"menu_data": menu_data})
