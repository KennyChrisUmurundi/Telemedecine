from django.urls import path
from . import views as auth_views
from django.contrib.auth import views as authy_views
from .forms import UserPasswordResetForm

urlpatterns = [
    path("", auth_views.login, name="login"),
    path("auth/logout", auth_views.logout, name="logout"),
    path(
        "auth/password_reset",
        authy_views.PasswordResetView.as_view(form_class=UserPasswordResetForm),
        name="password_reset",
    ),
    path(
        "auth/password_reset_done",
        authy_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "auth/password_reset_confirm/<uidb64>/<token>",
        authy_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "auth/password_reset_complete",
        authy_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    )
    # path("admin_auth/", auth_views.admin_login, name="admin_login"),
]
