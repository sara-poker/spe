from django.views.generic import (TemplateView)
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from web_project import TemplateLayout

from apps.setup.models import Country , CustomUser
from apps.test.models import Isp, ServerTest, SpeedTest, DeviceInfo, NetworkInfo
from apps.setup.serializers import ServerTestSerializer

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

import re

class ProfileView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        speed_test_qs = SpeedTest.objects.filter(user=self.request.user).select_related('device_info', 'network_info')

        # تعداد موفق و ناموفق
        success_count = speed_test_qs.filter(test_state='success').count()
        fail_count = speed_test_qs.filter(test_state='fail').count()

        # استخراج یونیک دستگاه‌ها
        unique_devices = set(speed_test_qs.values_list('device_info', flat=True))
        device_info_list = DeviceInfo.objects.filter(id__in=unique_devices)

        # استخراج یونیک شبکه‌ها
        unique_networks = set(speed_test_qs.values_list('network_info', flat=True))
        network_info_list = NetworkInfo.objects.filter(id__in=unique_networks)

        # اضافه به context
        context['success_count'] = success_count
        context['fail_count'] = fail_count
        context['device_info_list'] = device_info_list
        context['network_info_list'] = network_info_list

        return context

class UserDetail(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        User = get_user_model()
        user = User.objects.filter(id=self.kwargs['pk'])

        speed_test_qs = SpeedTest.objects.filter(user=self.kwargs['pk']).select_related('device_info', 'network_info')

        # تعداد موفق و ناموفق
        success_count = speed_test_qs.filter(test_state='success').count()
        fail_count = speed_test_qs.filter(test_state='fail').count()

        # استخراج یونیک دستگاه‌ها
        unique_devices = set(speed_test_qs.values_list('device_info', flat=True))
        device_info_list = DeviceInfo.objects.filter(id__in=unique_devices)

        # استخراج یونیک شبکه‌ها
        unique_networks = set(speed_test_qs.values_list('network_info', flat=True))
        network_info_list = NetworkInfo.objects.filter(id__in=unique_networks)

        # اضافه به context
        context['user'] = user[0]
        context['success_count'] = success_count
        context['fail_count'] = fail_count
        context['device_info_list'] = device_info_list
        context['network_info_list'] = network_info_list

        return context

class UsersTable(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        User = get_user_model()
        users = User.objects.exclude(id=self.request.user.id)

        context['users'] = users
        return context

class ServerTestView(TemplateView):

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        servers = ServerTest.objects.all()
        country = Country.objects.all().order_by('persian_name')
        isp = Isp.objects.all().order_by('name')

        context['servers'] = servers
        context['country'] = country
        context['isp'] = isp
        context['class_notification'] = self.request.GET.get('alert_class', 'none_alert_mo')
        context['message'] = self.request.GET.get('message', '')

        return context

    def post(self, request, *args, **kwargs):
        # حذف سرور (اگر فرم حذف ارسال شده باشه)
        if 'delete_server_id' in request.POST:
            server_id = request.POST.get('delete_server_id')
            ServerTest.objects.filter(id=server_id).delete()
            return redirect(f"{request.path}?alert_class=success_alert_mo&message=سرور با موفقیت حذف شد")

        # اضافه کردن سرور جدید
        name = request.POST.get('server_name', '').strip()
        url = request.POST.get('ip', '').strip()
        country_id = request.POST.get('country_server')
        isp_id = request.POST.get('isp_server')

        if not name or not url or country_id == "0" or isp_id == "0":
            return redirect(f"{request.path}?alert_class=err_alert_mo&message=لطفاً همه فیلدها را پر کنید")

        if ServerTest.objects.filter(name=name).exists():
            return redirect(f"{request.path}?alert_class=err_alert_mo&message=نام سرور تکراری است")

        if ServerTest.objects.filter(url=url).exists():
            return redirect(f"{request.path}?alert_class=err_alert_mo&message=آدرس IP تکراری است")

        ip_regex = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}$'
        if not re.fullmatch(ip_regex, url):
            return redirect(f"{request.path}?alert_class=err_alert_mo&message=آی‌پی وارد شده معتبر نیست")

        ServerTest.objects.create(
            name=name,
            url=url,
            country_id=country_id,
            isp_id=isp_id
        )

        return redirect(f"{request.path}?alert_class=success_alert_mo&message=سرور با موفقیت ثبت شد")

class GetAllIsp(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        server_test = ServerTest.objects.all().order_by("name")

        serializer = ServerTestSerializer(server_test, many=True)
        return Response(serializer.data)
