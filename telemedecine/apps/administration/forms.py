from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from telemedecine.apps.core.models.hospital_models import (
    Institution,
    Doctor,
    Speciality,
)

GENDER = (("M", "Male"), ("F", "Female"))


# def get_doctor_speciality():
#     categories = []
#     s = Speciality.objects.all().values()
#     for sp in s:
#         special = sp["speciality"]
#         categories.append(special)
#     return categories


# DOCTOR_SPECIALITY = get_doctor_speciality()


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


class UpdateProviderForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = "__all__"
        widgets = {
            "class": "form-control",
        }


class AddDoctorForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
            }
        ),
        label="First Name",
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
            }
        ),
        label="Last Name",
    )
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter doctor's email",
                "type": "email",
                "name": "email",
            }
        ),
    )
    gender = forms.ChoiceField(
        choices=GENDER,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Gender",
            }
        ),
    )
    publication = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "publications",
            }
        ),
        label="Last Name",
        required=False,
    )
    licence_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "licence_number",
            }
        ),
        label="licence_number",
        required=False,
    )
    # speciality = forms.ChoiceField(
    #     choices=[
    #         (choice.speciality, choice) for choice in Speciality.objects.all()
    #     ],
    #     widget=forms.Select(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Category",
    #         }
    #     ),
    # )

    # class Meta:
    #     model = Doctor
    #     fields = "__all__"
    #     # widgets = {"class": "form-control"}


class AddPharmacistForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
            }
        ),
        label="First Name",
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
            }
        ),
        label="Last Name",
    )
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter pharmacist's email",
                "type": "email",
                "name": "email",
            }
        ),
    )
    gender = forms.ChoiceField(
        choices=GENDER,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Type",
            }
        ),
    )
    # publication = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "type": "text",
    #             "name": "publications",
    #         }
    #     ),
    #     label="Last Name",
    #     required=False,
    # )
    licence_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "licence_number",
            }
        ),
        label="licence_number",
        required=False,
    )


class AddLabForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
            }
        ),
        label="First Name",
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
            }
        ),
        label="Last Name",
    )
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter email",
                "type": "email",
                "name": "email",
            }
        ),
    )
    gender = forms.ChoiceField(
        choices=GENDER,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Type",
            }
        ),
    )
    # publication = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "type": "text",
    #             "name": "publications",
    #         }
    #     ),
    #     label="Last Name",
    #     required=False,
    # )
    licence_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "licence_number",
            }
        ),
        label="licence_number",
        required=False,
    )


class AddReceptionistForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
            }
        ),
        label="First Name",
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
            }
        ),
        label="Last Name",
    )
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter receptionist's email",
                "type": "email",
                "name": "email",
            }
        ),
    )
    gender = forms.ChoiceField(
        choices=GENDER,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Type",
            }
        ),
    )


class AddNurseForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
            }
        ),
        label="First Name",
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
            }
        ),
        label="Last Name",
    )
    country = CountryField().formfield(
        widget=CountrySelectWidget(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter receptionist's email",
                "type": "email",
                "name": "email",
            }
        ),
    )
    gender = forms.ChoiceField(
        choices=GENDER,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Type",
            }
        ),
    )
    is_practitioner = forms.BooleanField()


class AddPatientForm(forms.Form):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "first_name",
            }
        ),
        label="First Name",
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "last_name",
            }
        ),
        label="Last Name",
    )
    # country = CountryField().formfield(
    #     widget=CountrySelectWidget(
    #         attrs={"class": "form-control"},
    #     ),
    #     required=False,
    # )
    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter patient's email",
                "type": "email",
                "name": "email",
            }
        ),
        required=False,
    )
    age = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "Age",
            }
        ),
        label="Phone Number",
    )

    gender = forms.ChoiceField(
        choices=GENDER,
        widget=forms.Select(
            attrs={
                "class": "form-control",
                "placeholder": "Gender",
            }
        ),
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "phone_number",
            }
        ),
        label="Phone Number",
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
                "name": "address",
            }
        ),
        label="Address",
    )
