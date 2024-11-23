from django import forms
import re
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(forms.Form):
    username = forms.CharField(label='User name', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Comfirm password', widget=forms.PasswordInput())
def clean_password2(self):
    if 'password1' in self.cleaned_data:
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 == password2 and password1:
            return password2
    raise forms.ValidationError("Invalid Password")
def clean_username(self):
    username = self.cleaned_data['username']
    if not re.search(r'^\w+&', username):
        raise forms.ValidationError("User name has special characters")
    try:
        User.objects.get(username=username)
    except User.DoesNotExist:
        return username
    raise forms.ValidationError("User already exists")
def save(self):
    User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'],
password=self.cleaned_data['password1'])

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'profile_picture']

