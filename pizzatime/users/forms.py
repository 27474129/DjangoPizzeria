from django import forms
from users.models import Users
from users.validation import *

import argon2



class RegForm(forms.ModelForm):
    password_repeat = forms.CharField(max_length=50, widget=forms.PasswordInput)
    class Meta:
        model = Users
        fields = ["firstname", "secondname", "phone", "password"]
        widgets = {
            "password" : forms.PasswordInput,
            "phone" : forms.NumberInput,
        }


class AuthForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ["phone", "password"]
        widgets = {
            "password" : forms.PasswordInput,
            "phone" : forms.NumberInput,
        }



class ConfirmPhoneForm(forms.Form):
    confirmation_code = forms.IntegerField()

