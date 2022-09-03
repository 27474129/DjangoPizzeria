from django import forms
from .models import Orders



class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ["address", "apartment", "floor", "contactless"]
        widgets = {
            "apartment" : forms.NumberInput,
            "floor" : forms.NumberInput,
        }

