from .models import Sale
from django import forms

class ProductForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ('count',)