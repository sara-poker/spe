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
        login_required(TestTable.as_view(template_name="tests.html")),
        name="tests_table",
    ),
    path(
        "test/<int:pk>/",
        login_required(TestDetail.as_view(template_name="test_detail.html")),
        name="test_detail",
    )

]
