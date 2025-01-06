from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
#from itreporting.models import Course

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email address', help_text='Your SHU email address.')
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=True)
    address = forms.CharField(max_length=255, required=True)
    city = forms.CharField(max_length=100, required=True)
    country = forms.CharField(max_length=100, required=True)


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Populate the Profile fields
            user.profile.date_of_birth = self.cleaned_data['date_of_birth']
            user.profile.address = self.cleaned_data['address']
            user.profile.city = self.cleaned_data['city']
            user.profile.country = self.cleaned_data['country']
            user.profile.save()  # Save the updated profile
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100, required=False)
    country = forms.CharField(max_length=100, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['image', 'date_of_birth', 'address', 'city', 'country']
