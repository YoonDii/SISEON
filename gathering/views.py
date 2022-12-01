from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib import messages
from gathering.models import Poll, Choice, Vote, GatheringComment
from gathering.forms import PollAddForm, EditPollForm, ChoiceAddForm, CommentForm
from django.http import JsonResponse
# Create your views here.

# class GatheringListView(ListView):
#     model = Gathering 
#     context_object_name = 'gatherings'
#     template_name = 'gathering/gathering_list.html'
#     paginate_by = 10 
#     ordering = ['-created_at']

# class GatheringDetailView(DetailView):
#     model = Gathering 
#     template_name = 'gathering/gathering_detail.html'
#     pk_url_kwarg = 'gathering_id'


#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['commentform'] = GatheringCommentForm()
#         context['pollform'] = PollAddForm()
       
#         gathering = self.object
#         context['polls'] = Poll.objects.filter(gathering=gathering).order_by('-pub_date')[:1]
        
        


#         return context


# class GatheringCreateView(CreateView):
#     model = Gathering 
#     form_class = GatheringForm 
#     template_name = "gathering/gathering_form.html"
   
#     def form_valid(self, form):
#         form.instance.user = self.request.user 
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         return reverse("gathering:gathering-detail", kwargs={"gathering_id": self.object.id})

# class GatheringUpdateView(UpdateView):
#     model = Gathering
#     form_class = GatheringForm 
#     template_name = "gathering/gathering_form.html"
#     pk_url_kwarg = "gathering_id"
    
#     def get_success_url(self):
#         return reverse("gathering:gathering-detail", kwargs={"gathering_id": self.object.id})


# def poll_add(request,gathering_id):
#     gathering = Gathering.objects.get(pk=gathering_id)    
#     if request.method == 'POST':
#         form = PollAddForm(request.POST)
#         if form.is_valid():
#             poll = form.save(commit=False)
#             poll.user = request.user
#             poll.gathering = gathering
#             poll.save()
#             new_choice1 = Choice(
#                     poll=poll, choice_text=form.cleaned_data['choice1']).save()
#             new_choice2 = Choice(
#                     poll=poll, choice_text=form.cleaned_data['choice2']).save()
#             messages.success(request, "성공적으로 추가함")
            
#             return redirect('gathering:gathering-detail', poll.gathering.id)
#     else:
#         form = PollAddForm()
#     context = {
#         'form': form,
#         }
#     return render(request, 'gathering/add_poll.html', context)


# class PollCreateView(CreateView):
#     http_method_names = ['post']
#     model = Poll 
#     form_class = PollAddForm 


#     def form_valid(self, form):
#         form.instance.user = self.request.user 
#         form.instance.gathering = Gathering.objects.get(id=self.kwargs.get('gathering_id'))
#         return super().form_valid(form)
    
#     def get_success_url(self):

#         return reverse('gathering:gathering-detail', kwargs={'gathering_id': self.kwargs.get('gathering_id')})


def polls_list(request):
    all_polls = Poll.objects.all()
    search_term = ''
    if 'name' in request.GET:
        all_polls = all_polls.order_by('title')

    if 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')

    if 'vote' in request.GET:
        all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6)  # Show 6 contacts per page
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    context = {
        'polls': polls,
        'params': params,
        'search_term': search_term,
    }
    return render(request, 'gathering/polls_list.html', context)



def list_by_user(request):
    all_polls = Poll.objects.filter(user=request.user)
    paginator = Paginator(all_polls, 7)  # Show 7 contacts per page

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls': polls,
    }
    return render(request, 'gathering/polls_list.html', context)



def polls_add(request):
    if request.method == 'POST':
        form = PollAddForm(request.POST)
        if form.is_valid:
            poll = form.save(commit=False)
            poll.user = request.user
            poll.save()
            new_choice1 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice1']).save()
            new_choice2 = Choice(
                poll=poll, choice_text=form.cleaned_data['choice2']).save()

            messages.success(
                request, "Poll & Choices added successfully.", extra_tags='alert alert-success alert-dismissible fade show')

            return redirect('gathering:gathering-list')
    else:
        form = PollAddForm()
    context = {
        'form': form,
    }
    return render(request, 'gathering/add_poll.html', context)


@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.user:
        return redirect('gathering:gathering-list')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(request, "Poll Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("gathering:gathering-list")

    else:
        form = EditPollForm(instance=poll)

    return render(request, "gathering/poll_edit.html", {'form': form, 'poll': poll})


@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.user:
        return redirect('gathering:gathering-list')
    poll.delete()
    messages.success(request, "Poll Deleted successfully.",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("gathering:list")


@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.user:
        return redirect('gathering:gathering-list')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice added successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('gathering:edit', poll.id)
    else:
        form = ChoiceAddForm()
    context = {
        'form': form,
    }
    return render(request, 'gathering/add_choice.html', context)


@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.user:
        return redirect('gathering:gathering-list')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice Updated successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('gathering:edit', poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'gathering/add_choice.html', context)


@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.user:
        return redirect('gathering:gathering-list')
    choice.delete()
    messages.success(
        request, "Choice Deleted successfully.", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('gathering:edit', poll.id)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    comments = GatheringComment.objects.filter(poll_id=poll_id).order_by('-pk')
    comment_form = CommentForm()
    for i in comments:
        i.updated_at = i.updated_at.strftime()
    if not poll.active:
        return render(request, 'gathering/poll_result.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'gathering/poll_detail.html', context)


@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(
            request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("gathering:gathering-list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        print(vote)
        return render(request, 'gathering/poll_result.html', {'poll': poll})
    else:
        messages.error(
            request, "No choice selected!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:detail", poll_id)
    return render(request, 'gathering/poll_result.html', {'poll': poll})


@login_required
def endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.user:
        return redirect('gathering:gathering-list')

    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, 'gathering/poll_result.html', {'poll': poll})
    else:
        return render(request, 'gathering/poll_result.html', {'poll': poll})

@login_required
def comment_create(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.poll = poll
        comment.user = request.user
        comment.save()
    return redirect("gathering:detail", poll.pk)


def comment_delete(request, comment_pk, articles_pk):
    comment = GatheringComment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("gathering:detail", articles_pk)


def comment_update(request, poll_id, comment_pk):
    comment = GatheringComment.objects.get(pk=comment_pk)

    data = {"comment_content": comment.content}

    return JsonResponse(data)


def comment_update_complete(request, poll_id, comment_pk):
    comment = GatheringComment.objects.get(pk=comment_pk)
    comment_form = CommentForm(request.POST, instance=comment)

    if comment_form.is_valid():
        comment = comment_form.save()

        data = {
            "comment_content": comment.content,
        }

        return JsonResponse(data)

    data = {
        "comment_content": comment.content,
    }

    return JsonResponse(data)


@login_required
def like(request, poll_id):
    articles = get_object_or_404(articles, pk=poll_id)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if articles.like_users.filter(id=request.user.id).exists():
    if request.user in articles.like_users.all():
        # 좋아요 삭제하고
        articles.like_users.remove(request.user)

    else:
        # 좋아요 추가하고
        articles.like_users.add(request.user)

    # 상세 페이지로 redirect

    data = {
        "like_cnt": articles.like_users.count(),
    }

    return JsonResponse(data)

#         return reverse('gathering-detail', kwargs={'gathering_id': self.kwargs.get('gathering_id')})

def meeting_offline(request):
    return render(request, 'gathering/meeting_offline.html')

