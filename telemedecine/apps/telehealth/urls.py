from django.urls import path, include
from .views import teleconsultation


app_name = "telehealth"
urlpatterns = [path("", teleconsultation, name="video_call")]
