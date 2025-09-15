from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "report/",
        login_required(ReportDashboardsView.as_view(template_name="dashboard_report.html")),
        name="index",
    ),
    path(
        "speed_test/",
        login_required(ReportDashboardsView.as_view(template_name="speed_test.html")),
        name="speed_test",
    ),
    path(
        "tests/",
        login_required(TestTableView.as_view(template_name="tests.html")),
        name="tests_table",
    ),
    path(
        "test/<int:pk>/",
        login_required(TestDetailView.as_view(template_name="test_detail.html")),
        name="test_detail",
    ),
    path(
        "report/isp/",
        login_required(IspView.as_view(template_name="isp.html")),
        name="isp",
    ),
    path(
        "api/get_all_isp/",
        GetAllIspAPIView.as_view(),
        name="get_all_isp",
    )

]
