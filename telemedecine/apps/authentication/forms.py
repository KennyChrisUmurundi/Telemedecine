from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django.contrib.auth.forms import PasswordResetForm


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(
        label="",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Enter a mail connected to a Telemedecine Account",
                "type": "email",
                "name": "email",
            }
        ),
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "type": "text",
                "name": "email",
            }
        ),
        label="Email",
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "type": "password",
                "name": "password1",
            }
        ),
        label="Password",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "type": "password",
                "name": "password2",
            }
        ),
        label="Password (again)",
    )

    """added attributes so as to customise for styling, like bootstrap"""

    class Meta:
        model = CustomUser
        fields = ["email", "password1", "password2"]
        field_order = ["email", "password1", "password2"]

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if "password1" in self.cleaned_data and "password2" in self.cleaned_data:
            if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
                raise forms.ValidationError("Passwords don't match. Please try again!")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# The save(commit=False) tells Django to save the new record, but dont commit it to the database yet


class AuthenticationForm(forms.Form):  # Note: forms.Form NOT forms.ModelForm
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "type": "text",
                "name": "email",
                "placeholder": "Email",
            }
        ),
        label="Email",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "type": "password",
                "name": "password",
                "placeholder": "Password",
            }
        ),
        label="Password",
    )

    class Meta:
        fields = ["email", "password"]
