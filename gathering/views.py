from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse 
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.contrib import messages
from gathering.models import Gathering, Choice, Vote, GatheringComment
from gathering.forms import GatheringAddForm, EditGatheringForm, ChoiceAddForm, CommentForm
from django.http import JsonResponse
# Create your views here.

def gathering_list(request):
    all_gatherings = Gathering.objects.all().order_by('-created_at')

    paginator = Paginator(all_gatherings, 6)  # Show 6 contacts per page
    page = request.GET.get('page')
    gatherings = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    print(params)
    context = {
        'gatherings': gatherings,
        'params': params,
    }
    return render(request, 'gathering/gathering_list.html', context)


def gathering_create(request):
    if request.method == 'POST':
        form = GatheringAddForm(request.POST)
        if form.is_valid:
            gathering = form.save(commit=False)
            gathering.user = request.user
            gathering.save()
            new_choice1 = Choice(
                gathering=gathering, choice_text=form.cleaned_data['choice1']).save()
            new_choice2 = Choice(
                gathering=gathering, choice_text=form.cleaned_data['choice2']).save()

            return redirect('gathering:gathering-list')
    else:
        form = GatheringAddForm()
    context = {
        'form': form,
    }
    return render(request, 'gathering/gathering_create.html', context)


@login_required
def gathering_edit(request, gathering_id):
    gathering = get_object_or_404(Gathering, pk=gathering_id)
    if request.user != gathering.user:
        return redirect('gathering:gathering-list')

    if request.method == 'POST':
        form = EditGatheringForm(request.POST, instance=gathering)
        if form.is_valid:
            form.save()
            messages.success(request, "gathering Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("gathering:gathering-list")

    else:
        form = EditGatheringForm(instance=gathering)

    return render(request, "gathering/gathering_edit.html", {'form': form, 'gathering': gathering})


@login_required
def gathering_delete(request, gathering_id):
    gathering = get_object_or_404(Gathering, pk=gathering_id)
    if request.user != gathering.user:
        return redirect('gathering:gathering-list')
    gathering.delete()
    messages.success(request, "투표가 완료되었습니다.",
                     extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("gathering:gathering-list")


@login_required
def add_choice(request, gathering_id):
    gathering = get_object_or_404(Gathering, pk=gathering_id)
    if request.user != gathering.user:
        return redirect('gathering:gathering-list')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.gathering = gathering
            new_choice.save()
            messages.success(
                request, "Choice added successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('gathering:gathering-edit', gathering.id)
    else:
        form = ChoiceAddForm()
    context = {
        'form': form,
    }
    return render(request, 'gathering/add_choice.html', context)


@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    gathering = get_object_or_404(Gathering, pk=choice.gathering.id)
    if request.user != gathering.user:
        return redirect('gathering:gathering-list')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.gathering = gathering
            new_choice.save()
            messages.success(
                request, "Choice Updated successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('gathering:gathering-edit', gathering.id)
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
    gathering = get_object_or_404(Gathering, pk=choice.gathering.id)
    if request.user != gathering.user:
        return redirect('gathering:gathering-list')
    choice.delete()
    messages.success(
        request, "Choice Deleted successfully.", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('gathering:gathering-edit', gathering.id)


def gathering_detail(request, gathering_id):
    gathering = get_object_or_404(Gathering, id=gathering_id)
    comments = GatheringComment.objects.filter(gathering_id=gathering_id).order_by('-pk')
    comment_form = CommentForm()
    for i in comments:
        i.updated_at = i.updated_at.strftime("%y-%m-%d")
    
    loop_count = gathering.choice_set.count()
    context = {
        'gathering': gathering,
        'loop_time': range(0, loop_count),
        'comments': comments,
        'comment_form': comment_form
    }
    if not gathering.active:
        return render(request, 'gathering/gathering_result.html', context)
    return render(request, 'gathering/gathering_detail.html', context)


@login_required
def gathering_vote(request, gathering_id):
    gathering = get_object_or_404(Gathering, pk=gathering_id)
    choice_id = request.POST.get('choice')
    if not gathering.user_can_vote(request.user):
        messages.error(
            request, "이미 투표하셨습니다!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("gathering:gathering-list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, gathering=gathering, choice=choice)
        vote.save()
        print(vote)
        return render(request, 'gathering/gathering_result.html', {'gathering': gathering})
    else:
        messages.error(
            request, "No choice selected!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("gathering:gathering-detail", gathering_id)


@login_required
def end_gathering(request, gathering_id):
    gathering = get_object_or_404(Gathering, pk=gathering_id)
    comments = GatheringComment.objects.filter(gathering_id=gathering_id).order_by('-pk')
    comment_form = CommentForm()
    if request.user != gathering.user:
        return redirect('gathering:gathering-list')
    for i in comments:
        i.updated_at = i.updated_at.strftime("%y-%m-%d")
    
    context = {
        'gathering': gathering,
        'comments': comments,
        'comment_form': comment_form,
    }

    if gathering.active is True:
        gathering.active = False
        gathering.save()
        return render(request, 'gathering/gathering_result.html', context)
    else:
        return render(request, 'gathering/gathering_result.html', context)

@login_required
def comment_create(request, gathering_id):
    gathering = Gathering.objects.get(pk=gathering_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.gathering = gathering
        comment.user = request.user
        comment.save()
    return redirect("gathering:gathering-detail", gathering.pk)


def comment_delete(request, comment_pk, gathering_id):
    comment = GatheringComment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("gathering:gathering-detail", gathering_id)


def comment_update(request, gathering_id, comment_pk):
    comment = GatheringComment.objects.get(pk=comment_pk)

    data = {"comment_content": comment.content}

    return JsonResponse(data)


def comment_update_complete(request, gathering_id, comment_pk):
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
def like(request, gathering_id):
    gathering = get_object_or_404(Gathering, pk=gathering_id)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if articles.like_users.filter(id=request.user.id).exists():
    if request.user in gathering.like_users.all():
        # 좋아요 삭제하고
        gathering.like_users.remove(request.user)

    else:
        # 좋아요 추가하고
        gathering.like_users.add(request.user)

    # 상세 페이지로 redirect

    data = {
        "like_cnt": gathering.like_users.count(),
    }

    return JsonResponse(data)


def meeting_offline(request):
    return render(request, 'gathering/meeting_offline.html')

