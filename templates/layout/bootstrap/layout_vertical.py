from django.conf import settings
from django.core.cache import cache
from django.db.models import Exists, OuterRef

from apps.test.models import SpeedTest, Isp
from apps.report.serializers import PROVINCES_FA

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
    pk = cache.get("isp_server_pk")
    if pk is not None:
        return pk

    resp = SpeedTest.objects.filter(server_test__isp=OuterRef('pk'))

    isp_qs = Isp.objects.annotate(
        has_test=Exists(resp)
    ).filter(has_test=True).order_by('id')

    pk = isp_qs[0].id if isp_qs.exists() else None
    print(">", pk)

    cache.set("isp_server_pk", pk, 60 * 60 * 24)
    return pk


def build_province():
    cache_key = "province_submenu"
    submenu = cache.get(cache_key)
    if submenu is not None:
        return submenu

    qs = (
        SpeedTest.objects
        .filter(network_info__province__isnull=False, speed_mbps__isnull=False)
        .values('network_info__province')
        .distinct()
    )

    submenu = []
    for row in qs:
        province_en = row["network_info__province"]
        province_fa = PROVINCES_FA.get(province_en, province_en)

        submenu.append({
            "url": f"/report/province/{province_en}/",
            "external": True,
            "name": province_fa,
            "slug": "provinces"
        })

    cache.set(cache_key, submenu, 60 * 60 * 24)  # کش برای ۲۴ ساعت
    return submenu


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
            "name": "استان ها",
            "icon": "menu-icon tf-icons ti ti-map",
            "slug": "province",
            "submenu": build_province()
        },
        {
            "name": "اپراتور ها",
            "icon": "menu-icon tf-icons ti ti-building-broadcast-tower",
            "slug": "setting",
            "submenu": [
                {
                    "url": "isp",
                    "name": "اپراتور های تست",
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
