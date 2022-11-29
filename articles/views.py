from django.shortcuts import render, redirect, get_object_or_404
from .models import Articles, Comment
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ArticlesForm, CommentForm

# Create your views here.


def index(request):
    articles = Articles.objects.order_by("-pk")  # 최신순으로나타내기

    context = {"articles": articles}
    return render(request, "articles/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = ArticlesForm(request.POST, request.FILES)
        print(request.POST)
        print(form.is_valid)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            return redirect("articles:index")
    else:
        form = ArticlesForm()
    context = {
        "form": form,
    }

    return render(request, "articles/create.html", context)


@login_required
def detail(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    comment_form = CommentForm()
    context = {
        "articles": articles,
        "comment_form": comment_form,
        "comments": articles.comment_set.all(),
    }

    return render(request, "articles/detail.html", context)


def update(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    if request.method == "POST":
        articles_form = ArticlesForm(request.POST, request.FILES, instance=articles)
        if articles_form.is_valid():
            articles_form.save()
            return redirect("articles:detail", articles.pk)
    else:
        articles_form = ArticlesForm(instance=articles)
    context = {"articles_form": articles_form}

    return render(request, "articles/update.html", context)


def delete(request, articles_pk):
    articles = Articles.objects.get(pk=articles_pk)
    articles.delete()
    return redirect("articles:index")


@login_required
def comment_create(request, pk):
    articles = Articles.objects.get(pk=pk)
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
