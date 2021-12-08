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
    path(
        "update_provider/<int:pk>",
        admin_views.UpdateProvider.as_view(),
        name="update_provider",
    ),
    path(
        "users-list/",
        admin_views.UserList.as_view(),
        name="users_list",
    ),
    path(
        "doctors/",
        admin_views.DoctorView.as_view(),
        name="doctors",
    ),
    path(
        "doctors/delete/<int:id>/",
        admin_views.delete_doctor,
        name="delete_doctor",
    ),
    path(
        "pharmacist/",
        admin_views.PharmacistView.as_view(),
        name="pharmacists",
    ),
    path(
        "pharmacist/delete/<int:id>/",
        admin_views.delete_pharmacist,
        name="delete_pharmacist",
    ),
]
