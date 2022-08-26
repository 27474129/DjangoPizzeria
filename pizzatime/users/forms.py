from django import forms
from .models import Users
from .validators import *


import argon2


class RegForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    password_repeat = forms.CharField(max_length=50, widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ["firstname", "secondname", "phone", "password"]
        widgets = {
            "password" : forms.PasswordInput,
            "phone" : forms.NumberInput,
        }

    def clean_firstname(self):
        firstname = self.cleaned_data["firstname"]
        validate_names(firstname, "firstname", self.add_error)
        return firstname

    def clean_secondname(self):
        secondname = self.cleaned_data["secondname"]
        validate_names(secondname, "secondname", self.add_error)
        return secondname

    def clean_phone(self):
        phone = self.cleaned_data[ "phone" ]
        validate_phone(phone, self.add_error)
        return phone


    def clean_password(self):
        password = self.cleaned_data[ "password" ]
        validate_password(password, self.add_error)
        password_hasher = argon2.PasswordHasher()
        password_hash = password_hasher.hash(password)
        return password_hash


class AuthForm(forms.Form):
    phone = forms.CharField(max_length=50, widget=forms.NumberInput)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)



