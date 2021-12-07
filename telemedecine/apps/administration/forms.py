from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from telemedecine.apps.core.models.hospital_models import Institution


class AddProviderForm(forms.Form):
    provider_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "provider_name",
            }
        ),
        label="Provider Name",
    )
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={"class": "form-control"})
    )
    state = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "state",
                "placeholder": "Input State",
            }
        ),
        label="State",
    )
    city = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "city",
                "placeholder": "Input city",
            }
        ),
        label="City",
    )
    specialization = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "specialization",
                "placeholder": "Provider Specialization",
            }
        ),
        label="Specialization",
        required=False,
    )
    admin_mail = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Admin email",
                "type": "email",
                "name": "email",
            }
        ),
    )

    # class Meta:
    #     model = Institution
