from django import forms 
from gathering.models import Gathering, GatheringComment, Poll, Choice

class GatheringForm(forms.ModelForm):
    class Meta:
        model = Gathering
        fields = [
            'title',
            'category',
            'content',
            'image',
        ]


class GatheringCommentForm(forms.ModelForm):
    class Meta:
        model = GatheringComment
        fields = [
            'content',
        ]

class PollAddForm(forms.ModelForm):

    choice1 = forms.CharField(label='Choice 1', max_length=100, min_length=1,)
    choice2 = forms.CharField(label='Choice 2', max_length=100, min_length=1,)

    class Meta:
        model = Poll
        fields = ['text', 'choice1', 'choice2']
        
class EditPollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['text', ]
        

class ChoiceAddForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text',]
