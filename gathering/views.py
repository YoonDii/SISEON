from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import User, Notification
from gathering.models import Gatherings, Choice, Vote, GatheringsComment
from gathering.forms import (
    GatheringsAddForm,
    EditGatheringsForm,
    ChoiceAddForm,
    CommentForm,
)
from django.http import JsonResponse
from datetime import date, datetime, timedelta

# Create your views here.


def maketable(p):
    table = [0] * len(p)
    i = 0
    for j in range(1, len(p)):
        while i > 0 and p[i] != p[j]:
            i = table[i - 1]
        if p[i] == p[j]:
            i += 1
            table[j] = i
    return table


def KMP(p, t):
    ans = []
    table = maketable(p)
    i = 0
    for j in range(len(t)):
        while i > 0 and p[i] != t[j]:
            i = table[i - 1]
        if p[i] == t[j]:
            if i == len(p) - 1:
                ans.append(j - len(p) + 2)
                i = table[i]
            else:
                i += 1
    return ans


def gathering_list(request):

    all_gatherings = Gatherings.objects.all().order_by('-created_at')
    paginator = Paginator(all_gatherings, 8)  
    page = request.GET.get('page')

    gatherings = paginator.get_page(page)


    get_dict_copy = request.GET.copy()

    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()
    
    context = {"gatherings": gatherings,'params': params}


    return render(request, "gathering/gathering_list.html", context)


def gathering_create(request):
    if request.method == "POST":
        form = GatheringsAddForm(request.POST)
        if form.is_valid:
            gathering = form.save(commit=False)
            gathering.user = request.user
            gathering.save()
            new_choice1 = Choice(
                gathering=gathering, choice_text=form.cleaned_data["choice1"]
            ).save()

            new_choice2 = Choice(
                gathering=gathering, choice_text=form.cleaned_data["choice2"]
            ).save()

            return redirect("gathering:gathering-list")
    else:
        form = GatheringsAddForm()
    context = {
        "form": form,
    }
    return render(request, "gathering/gathering_create.html", context)


def gathering_detail(request, gathering_id):
    gathering = get_object_or_404(Gatherings, id=gathering_id)
    user = User.objects.get(pk=request.user.pk)
    comments = GatheringsComment.objects.filter(gathering_id=gathering_id).order_by(
        "-pk"
    )
    comment_form = CommentForm()
    for i in comments:
        i.updated_at = i.updated_at.strftime("%y-%m-%d")
        with open("filtering.txt", "r", encoding="utf-8") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, i.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(i.content) // 2:
                            i.content = (
                                len(i.content[k - 1 : len(word)]) * "*"
                                + i.content[len(word) :]
                            )
                        else:
                            i.content = (
                                i.content[0 : k - 1] + len(i.content[k - 1 :]) * "*"
                            )
    if request.user.is_authenticated:
        new_message = Notification.objects.filter(Q(user_id=user.pk) & Q(check=False))
        message_count = len(new_message)
    loop_count = gathering.choice_set.count()
    context = {
        "gathering": gathering,
        "loop_time": range(0, loop_count),
        "comments": comments,
        "comment_form": comment_form,
        "count": message_count,
    }

    response = render(request, "gathering/gathering_detail.html", context)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookievalue = request.COOKIES.get("hitreview", "")

    if f"{gathering_id}" not in cookievalue:
        cookievalue += f"{gathering_id}"
        response.set_cookie(
            "hitreview", value=cookievalue, max_age=max_age, httponly=True
        )
        gathering.hits += 1
        gathering.save()

    if not gathering.active:
        return render(request, "gathering/gathering_result.html", context)
    return response


@login_required
def gathering_edit(request, gathering_id):
    gathering = get_object_or_404(Gatherings, pk=gathering_id)
    if request.user != gathering.user:
        return redirect("gathering:gathering-list")
    if request.method == "POST":
        form = EditGatheringsForm(request.POST, instance=gathering)
        if form.is_valid:
            form.save()
            return redirect("gathering:gathering-detail", gathering.id)
    else:
        form = EditGatheringsForm(instance=gathering)

    return render(
        request, "gathering/gathering_edit.html", {"form": form, "gathering": gathering}
    )


@login_required
def gathering_delete(request, gathering_id):
    gathering = get_object_or_404(Gatherings, pk=gathering_id)
    if request.user != gathering.user:
        return redirect("gathering:gathering-list")
    gathering.delete()
    messages.success(
        request,
        "투표가 완료되었습니다.",
        extra_tags="alert alert-success alert-dismissible fade show",
    )
    return redirect("gathering:gathering-list")


@login_required
def add_choice(request, gathering_id):
    gathering = get_object_or_404(Gatherings, pk=gathering_id)
    if request.user != gathering.user:
        return redirect("gathering:gathering-list")

    if request.method == "POST":
        form = ChoiceAddForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.gathering = gathering
            new_choice.save()
            messages.success(
                request,
                "선택사항이 추가되었습니다.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("gathering:gathering-edit", gathering.id)
    else:
        form = ChoiceAddForm()
    context = {
        "form": form,
    }
    return render(request, "gathering/add_choice.html", context)


@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    gathering = get_object_or_404(Gatherings, pk=choice.gathering.id)
    if request.user != gathering.user:
        return redirect("gathering:gathering-list")

    if request.method == "POST":
        form = ChoiceAddForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.gathering = gathering
            new_choice.save()
            messages.success(
                request,
                "선택사항이 업데이트 되었습니다.",
                extra_tags="alert alert-success alert-dismissible fade show",
            )
            return redirect("gathering:gathering-edit", gathering.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        "form": form,
        "edit_choice": True,
        "choice": choice,
    }
    return render(request, "gathering/add_choice.html", context)


@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    gathering = get_object_or_404(Gatherings, pk=choice.gathering.id)
    if request.user != gathering.user:
        return redirect("gathering:gathering-list")
    choice.delete()
    messages.success(
        request,
        "선택사항이 삭제되었습니다.",
        extra_tags="alert alert-success alert-dismissible fade show",
    )
    return redirect("gathering:gathering-edit", gathering.id)


@login_required
def gathering_vote(request, gathering_id):
    gathering = get_object_or_404(Gatherings, pk=gathering_id)
    choice_id = request.POST.get("choice")
    comments = GatheringsComment.objects.filter(gathering_id=gathering_id).order_by("-pk")
    comment_form = CommentForm()
    if not gathering.user_can_vote(request.user):
        messages.error(
            request,
            "이미 투표하셨습니다!",
            extra_tags="alert alert-warning alert-dismissible fade show",
        )
        return redirect("gathering:gathering-detail", gathering_id)

    elif choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, gathering=gathering, choice=choice)
        vote.save()
        context = {
            "gathering": gathering,
            "comments": comments,
            "comment_form": comment_form,
        }
        return render(request, "gathering/gathering_result.html", context)
    else:
        messages.error(
            request,
            "선택 후 투표 부탁드립니다",
            extra_tags="alert alert-warning alert-dismissible fade show",
        )
        return redirect("gathering:gathering-detail", gathering_id)


@login_required
def end_gathering(request, gathering_id):
    gathering = get_object_or_404(Gatherings, pk=gathering_id)

    comments = GatheringsComment.objects.filter(gathering_id=gathering_id).order_by(
        "-pk"
    )
    comment_form = CommentForm()
    for i in comments:
        i.updated_at = i.updated_at.strftime("%y-%m-%d")

    if request.user != gathering.user:
        return redirect("gathering:gathering-list")

    context = {
        "gathering": gathering,
        "comments": comments,
        "comment_form": comment_form,
    }

    if gathering.active is True:
        gathering.active = False
        gathering.save()
        return render(request, "gathering/gathering_result.html", context)
    else:
        return render(request, "gathering/gathering_result.html", context)


@login_required
def comment_create(request, gathering_id):
    gathering = Gatherings.objects.get(pk=gathering_id)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.gathering = gathering
        comment.user = request.user
        comment.save()
    return redirect("gathering:gathering-detail", gathering.pk)


def comment_delete(request, comment_pk, gathering_id):
    comment = GatheringsComment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("gathering:gathering-detail", gathering_id)


def comment_update(request, gathering_id, comment_pk):
    comment = GatheringsComment.objects.get(pk=comment_pk)

    data = {"comment_content": comment.content}

    return JsonResponse(data)


def comment_update_complete(request, gathering_id, comment_pk):
    comment = GatheringsComment.objects.get(pk=comment_pk)
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
    gathering = get_object_or_404(Gatherings, pk=gathering_id)
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
    return render(request, "gathering/meeting_offline.html")


@login_required
def search(request):
    all_data = Gatherings.objects.order_by("-pk")
    search = request.GET.get("search", "")
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(all_data, 10)
    page_obj = paginator.get_page(page)
    if search:
        search_list = all_data.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(nickname__icontains=search)
            | Q(category__icontains=search)
        )
        paginator = Paginator(search_list, 10)  # 페이지당 10개씩 보여주기
        page_obj = paginator.get_page(page)
        context = {
            "search": search,
            "search_list": search_list,
            "question_list": page_obj,
        }
    else:
        context = {
            "search": search,
            "search_list": all_data,
            "question_list": page_obj,
        }

    return render(request, "gathering/search.html", context)
