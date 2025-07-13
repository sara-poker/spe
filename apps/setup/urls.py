from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "setup/server_test",
        login_required(ServerTestView.as_view(template_name="server_test.html")),
        name="serverTest",
    )
]
