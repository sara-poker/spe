from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path(
        "setup/profile",
        login_required(ProfileView.as_view(template_name="profile.html")),
        name="profile",
    ),
    path(
        "setup/server_test",
        login_required(ServerTestView.as_view(template_name="server_test.html")),
        name="serverTest",
    ),
    path(
        "api/get_all_server_test",
        GetAllServerTest.as_view(),
        name="get_all_server_test",
    ),
    path(
        "api/add_record",
        AddRecord.as_view(),
        name="add_record",
    ),
    path(
        "setup/users/table",
        login_required(UsersTable.as_view(template_name="users_table.html")),
        name="usersTable",
    ),
    path(
        "setup/user/detail/<int:pk>/",
        login_required(UserDetail.as_view(template_name="user_detail.html")),
        name="usersDetail",
    )
]
