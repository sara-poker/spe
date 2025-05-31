from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "report",
        login_required(ReportDashboardsView.as_view(template_name="dashboard_report.html")),
        name="index",
    )

]
