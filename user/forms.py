from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Konfirmasi Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'is_active']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            self.add_error('password_confirmation', "Password dan konfirmasi password tidak cocok.")

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'is_active']
