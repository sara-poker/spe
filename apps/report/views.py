from django.views.generic import (TemplateView)
from web_project import TemplateLayout

from apps.test.models import SpeedTest

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
            "msg":"سلام"
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

        test = Test.objects.exclude(server_isp=None)  # فیلتر اولیه برای حذف مقادیر null
        vpn = Vpn.objects.all()

        country_server_ids = test.values_list('server_country', flat=True).distinct()
        country_ids = vpn.values_list('vpn_country', flat=True).distinct()

        country_server_ids = [item for item in country_server_ids if item != 'nan']
        country_ids = [item for item in country_ids if item != 'nan']

        country_server = Country.objects.filter(id__in=country_server_ids).order_by('persian_name')
        country = Country.objects.filter(id__in=country_ids).order_by('persian_name')

        selected_date_str = self.request.GET.get('selected_date')
        selected_vpn = self.request.GET.get('vpn')
        selected_country_server = self.request.GET.get('server_country')
        selected_country = self.request.GET.get('country')

        if selected_date_str:
            test = filter_date_year(selected_date_str, test)

        if selected_vpn:
            test = filter_vpn(selected_vpn, test)

        if selected_country_server:
            test = filter_country_server(selected_country_server, test)

        if selected_country:
            test = filter_country(selected_country, test)

        main_isp = Isp.objects.filter(pk=self.kwargs['pk']).first()
        if main_isp:
            main_isp.name2 = main_isp.name.replace(" ", "")

        test_data = test.values('server_isp', 'server_country__name').annotate(server_count=Count('id')).exclude(
            server_isp='nan')

        data = {}
        for item in test_data:
            isp = item['server_isp']
            country_m = item['server_country__name']
            count = item['server_count']

            if isp not in data:
                data[isp] = {}
            data[isp][country_m] = count

        test = test.filter(server_isp=main_isp.name)

        isp_ip = test.values('server_ip').distinct()
        isp_country = test.values('server_country__persian_name').distinct()
        isp_vpn = test.values('vpn__name').distinct()

        count_ip = isp_ip.count()
        count_country = isp_country.count()
        count_vpn = isp_vpn.count()

        context.update({
            'vpn': vpn,
            'country_server': country_server,
            'country': country,
            'data': data,
            'isp': main_isp,
            'isp_ip': isp_ip,
            'isp_vpn': isp_vpn,
            'isp_country': isp_country,
            'count_ip': count_ip,
            'count_country': count_country,
            'count_vpn': count_vpn,
            'selected_date': selected_date_str,
            'selected_country_server': selected_country_server,
            'selected_vpn': selected_vpn,
            'selected_country': selected_country,
        })

        return context
