from django import forms
from .models import Order


class CheckOutForm(forms.ModelForm):
    """creating the checkout form"""

    class Meta:
        model = Order
        fields = ['customer_name', 'email', 'phone']
