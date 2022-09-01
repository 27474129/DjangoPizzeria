from django import forms
from .models import Orders



class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = [
            "is_need_delivery", "address", "apartment",
            "floor", "contactless"
        ]
