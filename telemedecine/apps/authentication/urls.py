from django.urls import path
from . import views as auth_views

urlpatterns = [
    path("login/", auth_views.login, name="login"),
    # path("admin_auth/", auth_views.admin_login, name="admin_login"),
]
