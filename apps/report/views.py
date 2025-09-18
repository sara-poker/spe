from django.views.generic import (TemplateView)
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Avg
from django.shortcuts import redirect

from web_project import TemplateLayout

from apps.test.models import SpeedTest, Isp
from apps.report.serializers import GetAllIspAPISerializer, PROVINCES_FA

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

        qs = (
            SpeedTest.objects
            .filter(network_info__province__isnull=False, speed_mbps__isnull=False)
            .values('network_info__province')
            .annotate(avg_speed=Avg('speed_mbps'))
        )

        def categorize(v):
            if v > 100:
                return 'very_fast'
            if v >= 50:
                return 'fast'
            if v >= 20:
                return 'middle'
            if v > 0:
                return 'slow'
            return 'no-data'

        province_data = {}
        for row in qs:
            prov = row['network_info__province']
            avg = row['avg_speed']
            if avg is None:
                continue
            avg = round(avg, 2)
            province_data[prov] = {'avg': avg, 'category': categorize(avg)}

        context['province_data'] = province_data

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


class ProvinceView(TemplateView):
    template_name = "province.html"

    def dispatch(self, request, *args, **kwargs):
        province = kwargs.get("pk")

        if province not in PROVINCES_FA:
            return redirect("/")

        speed_test = SpeedTest.objects.filter(network_info__province=province)
        if speed_test.count() == 0:
            return redirect("/")

        request._speed_test = speed_test

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        province = self.kwargs["pk"]
        speed_test = getattr(self.request, "_speed_test", {})

        speed_test_success = speed_test.filter(test_state=True)

        name = PROVINCES_FA.get(province, province)

        # دسته بندی اول: ISP
        data = []
        for isp_id, isp_name in (
            speed_test_success
                .values_list('network_info__isp', 'network_info__isp__name')
                .distinct()
        ):
            qs = speed_test_success.filter(network_info__isp=isp_id)
            total = qs.count()

            def speed_range(min_, max_):
                return qs.filter(speed_mbps__gte=min_, speed_mbps__lt=max_).count()

            subdata = [
                {"category": "خیلی سریع", "value": speed_range(75, 101)},
                {"category": "سریع", "value": speed_range(50, 75)},
                {"category": "متوسط", "value": speed_range(25, 50)},
                {"category": "کم سرعت", "value": speed_range(0, 25)},
            ]

            data.append({
                "category": isp_name or "نامشخص",  # اینجا نام واقعی ISP قرار می‌گیرد
                "value": total,
                "subData": subdata
            })

        context["province"] = name
        context["chart_data"] = data
        return context


class IspView(TemplateView):
    template_name = "isp.html"
    report_type = None

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        report_type = self.report_type
        print("report>>", report_type)

        isp = Isp.objects.filter(pk=self.kwargs['pk']).first()

        if report_type == 'standard':
            speed_test = SpeedTest.objects.filter(network_info__isp_id=self.kwargs['pk'])
        else:
            speed_test = SpeedTest.objects.filter(server_test__isp_id=self.kwargs['pk'])

        success_speed_test_list = speed_test.filter(test_state=True)
        success_speed_test = success_speed_test_list.count()
        fail_speed_test = speed_test.count() - success_speed_test

        success_speed_test_percent = round((success_speed_test * 100) / speed_test.count(), 2)
        fail_speed_test_percent = round((100 - success_speed_test_percent), 2)

        unique_ips = speed_test.values_list('network_info__ip', flat=True).distinct()

        unique_users_ids = speed_test.values_list('user', flat=True).distinct()
        User = get_user_model()
        unique_users = User.objects.filter(id__in=unique_users_ids)

        download_speed_test = success_speed_test_list.exclude(speed_mbps__isnull=True).values_list('speed_mbps',
                                                                                                   flat=True).distinct()
        upload_speed_test = success_speed_test_list.exclude(upload_speed_mbps__isnull=True).values_list(
            'upload_speed_mbps', flat=True).distinct()
        ping_speed_test = success_speed_test_list.exclude(ping_avg__isnull=True).values_list('ping_avg',
                                                                                             flat=True).distinct()
        jitter_speed_test = success_speed_test_list.exclude(jitter__isnull=True).values_list('jitter',
                                                                                             flat=True).distinct()

        context['isp'] = isp

        context['report_type'] = report_type

        context['test_count'] = speed_test.count()
        context['success_speed_test'] = success_speed_test
        context['fail_speed_test'] = fail_speed_test
        context['success_speed_test_percent'] = success_speed_test_percent
        context['fail_speed_test_percent'] = fail_speed_test_percent

        if download_speed_test:
            context['max_download_speed'] = max(download_speed_test)
            context['min_download_speed'] = min(download_speed_test)
            context['avg_download_speed'] = round((sum(download_speed_test) / len(download_speed_test)), 1)
        else:
            context['max_download_speed'] = 0
            context['min_download_speed'] = 0
            context['avg_download_speed'] = 0

        if upload_speed_test:
            context['max_upload_speed'] = max(upload_speed_test)
            context['min_upload_speed'] = min(upload_speed_test)
            context['avg_upload_speed'] = round((sum(upload_speed_test) / len(upload_speed_test)), 2)
        else:
            context['max_upload_speed'] = 0
            context['min_upload_speed'] = 0
            context['avg_upload_speed'] = 0

        if ping_speed_test:
            context['max_ping_speed'] = max(ping_speed_test)
            context['min_ping_speed'] = min(ping_speed_test)
            context['avg_ping_speed'] = round((sum(ping_speed_test) / len(ping_speed_test)), 2)
        else:
            context['max_ping_speed'] = 0
            context['min_ping_speed'] = 0
            context['avg_ping_speed'] = 0

        if jitter_speed_test:
            context['max_jitter_speed'] = max(jitter_speed_test)
            context['min_jitter_speed'] = min(jitter_speed_test)
            context['avg_jitter_speed'] = round((sum(jitter_speed_test) / len(jitter_speed_test)), 2)
        else:
            context['max_jitter_speed'] = 0
            context['min_jitter_speed'] = 0
            context['avg_jitter_speed'] = 0

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
        ).filter(has_test=True).order_by('id')

        serializer = GetAllIspAPISerializer(isp, many=True)
        return Response(serializer.data)


class GetAllIspServerTestAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        isp_with_test = SpeedTest.objects.filter(
            server_test__isp=OuterRef('pk')
        )

        isp = Isp.objects.annotate(
            has_test=Exists(isp_with_test)
        ).filter(has_test=True).order_by('id')

        serializer = GetAllIspAPISerializer(isp, many=True)
        return Response(serializer.data)
