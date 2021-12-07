from django.urls import path
from . import views as admin_views


app_name = "administration"
urlpatterns = [
    path("dashboard/", admin_views.dashboard, name="dashboard"),
    path("providers/", admin_views.Providers.as_view(), name="providers"),
    path(
        "providers/delete/<int:id>/",
        admin_views.delete_provider,
        name="delete_provider",
    ),
]
