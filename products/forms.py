from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """Form used by staff to create and update products."""

    class Meta:
        model = Product
        fields = "__all__"