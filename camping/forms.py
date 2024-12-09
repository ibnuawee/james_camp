from django import forms
from .models import Category, CampingItem

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class CampingItemForm(forms.ModelForm):
    class Meta:
        model = CampingItem
        fields = ['name', 'category', 'description', 'price', 'stock']
