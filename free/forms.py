from django import forms
from .models import Free, Comment, Photo
from django.forms import ClearableFileInput


class FreeForm(forms.ModelForm):
    class Meta:
        model = Free
        fields = [
            "title",
            "content",
        ]

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
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
        fields = [
            "content",
        ]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 1,
                    "placeholder": "댓글을 남겨주세요!",
                }
            ),
        }

        labels = {
            "content": "",
        }
