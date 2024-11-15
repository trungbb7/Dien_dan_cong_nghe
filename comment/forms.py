from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter tags separated by commas",
            }
        ),
    )

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "tags",
        ]
