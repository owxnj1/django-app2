from django import forms
from .models import Registration

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea, required=True)

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['module']  
        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
        }