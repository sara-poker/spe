from django.views.generic import (TemplateView)
from django.db.models import Exists, OuterRef
from django.contrib.auth import get_user_model

from web_project import TemplateLayout

from apps.test.models import SpeedTest, Isp
from apps.report.serializers import GetAllIspAPISerializer

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


def convert_date(date):
    date = date.replace(" ", "")
    year = date[:4]
    month = date[5:7]
    day = date[8:10]
    return year + month + day


def convert_date2(date):
    date = str(date)
    year = date[:4]
    month = date[4:6]
    day = date[6:8]
    return year + "/" + month + "/" + day


def filter_date(date, queryset):
    selected_date_str = date.split("تا")
    if len(selected_date_str) == 2:
        start_date = convert_date(selected_date_str[0])
        end_date = convert_date(selected_date_str[1])
    else:
        start_date = convert_date(selected_date_str[0])
        end_date = start_date

    return queryset.filter(date__range=(start_date, end_date)).order_by('date')


def filter_date_year(date, queryset):
    date = int(date)
    if date == 0:
        return queryset
    start_date = date
    end_date = start_date + 10000

    return queryset.filter(date__gte=start_date, date__lte=end_date).order_by('date')


def filter_vpn(vpn, queryset):
    if vpn == "0":
        return queryset
    return queryset.filter(vpn_id=vpn)


def filter_country_server(country_server, queryset):
    if country_server == "0":
        return queryset
    return queryset.filter(server_country=country_server)


def filter_province(province, queryset):
    return queryset.filter(city=province)


def filter_country(country, queryset):
    if country == "0":
        return queryset
    return queryset.filter(vpn__vpn_country=country)


def filter_operator(oprator, queryset):
    return queryset.filter(oprator__in=oprator)


# Create your views here.
class ReportDashboardsView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        context.update({
            "msg": "سلام"
        })

        return context


class TestTableView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        tests = SpeedTest.objects.all().order_by('-id')

        context['tests'] = tests
        return context


class TestDetailView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        test = SpeedTest.objects.get(pk=self.kwargs['pk'])

        context['test'] = test
        context["speed_MBps"] = test.speed_mbps / 8
        context["upload_speed_MBps"] = test.upload_speed_mbps / 8
        return context


class IspView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        isp = Isp.objects.filter(pk=self.kwargs['pk']).first()
        speed_test = SpeedTest.objects.filter(network_info__isp_id=self.kwargs['pk'])
        success_speed_test = speed_test.filter(test_state=True).count()
        fail_speed_test = speed_test.count() - success_speed_test

        success_speed_test_percent = round((success_speed_test * 100) / speed_test.count(), 2)
        fail_speed_test_percent = 100 - success_speed_test_percent

        unique_ips = speed_test.values_list('network_info__ip', flat=True).distinct()

        unique_users_ids = speed_test.values_list('user', flat=True).distinct()
        User = get_user_model()
        unique_users = User.objects.filter(id__in=unique_users_ids)

        context['isp'] = isp

        context['test_count'] = speed_test.count()
        context['success_speed_test'] = success_speed_test
        context['fail_speed_test'] = fail_speed_test
        context['success_speed_test_percent'] = success_speed_test_percent
        context['fail_speed_test_percent'] = fail_speed_test_percent

        context['ips_count'] = unique_ips.count()
        context['unique_ips'] = list(unique_ips)

        context['users_count'] = unique_users.count()
        context['unique_users'] = list(unique_users)

        return context


class GetAllIspAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        isp_with_test = SpeedTest.objects.filter(
            network_info__isp=OuterRef('pk')
        )

        isp = Isp.objects.annotate(
            has_test=Exists(isp_with_test)
        ).filter(has_test=True)

        serializer = GetAllIspAPISerializer(isp, many=True)
        return Response(serializer.data)
