from django import forms
from transaction.models import Transaction, PaymentMethod


class UserTransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['quantity', 'rent_date', 'return_date', 'identity_photo','payment_method', 'note']
        widgets = {
            'rent_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item', None)
        super(UserTransactionForm, self).__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']

        if not self.item:
            raise forms.ValidationError("Item tidak valid atau tidak ditemukan.")
        if quantity > self.item.stock:
            raise forms.ValidationError(f"Stok tidak mencukupi. Hanya tersedia {self.item.stock}.")
        return quantity

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name', 'description', 'is_active']
