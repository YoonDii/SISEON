from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from gathering.models import Gathering, GatheringComment, Vote, VoteContent
from gathering.forms import GatheringCommentForm, VoteForm
# Create your views here.

class GatheringListView(ListView):
    model = Gathering 
    context_object_name = 'gatherings'
    template_name = 'gathering/gathering_list.html'
    paginate_by = 10 
    ordering = ['-created_at']

class GatheringDetailView(DetailView):
    model = Gathering 
    template_name = 'gathering/gathering_detail.html'
    pk_url_kwarg = 'gathering_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentform'] = GatheringCommentForm()
        context['voteform'] = VoteForm()
        
        # user = self.request.user
        # if user.is_authenticated:
        #     gathering = self.object
        #     context['like_users'] = Gathering.objects.filter(gathering=gathering).filter(like_users=user)
        return context