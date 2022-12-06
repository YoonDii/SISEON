from django import forms
from .models import Notices

# from django.forms import ClearableFileInput


class NoticesForm(forms.ModelForm):
    class Meta:
        model = Notices
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
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        }


# class PhotoForm(forms.ModelForm):
#     class Meta:
#         model = Photo
#         fields = [
#             "image",
#         ]
#         widgets = {
#             "image": ClearableFileInput(attrs={"multiple": True}),
#         }
