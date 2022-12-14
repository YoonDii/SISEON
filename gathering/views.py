from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.core.paginator import Paginator
from django.contrib import messages
from accounts.models import User, Notification
from gathering.models import Gatherings, Choice, Vote, GatheringsComment, ReComment3
from gathering.forms import (
    GatheringsAddForm,
    EditGatheringsForm,
    ChoiceAddForm,
    CommentForm,
    ReCommentForm,
)
from django.http import JsonResponse
from datetime import date, datetime, timedelta
import json

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
    all_gathering = Gatherings.objects.all().order_by("-created_at")

    page = request.GET.get("page", "1")
    paginator = Paginator(all_gathering, 9)
    page_obj = paginator.get_page(page)
    context = {
        "all_gatherings": all_gathering,
        "page_obj": page_obj,
    }
    return render(request, "gathering/gathering_list.html", context)


@login_required
def gathering_create(request):
    if request.method == "POST":
        form = GatheringsAddForm(request.POST)
        if form.is_valid():
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
    comment_form.fields["content"].widget.attrs[
        "placeholder"
    ] = "댓글을 남겨주세요!\n댓글이 길어질 땐 댓글창을 늘려보세요."
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
    if not gathering.active:
        response = render(request, "gathering/gathering_result.html", context)
    else:
        response = render(request, "gathering/gathering_detail.html", context)
    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookievalue = request.COOKIES.get("hitgathering", "")

    if f"{gathering_id}" not in cookievalue:
        cookievalue += f"{gathering_id}"
        response.set_cookie(
            "hitgathering", value=cookievalue, max_age=max_age, httponly=True
        )
        gathering.hits += 1
        gathering.save()
    return response


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


# 게시글 수정 페이지
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
        form_choice = ChoiceAddForm()
        form_edit = []
        for choice in gathering.choice_set.all():
            form_edit.append([choice, ChoiceAddForm(instance=choice)])

    return render(
        request,
        "gathering/gathering_edit.html",
        {
            "form": form,
            "gathering": gathering,
            "form_choice": form_choice,
            "form_edit": form_edit,
        },
    )


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
    comments = GatheringsComment.objects.filter(gathering_id=gathering_id).order_by(
        "-pk"
    )
    comment_form = CommentForm()
    comment_form.fields["content"].widget.attrs[
        "placeholder"
    ] = "댓글을 남겨주세요!\n댓글이 길어질 땐 댓글창을 늘려보세요."
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
    comment_form.fields["content"].widget.attrs[
        "placeholder"
    ] = "댓글을 남겨주세요!\n댓글이 길어질 땐 댓글창을 늘려보세요."
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
def comment_create(request, gathering_pk):
    gatherings = Gatherings.objects.get(pk=gathering_pk)
    comment_form = CommentForm(request.POST)
    user = request.user.pk
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.gathering = gatherings
        comment.user = request.user
        comment.save()
        message = f"모임게시판 {gatherings.title}의 글에 {request.user.nickname}님이 댓글을 달았습니다."
        Notification.objects.create(
            user=gatherings.user, message=message, category="모임", nid=gatherings.pk
        )
    temp1 = GatheringsComment.objects.filter(gathering_id=gathering_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment3.objects.filter(comment_id=t.pk).order_by("-pk")
        t.updated_at = t.updated_at.strftime("%Y-%m-%d %H:%M")
        with open("filtering.txt", "r", encoding="utf-8") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.nickname,
                "recomment_cnt": temp2.count(),
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
            }
        )
        for r in temp2:
            r.updated_at = r.updated_at.strftime("%Y-%m-%d %H:%M")
            with open("filtering.txt", "r", encoding="utf-8") as txtfile:
                for word in txtfile.readlines():
                    word = word.strip()
                    ans = KMP(word, r.body)
                    if ans:
                        for k in ans:
                            k = int(k)
                            if k < len(r.body) // 2:
                                r.content = (
                                    len(r.body[k - 1 : len(word)]) * "*"
                                    + r.body[len(word) :]
                                )
                            else:
                                r.body = r.body[0 : k - 1] + len(r.body[k - 1 :]) * "*"
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.nickname,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                }
            )
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "gathering_pk": gathering_pk,
        "user": user,
    }
    return JsonResponse(context)


@login_required
def comment_delete(request, comment_pk, gathering_pk):
    comment = GatheringsComment.objects.get(pk=comment_pk)
    gathering_pk = Gatherings.objects.get(pk=gathering_pk).pk
    user = request.user.pk
    comment.delete()
    temp1 = GatheringsComment.objects.filter(gathering_id=gathering_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment3.objects.filter(comment_id=t.pk).order_by("-pk")
        t.updated_at = t.updated_at.strftime("%Y-%m-%d %H:%M")
        with open("filtering.txt", "r", encoding="utf-8") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.nickname,
                "recomment_cnt": temp2.count(),
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
            }
        )
        for r in temp2:
            r.updated_at = r.updated_at.strftime("%Y-%m-%d %H:%M")
            with open("filtering.txt", "r", encoding="utf-8") as txtfile:
                for word in txtfile.readlines():
                    word = word.strip()
                    ans = KMP(word, r.body)
                    if ans:
                        for k in ans:
                            k = int(k)
                            if k < len(r.body) // 2:
                                r.content = (
                                    len(r.body[k - 1 : len(word)]) * "*"
                                    + r.body[len(word) :]
                                )
                            else:
                                r.body = r.body[0 : k - 1] + len(r.body[k - 1 :]) * "*"
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.nickname,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                }
            )
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "gathering_pk": gathering_pk,
        "user": user,
    }
    return JsonResponse(context)


@login_required
def comment_update(request, gathering_pk, comment_pk):
    comment = GatheringsComment.objects.get(pk=comment_pk)
    comment_username = comment.user.username
    user = request.user.pk
    gathering_pk = Gatherings.objects.get(pk=gathering_pk).pk
    jsonObject = json.loads(request.body)
    if request.method == "POST":
        comment.content = jsonObject.get("content")
        comment.save()
    temp1 = GatheringsComment.objects.filter(gathering_id=gathering_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment3.objects.filter(comment_id=t.pk).order_by("-pk")
        t.updated_at = t.updated_at.strftime("%Y-%m-%d %H:%M")
        with open("filtering.txt", "r", encoding="utf-8") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.nickname,
                "recomment_cnt": temp2.count(),
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
            }
        )
        for r in temp2:
            r.updated_at = r.updated_at.strftime("%Y-%m-%d %H:%M")
            with open("filtering.txt", "r", encoding="utf-8") as txtfile:
                for word in txtfile.readlines():
                    word = word.strip()
                    ans = KMP(word, r.body)
                    if ans:
                        for k in ans:
                            k = int(k)
                            if k < len(r.body) // 2:
                                r.content = (
                                    len(r.body[k - 1 : len(word)]) * "*"
                                    + r.body[len(word) :]
                                )
                            else:
                                r.body = r.body[0 : k - 1] + len(r.body[k - 1 :]) * "*"
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.nickname,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                }
            )
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "gathering_pk": gathering_pk,
        "user": user,
    }
    return JsonResponse(context)


@login_required
def recomment_create(request, gathering_pk, comment_pk):
    gathering_pk = Gatherings.objects.get(pk=gathering_pk).pk
    gathering = Gatherings.objects.get(pk=gathering_pk)
    users = User.objects.get(pk=request.user.pk)
    comments = GatheringsComment.objects.get(pk=comment_pk)
    recomment_form = ReCommentForm(request.POST)
    user = request.user.pk
    if recomment_form.is_valid():
        comment = recomment_form.save(commit=False)
        comment.user = request.user
        comment.comment = comments
        comment.save()
        message = f"모임게시판 {gathering.title}의 글에 {users.nickname}님이 대댓글을 달았습니다."
        Notification.objects.create(
            user=gathering.user, message=message, category="모임", nid=gathering.pk
        )
    temp1 = GatheringsComment.objects.filter(gathering_id=gathering_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment3.objects.filter(comment_id=t.pk).order_by("-pk")
        t.updated_at = t.updated_at.strftime("%Y-%m-%d %H:%M")
        with open("filtering.txt", "r", encoding="utf-8") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.nickname,
                "recomment_cnt": temp2.count(),
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
            }
        )
        for r in temp2:
            r.updated_at = r.updated_at.strftime("%Y-%m-%d %H:%M")
            with open("filtering.txt", "r", encoding="utf-8") as txtfile:
                for word in txtfile.readlines():
                    word = word.strip()
                    ans = KMP(word, r.body)
                    if ans:
                        for k in ans:
                            k = int(k)
                            if k < len(r.body) // 2:
                                r.content = (
                                    len(r.body[k - 1 : len(word)]) * "*"
                                    + r.body[len(word) :]
                                )
                            else:
                                r.body = r.body[0 : k - 1] + len(r.body[k - 1 :]) * "*"
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.nickname,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                }
            )
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "gathering_pk": gathering_pk,
        "user": user,
    }
    return JsonResponse(context)


@login_required
def recomment_delete(request, gathering_pk, comment_pk, recomment_pk):
    recomment = ReComment3.objects.get(pk=recomment_pk)
    gathering_pk = Gatherings.objects.get(pk=gathering_pk).pk
    user = request.user.pk
    recomment.delete()
    temp1 = GatheringsComment.objects.filter(gathering_id=gathering_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment3.objects.filter(comment_id=t.pk).order_by("-pk")
        t.updated_at = t.updated_at.strftime("%Y-%m-%d %H:%M")
        with open("filtering.txt", "r", encoding="utf-8") as txtfile:
            for word in txtfile.readlines():
                word = word.strip()
                ans = KMP(word, t.content)
                if ans:
                    for k in ans:
                        k = int(k)
                        if k < len(t.content) // 2:
                            t.content = (
                                len(t.content[k - 1 : len(word)]) * "*"
                                + t.content[len(word) :]
                            )
                        else:
                            t.content = (
                                t.content[0 : k - 1] + len(t.content[k - 1 :]) * "*"
                            )
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.nickname,
                "recomment_cnt": temp2.count(),
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
            }
        )
        for r in temp2:
            r.updated_at = r.updated_at.strftime("%Y-%m-%d %H:%M")
            with open("filtering.txt", "r", encoding="utf-8") as txtfile:
                for word in txtfile.readlines():
                    word = word.strip()
                    ans = KMP(word, r.body)
                    if ans:
                        for k in ans:
                            k = int(k)
                            if k < len(r.body) // 2:
                                r.content = (
                                    len(r.body[k - 1 : len(word)]) * "*"
                                    + r.body[len(word) :]
                                )
                            else:
                                r.body = r.body[0 : k - 1] + len(r.body[k - 1 :]) * "*"
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.nickname,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                }
            )
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "gathering_pk": gathering_pk,
        "user": user,
    }
    return JsonResponse(context)


@login_required
def like(request, gathering_pk):
    gathering = get_object_or_404(Gatherings, pk=gathering_pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if articles.like_users.filter(id=request.user.id).exists():
    if request.user in gathering.like_users.all():
        # 좋아요 삭제하고
        gathering.like_users.remove(request.user)
        is_like = False
    else:
        # 좋아요 추가하고
        gathering.like_users.add(request.user)
        is_like = True

    data = {
        "isLike": is_like,
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
            | Q(user_id__nickname__icontains=search)
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


def fail(request):
    return render(request, "gathering/fail.html")


def study(request):
    study = Gatherings.objects.filter(category="스터디").order_by("-pk")
    page = request.GET.get("page", "1")
    paginator = Paginator(study, 9)
    page_obj = paginator.get_page(page)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "gathering/search_study.html", context)


def moim(request):
    moim = Gatherings.objects.filter(category="모임").order_by("-pk")
    page = request.GET.get("page", "1")
    paginator = Paginator(moim, 9)
    page_obj = paginator.get_page(page)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "gathering/search_moim.html", context)
