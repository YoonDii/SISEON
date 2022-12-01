from django import forms 
from gathering.models import Poll, Choice, GatheringComment


class PollAddForm(forms.ModelForm):

    choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Poll
        fields = ['title','category','content', 'choice1', 'choice2', ]
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['content', ]
        widgets = {
            'title': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'cols': 20}),
        }


class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', ]
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control', })
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
