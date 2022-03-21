from django.shortcuts import render

# Create your views here.


def teleconsultation(request):
    return render(request, "telehealth/room.html")
