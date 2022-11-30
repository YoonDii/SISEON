from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse 
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from gathering.models import Gathering, GatheringComment, Poll, Choice
from gathering.forms import GatheringForm, GatheringCommentForm, PollAddForm
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
        context['pollform'] = PollAddForm()

        gathering = self.object

        context['polls'] = Poll.objects.filter(gathering=gathering).order_by('-pub_date')[:1]
        return context

class GatheringCreateView(CreateView):
    model = Gathering 
    form_class = GatheringForm 
    template_name = "gathering/gathering_form.html"
   
    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("gathering:gathering-detail", kwargs={"gathering_id": self.object.id})

class GatheringUpdateView(UpdateView):
    model = Gathering
    form_class = GatheringForm 
    template_name = "gathering/gathering_form.html"
    pk_url_kwarg = "gathering_id"
    
    def get_success_url(self):
        return reverse("gathering:gathering-detail", kwargs={"gathering_id": self.object.id})


def poll_add(request,gathering_id):
    gathering = Gathering.objects.get(pk=gathering_id)    
    if request.method == 'POST':
        form = PollAddForm(request.POST)
        if form.is_valid():
            poll = form.save(commit=False)
            poll.user = request.user
            poll.gathering = gathering
            poll.save()
            new_choice1 = Choice(
                    poll=poll, choice_text=form.cleaned_data['choice1']).save()
            new_choice2 = Choice(
                    poll=poll, choice_text=form.cleaned_data['choice2']).save()
            messages.success(request, "성공적으로 추가함")
            
            return redirect('gathering:gathering-detail', poll.gathering.id)
    else:
        form = PollAddForm()
    context = {
        'form': form,
        }
    return render(request, 'gathering/add_poll.html', context)


# class PollCreateView(CreateView):
#     http_method_names = ['post']
#     model = Poll 
#     form_class = PollAddForm 


#     def form_valid(self, form):
#         form.instance.user = self.request.user 
#         form.instance.gathering = Gathering.objects.get(id=self.kwargs.get('gathering_id'))
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse('gathering-detail', kwargs={'gathering_id': self.kwargs.get('gathering_id')})
    
