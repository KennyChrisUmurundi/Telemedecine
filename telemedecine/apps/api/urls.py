from django.urls import path
from .views import ProviderRegistrationAPIView

urlpatterns = [path("provider/register", ProviderRegistrationAPIView.as_view())]
