from django.shortcuts import render, redirect, get_object_or_404
from .models import Articles, Comment, Photo
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ArticlesForm, CommentForm, PhotoForm
from accounts.models import User, Notification
from django.db.models import Count
from django.db.models import Q

# Create your views here.


def index(request):
    articles = Articles.objects.order_by("-pk")  # 최신순으로나타내기
    context = {"articles": articles}
    return render(request, "articles/index.html", context)


@login_required
def create(request):
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
        "form": form,
        "photo_form": photo_form,
    }
    return render(request, "articles/create.html", context)


@login_required
def detail(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    comments = Comment.objects.filter(articles_id=articles_pk).order_by("-pk")
    comment_form = CommentForm()
    photos = articles.photo_set.all()
    for i in comments:  # 시간바꾸는로직
        i.updated_at = i.updated_at.strftime("%y-%m-%d")
    context = {"articles": articles, "comment_form": comment_form, "comments": comments, "photos":photos,}

    return render(request, "articles/detail.html", context)


def update(request, articles_pk):
    article = Articles.objects.get(pk=articles_pk)
    if request.user == article.user:
        photos = article.photo_set.all()
        instancetitle = article.title
        if request.method == "POST":
            articles_form = ArticlesForm(request.POST, request.FILES, instance=article)
            if photos:
                photo_form = PhotoForm(request.POST, request.FILES, instance=photos[0])
            else:
                photo_form = PhotoForm(request.POST, request.FILES)
            images = request.FILES.getlist("image")
            for photo in photos:
                if photo.image:
                    photo.delete()
            if articles_form.is_valid() and photo_form.is_valid():
                article = articles_form.save(commit=False)
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
            articles_form = ArticlesForm(instance=article)
            if photos:
                photo_form = PhotoForm(instance=photos[0])
            else:
                photo_form = PhotoForm()
        if request.user.is_authenticated:
            new_message = Notification.objects.filter(
                Q(user=request.user) & Q(check=False)
            )
            message_count = len(new_message)
            context = {
                "count": message_count,
                "articles_form": articles_form,
                "photo_form": photo_form,
                "instancetitle": instancetitle,
                "article": article,
            }
        else:
            context = {
                "articles_form": articles_form,
                "photo_form": photo_form,
                "instancetitle": instancetitle,
                "article": article,
            }
        return render(request, "articles/update.html", context)
    else:
        return redirect("articles:index")


def delete(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    articles.delete()
    return redirect("articles:index")


@login_required
def comment_create(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.articles = articles
        comment.user = request.user
        comment.save()
    return redirect("articles:detail", articles.pk)


def comment_delete(request, comment_pk, articles_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect("articles:detail", articles_pk)


def comment_update(request, articles_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)

    data = {"comment_content": comment.content}

    return JsonResponse(data)


def comment_update_complete(request, articles_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
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
def like(request, articles_pk):
    articles = get_object_or_404(articles, pk=articles_pk)
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
