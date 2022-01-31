import logging
import uuid

from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from telemedecine.apps.core.models.hospital_models import Institution
from .serializers import ProviderRegistrationSerializer
from django.core.mail import send_mail

from telemedecine.apps.authentication.models import CustomUser
from telemedecine.apps.core.models.administration import Role


logger = logging.getLogger(__name__)


class ProviderRegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ProviderRegistrationSerializer

    def post(self, request):
        return_data = {}
        request_data = self.request.data
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)

        provider_name = serializer.validated_data.get("provider_name")
        country = serializer.validated_data.get("country")
        state = serializer.validated_data.get("state")
        city = serializer.validated_data.get("city")
        specialization = serializer.validated_data.get("specialization")
        admin_mail = serializer.validated_data.get("email_1")
        admin_mail_confirm = serializer.validated_data.get("email_2")
        print("THE EMAILLL:%s" % admin_mail)
        if not admin_mail == admin_mail_confirm:
            print("same email")
            return_data["responseMessage"] = _("The Two Email do not match")
            return_data["success"] = False
            return Response(return_data, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin_mail_existing = Institution.objects.get(
                default_admin__email=admin_mail
            )
            return_data["responseMessage"] = _(
                "This email is already connected to an institution"
            )
            return_data["success"] = False
            return Response(return_data, status=status.HTTP_400_BAD_REQUEST)
        except Institution.DoesNotExist:
            pass
        temp_password = uuid.uuid4().hex[:6].upper()
        try:
            admin_user = CustomUser.objects.create_user(admin_mail, temp_password)
            admin_user.save()
        except BaseException:
            admin_user = CustomUser.objects.get(email=admin_mail)
        try:
            send_mail(
                "Telemedecine User Creation",
                "Hi "
                + admin_user.email
                + " Your Generated Password is "
                + temp_password
                + " Please change it and create your own",
                " telemedecine@gmail.com",
                [admin_mail],
                fail_silently=False,
            )
        except BaseException:
            pass
        provider = Institution.objects.create(
            institution_name=provider_name,
            country=country,
            state=state,
            city=city,
            default_admin=admin_user,
        )
        if specialization:
            provider.specialization = specialization

        provider.save()
        try:
            role = Role.objects.get(
                user=admin_user,
                institution=provider,
                role=Role.ADMIN,
            )
        except Role.DoesNotExist:
            role = Role.objects.create(
                user=admin_user,
                institution=provider,
                role=Role.ADMIN,
            )
            role.save()
        return_data["responseMessage"] = _("Provider Created successfully")
        return_data["success"] = True
        print(return_data)
        return Response(return_data, status=status.HTTP_200_OK)
