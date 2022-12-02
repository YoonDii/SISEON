from django import forms
from gathering.models import Gathering, Choice, GatheringComment


class GatheringAddForm(forms.ModelForm):

    choice1 = forms.CharField(
        label="선택 1",
        max_length=100,
        min_length=1,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    choice2 = forms.CharField(
        label="선택 2",
        max_length=100,
        min_length=1,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Gathering
        fields = [
            "title",
            "category",
            "content",
            "choice1",
            "choice2",
        ]
        widgets = {
            "title": forms.Textarea(
                attrs={"class": "form-control", "rows": 5, "cols": 20}
            ),
        }
        labels = {
            "category": "카테고리",
            "title": "제목",
            "content": "내용",
            "choice1": "선택1",
            "choice2": "선택2",
        }


class EditGatheringForm(forms.ModelForm):
    class Meta:
        model = Gathering
        fields = [
            "content",
        ]
        widgets = {
            "title": forms.Textarea(
                attrs={"class": "form-control", "rows": 5, "cols": 20}
            ),
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = [
            "choice_text",
        ]
        widgets = {
            "choice_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = GatheringComment
        fields = [
            "content",
        ]

        widgets = {
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 1}),
        }
