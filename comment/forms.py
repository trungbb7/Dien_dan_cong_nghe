from django import forms
from .models import Post,Comment


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

class commentsForm(forms.ModelForm):
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control__comment--input",
                "placeholder": "Enter your comment here",
                "cols": "93",
                "rows": "5",
            }
        ),
    )
    class Meta:
        model = Comment
        fields = [
            "content",
        ]
    