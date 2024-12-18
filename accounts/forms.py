from django import forms
import re
from django.contrib.auth.models import User
from jsonschema import ValidationError
from .models import Profile


class RegistrationForm(forms.Form):
    username = forms.CharField(label="User name", max_length=30)
    email = forms.EmailField(label="Email")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Comfirm password", widget=forms.PasswordInput())

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not re.match(r"^[\w]+$", username):
            raise ValidationError("User name contains special characters")
        if User.objects.filter(username=username).exists():
            raise ValidationError("User already exists")
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password1"],
        )
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone_number", "address", "profile_picture"]
