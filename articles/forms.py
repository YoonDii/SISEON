from django import forms
from .models import Articles


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = [
            "title",
            "category",
            "content",
            "image",
        ]

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        }
