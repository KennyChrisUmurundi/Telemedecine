from django.urls import path
from . import views as admin_views


app_name = "administration"
urlpatterns = [path("dashboard/", admin_views.dashboard, name="dashboard")]
