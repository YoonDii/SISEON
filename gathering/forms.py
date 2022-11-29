from django import forms 
from gathering.models import Gathering, GatheringComment, Vote, VoteContent

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

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = '__all__'