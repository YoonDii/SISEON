from django import forms
from .models import Articles, Comment, Photo
from django.forms import ClearableFileInput


class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Articles
        fields = [
            "title",
            "category",
            "content",
            "unname",
        ]

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        }
        labels = {
            "unname": "익명선택",
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            "image",
        ]
        widgets = {
            "image": ClearableFileInput(attrs={"multiple": True}),
        }
        labels = {
            "image": "이미지를 선택해주세요.",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            "content","unname",
        }
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 1}),
        }
        labels = {
            "unname": "익명선택",
        }