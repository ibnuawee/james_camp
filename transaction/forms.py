from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item', 'quantity', 'status']

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        item = self.cleaned_data['item']
        if quantity > item.stock:
            raise forms.ValidationError(f"Stok tidak mencukupi. Hanya tersedia {item.stock}.")
        return quantity
