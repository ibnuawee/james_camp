from django import forms
from .models import AboutContent

class AboutContentForm(forms.ModelForm):
    class Meta:
        model = AboutContent
        fields = ['address', 'phone', 'email', 'heading', 'description', 'link_text', 'link_url']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }
