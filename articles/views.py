from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ArticlesForm, CommentForm, ReCommentForm, PhotoForm
from accounts.models import User, Notification
from django.db.models import Count
from django.db.models import Q
from datetime import date, datetime, timedelta
import json
from django.core.paginator import Paginator

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


def index(request):
    articles = Articles.objects.order_by("-pk")  # 최신순으로나타내기
    page = request.GET.get("page", "1")
    paginator = Paginator(articles, 3)
    page_obj = paginator.get_page(page)
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
        message_count = len(new_message)
        context = {
            "articles": articles,
            "count": message_count,
            "question_list": page_obj,
        }
    else:
        context = {"articles": articles, "question_list": page_obj}
    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
        message_count = len(new_message)
    if request.method == "POST":
        form = ArticlesForm(request.POST, request.FILES)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if form.is_valid() and photo_form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            if len(images):
                for image in images:
                    image_instance = Photo(article=article, image=image)
                    article.save()
                    image_instance.save()
            else:
                article.save()
            return redirect("articles:index")
    else:
        form = ArticlesForm()
        photo_form = PhotoForm()

    context = {
        "count":message_count,
        "form": form,
        "photo_form": photo_form,
    }
    return render(request, "articles/create.html", context)


@login_required
def detail(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    user = User.objects.get(pk=request.user.pk)
    comments = Comment.objects.filter(articles_id=articles_pk).order_by("-pk")
    comment_form = CommentForm()
    recomment_form = ReCommentForm()
    comment_form.fields["content"].widget.attrs["placeholder"] = "댓글 작성"
    recomment_form.fields["body"].widget.attrs["placeholder"] = "답글 작성"

    photos = articles.photo_set.all()
    for i in comments:  # 시간바꾸는로직
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
    context = {
        "count": message_count,
        "articles": articles,
        "comment_form": comment_form,
        "recomment_form": recomment_form,
        "comments": comments,
        "photos": photos,
    }

    response = render(request, "articles/detail.html", context)

    expire_date, now = datetime.now(), datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()

    cookievalue = request.COOKIES.get("hitreview", "")

    if f"{articles_pk}" not in cookievalue:
        cookievalue += f"{articles_pk}"
        response.set_cookie(
            "hitreview", value=cookievalue, max_age=max_age, httponly=True
        )
        articles.hits += 1
        articles.save()
    return response


@login_required
def update(request, articles_pk):
    article = Articles.objects.get(pk=articles_pk)
    user = User.objects.get(pk=request.user.pk)
    if request.user == article.user:
        photos = article.photo_set.all()
        instancetitle = article.title
        if request.method == "POST":
            form = ArticlesForm(request.POST, request.FILES, instance=article)
            if photos:
                photo_form = PhotoForm(request.POST, request.FILES, instance=photos[0])
            else:
                photo_form = PhotoForm(request.POST, request.FILES)
            images = request.FILES.getlist("image")
            for photo in photos:
                if photo.image:
                    photo.delete()
            if form.is_valid() and photo_form.is_valid():
                article = form.save(commit=False)
                article.check = True
                article.user = request.user
                if len(images):
                    for image in images:
                        image_instance = Photo(article=article, image=image)
                        article.save()
                        image_instance.save()
                else:
                    article.save()
                return redirect("articles:detail", article.pk)
        else:
            form = ArticlesForm(instance=article)
            if photos:
                photo_form = PhotoForm(instance=photos[0])
            else:
                photo_form = PhotoForm()
        if request.user.is_authenticated:
            new_message = Notification.objects.filter(
                Q(user_id=user.pk) & Q(check=False)
            )
            message_count = len(new_message)
            context = {
                "count": message_count,
                "form": form,
                "photo_form": photo_form,
                "instancetitle": instancetitle,
                "article": article,
            }
        else:
            context = {
                "form": form,
                "photo_form": photo_form,
                "instancetitle": instancetitle,
                "article": article,
            }
        return render(request, "articles/update.html", context)
    else:
        return redirect("articles:index")


@login_required
def delete(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    articles.delete()
    return redirect("articles:index")

@login_required
def fail(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
        message_count = len(new_message)
    context = {
        "count":message_count,
    }
    return render(request, "articles/fail.html")


@login_required
def comment_create(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    users = User.objects.get(pk=request.user.pk)
    comment_form = CommentForm(request.POST)
    recomment_form = ReCommentForm(request.POST)
    user = request.user.pk
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.articles = articles
        comment.user = request.user
        comment.save()
        if comment.unname:
            message = f"질문게시판 {articles.title}의 글에 {'익명' + str(users.pk)}님이 댓글을 달았습니다."
        else:
            message = f"질문게시판 {articles.title}의 글에 {users}님이 댓글을 달았습니다."
        Notification.objects.create(
            user=articles.user, message=message, category="질문", nid=articles.pk
        )
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
        message_count = len(new_message)
    temp1 = Comment.objects.filter(articles_id=articles_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment2.objects.filter(comment_id=t.pk).order_by("-pk")
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
        if t.unname:
            t.user.username = "익명" + str(t.user_id)
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
                "recomment_cnt": temp2.count(),
                "unname": t.unname,
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
            if r.unname:
                r.user.username = "익명" + str(r.user_id)
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.username,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                    "unname": r.unname,
                }
            )
    context = {
        "count": message_count,
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "articles_pk": articles_pk,
        "user": user,
    }
    return JsonResponse(context)


@login_required
def comment_delete(request, comment_pk, articles_pk):
    comment = Comment.objects.get(pk=comment_pk)
    articles_pk = Articles.objects.get(pk=articles_pk).pk
    user = request.user.pk
    comment.delete()
    # 제이슨은 객체 형태로 받질 않음 그래서 리스트 형태로 전환을 위해 리스트 생성
    temp1 = Comment.objects.filter(articles_id=articles_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment2.objects.filter(comment_id=t.pk).order_by("-pk")
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
        if t.unname:
            t.user.username = "익명" + str(t.user_id)
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
                "recomment_cnt": temp2.count(),
                "unname": t.unname,
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
            if r.unname:
                r.user.username = "익명" + str(r.user_id)
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.username,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                    "unname": r.unname,
                }
            )
    print(comment_data)
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "articles_pk": articles_pk,
        "user": user,
    }
    return JsonResponse(context)


@login_required
def comment_update(request, articles_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment_username = comment.user.username
    user = request.user.pk
    articles_pk = Articles.objects.get(pk=articles_pk).pk
    jsonObject = json.loads(request.body)
    if request.method == "POST":
        comment.content = jsonObject.get("content")
        comment.save()
    temp1 = Comment.objects.filter(articles_id=articles_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment2.objects.filter(comment_id=t.pk).order_by("-pk")
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
        if t.unname:
            t.user.username = "익명" + str(t.user_id)
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
                "recomment_cnt": temp2.count(),
                "unname": t.unname,
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
            if r.unname:
                r.user.username = "익명" + str(r.user_id)
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.username,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                    "unname": r.unname,
                }
            )
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "articles_pk": articles_pk,
        "user": user,
    }
    return JsonResponse(context)


@login_required
def recomment_create(request, articles_pk, comment_pk):
    articles = Articles.objects.get(pk=articles_pk)
    users = User.objects.get(pk=request.user.pk)
    comments = Comment.objects.get(pk=comment_pk)
    recomment_form = ReCommentForm(request.POST)
    user = request.user.pk
    if recomment_form.is_valid():
        comment = recomment_form.save(commit=False)
        comment.user = request.user
        comment.comment = comments
        comment.save()
        if comment.unname:
            message = f"질문게시판 {articles.title}의 글에 {'익명' + str(users.pk)}님이 대댓글을 달았습니다."
        else:
            message = f"질문게시판 {articles.title}의 글에 {users}님이 대댓글을 달았습니다."
        Notification.objects.create(
            user=articles.user, message=message, category="질문", nid=articles.pk
        )
    temp1 = Comment.objects.filter(articles_id=articles_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment2.objects.filter(comment_id=t.pk).order_by("-pk")
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
        if t.unname:
            t.user.username = "익명" + str(t.user_id)
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
                "recomment_cnt": temp2.count(),
                "unname": t.unname,
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
            if r.unname:
                r.user.username = "익명" + str(r.user_id)
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.username,
                    "content": r.body,
                    "commentPk": t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                    "unname": r.unname,
                }
            )
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "articles_pk": articles_pk,
        "user": user,
    }
    return JsonResponse(context)

@login_required
def recomment_delete(request,articles_pk, comment_pk, recomment_pk):
    recomment = ReComment2.objects.get(pk=recomment_pk)
    articles_pk = Articles.objects.get(pk=articles_pk).pk
    user = request.user.pk
    recomment.delete()
    # 제이슨은 객체 형태로 받질 않음 그래서 리스트 형태로 전환을 위해 리스트 생성
    temp1 = Comment.objects.filter(articles_id=articles_pk).order_by("-pk")
    comment_data = []
    recomment_data2 = []
    for t in temp1:
        temp2 = ReComment2.objects.filter(comment_id=t.pk).order_by("-pk")
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
        if t.unname:
            t.user.username = "익명" + str(t.user_id)
        comment_data.append(
            {
                "id": t.user_id,
                "userName": t.user.username,
                "content": t.content,
                "commentPk": t.pk,
                "updated_at": t.updated_at,
                "recomment_cnt": temp2.count(),
                "unname": t.unname,
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
                                r.body = (
                                    r.body[0 : k - 1] + len(r.body[k - 1 :]) * "*"
                                )
            if r.unname:
                r.user.username = "익명" + str(r.user_id)
            recomment_data2.append(
                {
                    "id": r.user_id,
                    "userName": r.user.username,
                    "content": r.body,
                    "commentPk":t.pk,
                    "recommentPk": r.pk,
                    "updated_at": r.updated_at,
                    "unname": r.unname,
                }
            )
    context = {
        "comment_data": comment_data,
        "recomment_data2": recomment_data2,
        "comment_data_count": len(comment_data),
        "articles_pk": articles_pk,
        "user": user,
    }
    return JsonResponse(context)
@login_required
def like(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    if request.user not in articles.like_users.all():
        articles.like_users.add(request.user)
        is_like = True
    else:
        articles.like_users.remove(request.user)
        is_like = False

    data = {
        "isLike": is_like,
        "likeCount": articles.like_users.count(),
    }
    return JsonResponse(data)


@login_required
def search(request):
    all_data = Articles.objects.order_by("-pk")
    search = request.GET.get("search", "")
    page = request.GET.get("page", "1")  # 페이지
    paginator = Paginator(all_data, 5)
    page_obj = paginator.get_page(page)
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
        message_count = len(new_message)
    if search:
        search_list = all_data.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(user_id__nickname__icontains=search)
            | Q(category__icontains=search)
        )
        paginator = Paginator(search_list, 5)  # 페이지당 10개씩 보여주기
        page_obj = paginator.get_page(page)
        context = {
            "search": search,
            "search_list": search_list,
            "question_list": page_obj,
            "count":message_count,
        }
    else:
        context = {
            "search": search,
            "search_list": all_data,
            "question_list": page_obj,
            "count":message_count,
        }

    return render(request, "articles/search.html", context)
