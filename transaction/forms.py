from django import forms
from .models import Transaction, PaymentMethod


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item', 'quantity', 'status', 'rent_date', 'return_date', 'identity_photo','payment_method', 'note']
        widgets = {
            'rent_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        item = self.cleaned_data['item']
        if quantity > item.stock:
            raise forms.ValidationError(f"Stok tidak mencukupi. Hanya tersedia {item.stock}.")
        return quantity

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name', 'description', 'is_active']
