from django import forms
from .models import Articles, Comment, ReComment2, Photo
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
            "title": forms.TextInput(
                attrs={
                    "placeholder": "제목을 입력해주세요.",
                }
            ),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        }
        labels = {
            "title": "제목",
            "category": "분류",
            "unname": "익명선택",
            "content": "내용",
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
            "content",
            "unname",
        }
        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 1}),
        }
        labels = {
            "unname": "익명선택",
        }


class ReCommentForm(forms.ModelForm):
    class Meta:
        model = ReComment2
        fields = [
            "body",
            "unname",
        ]
        widgets = {
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 1}),
        }
        labels = {
            "unname": "익명선택",
        }
