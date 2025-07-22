from django.views.generic import (TemplateView)
from web_project import TemplateLayout
from apps.setup.models import Country
from apps.test.models import Isp, ServerTest
from django.shortcuts import redirect

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.setup.serializers import ServerTestSerializer
from rest_framework.response import Response

import re


class ProfileView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        user = self.request.user

        context['user'] = user

        return context

# Create your views here.
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
