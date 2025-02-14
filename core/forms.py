from django import forms
from .models import CustomCategory

class CustomCategoryForm(forms.ModelForm):
    class Meta:
        model = CustomCategory
        fields = ['name', 'keywords']
