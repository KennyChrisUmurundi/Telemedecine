from rest_framework import serializers


class ProviderRegistrationSerializer(serializers.Serializer):
    provider_name = serializers.CharField()
    country = serializers.CharField()
    state = serializers.CharField()
    city = serializers.CharField()
    specialization = serializers.CharField(
        required=False, allow_null=True, allow_blank=True
    )
    email_1 = serializers.CharField()
    email_2 = serializers.CharField()
