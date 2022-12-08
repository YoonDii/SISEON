from .models import Notes
from django import forms


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ("title", "content")
        labels = {
            "title": "제목",
            "content": "내용",
        }