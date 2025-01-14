"""telemedecine URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

# from django.conf.urls import handler400, handler403, handler404, handler500

urlpatterns = [
    path("utawala/", admin.site.urls),
    path("", include("telemedecine.apps.authentication.urls")),
    path("administration/", include("telemedecine.apps.administration.urls")),
    path("api/", include("telemedecine.apps.api.urls")),
    path("telehealth/", include("telemedecine.apps.telehealth.urls"))
    # path("auth/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# handler404 = "telemedecine.apps.core.views.page_404_view"
