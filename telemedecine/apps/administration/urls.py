from django.urls import path
from . import views as admin_views


app_name = "administration"
urlpatterns = [
    path(
        "test/call",
        admin_views.TestCall.as_view(),
        name="test_call",
    ),
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
    ######## LABORATORY
    path(
        "lab_specialist/",
        admin_views.LaboratoryView.as_view(),
        name="lab",
    ),
    path(
        "lab_specialist/delete/<int:id>/",
        admin_views.delete_laboratorist,
        name="delete_laboratorist",
    ),
    ######## USERS
    path(
        "system_users/",
        admin_views.SystemUser.as_view(),
        name="system_users",
    ),
    ######## RECEPTIONIST
    path(
        "receptionist/",
        admin_views.ReceptionistView.as_view(),
        name="receptionist",
    ),
    path(
        "receptionist/delete/<int:id>/",
        admin_views.delete_laboratorist,
        name="receptionist_delete",
    ),
    ######## NURSE
    path(
        "nurse/",
        admin_views.NurseView.as_view(),
        name="nurse",
    ),
    path(
        "nurse/delete/<int:id>/",
        admin_views.delete_nurse,
        name="delete_nurse",
    ),
    ######## PATIENTS
    path(
        "patient/",
        admin_views.PatientView.as_view(),
        name="patient",
    ),
]
