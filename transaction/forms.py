from django import forms
from .models import Transaction, PaymentMethod


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item', 'quantity', 'rent_date', 'return_date', 'identity_photo','payment_method', 'note', 'status']
        widgets = {
            'rent_date': forms.DateInput(attrs={'type': 'date'}),
            'return_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        item = self.cleaned_data.get('item')

        if not item:
            raise forms.ValidationError("Item tidak valid atau tidak ditemukan.")

        if self.instance.pk:
            original = Transaction.objects.get(pk=self.instance.pk)
            if original.status == 'pending' and self.cleaned_data.get('status') in ['paid', 'processing']:
                if quantity > item.stock:
                    raise forms.ValidationError(f"Stok tidak mencukupi. Hanya tersedia {item.stock}.")
        else:
            if quantity > item.stock:
                raise forms.ValidationError(f"Stok tidak mencukupi. Hanya tersedia {item.stock}.")

        return quantity

class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = ['name', 'description', 'is_active']
