from django.conf import settings
import json

from web_project.template_helpers.theme import TemplateHelper

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
                    "url": "isp",
                    "name": "اپراتور ها",
                    "slug": "isp",
                    "pk": True
                },
                {
                    "url": "isp_server_test",
                    "name": "اپراتور سرور های تست",
                    "slug": "isp_server_test",
                    "pk": True
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
