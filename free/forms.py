from django import forms
from .models import Free, Comment, ReComment1, Photo
from django.forms import ClearableFileInput


class FreeForm(forms.ModelForm):
    class Meta:
        model = Free
        fields = [
            "title",
            "content",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "제목을 입력해주세요.",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 10,
                    "placeholder": "익명으로 자유롭게 글을 남겨보세요!",
                }
            ),
        }

        labels = {
            "title": "",
            "content": "",
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = [
            "image",
        ]
        widgets = {
            "image": ClearableFileInput(
                attrs={
                    "multiple": True,
                    "onchange": "setThumbnail(event)",
                }
            ),
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
class ReCommentForm(forms.ModelForm):

    class Meta:
        model = ReComment1
        fields = ['body']
        labels = {
            "body": "",
        }
        error_messages = {
            'body': {
                'required':"",
            },
        }