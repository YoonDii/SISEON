from django.shortcuts import render, redirect, get_object_or_404
from .models import Free, Comment, Photo
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import FreeForm, CommentForm, PhotoForm
from accounts.models import User, Notification
from django.db.models import Count
from django.db.models import Q

# Create your views here.


def index(request):
    frees = Free.objects.order_by("-pk")  # 최신순으로나타내기
    context = {"frees": frees}
    return render(request, "free/index.html", context)


@login_required
def create(request):
    if request.method == "POST":
        form = FreeForm(request.POST, request.FILES)
        photo_form = PhotoForm(request.POST, request.FILES)
        images = request.FILES.getlist("image")
        if form.is_valid() and photo_form.is_valid():
            free = form.save(commit=False)
            free.user = request.user
            if len(images):
                for image in images:
                    image_instance = Photo(free=free, image=image)
                    free.save()
                    image_instance.save()
            else:
                free.save()
            return redirect("free:index")
    else:
        form = FreeForm()
        photo_form = PhotoForm()

    context = {
        "form": form,
        "photo_form": photo_form,
    }
    return render(request, "free/create.html", context)


@login_required
def detail(request, free_pk):
    free = Free.objects.get(pk=free_pk)
    comments = Comment.objects.filter(free_id=free_pk).order_by("-pk")
    comment_form = CommentForm()
    photos = free.photo_set.all()
    for i in comments:  # 시간바꾸는로직
        i.updated_at = i.updated_at.strftime("%y-%m-%d")
    context = {
        "free": free,
        "comment_form": comment_form,
        "comments": comments,
        "photos": photos,
    }

    return render(request, "free/detail.html", context)


def update(request, free_pk):
    free = Free.objects.get(pk=free_pk)
    if request.user == free.user:
        photos = free.photo_set.all()
        instancetitle = free.title
        if request.method == "POST":
            free_form = FreeForm(request.POST, request.FILES, instance=free)
            if photos:
                photo_form = PhotoForm(request.POST, request.FILES, instance=photos[0])
            else:
                photo_form = PhotoForm(request.POST, request.FILES)
            images = request.FILES.getlist("image")
            for photo in photos:
                if photo.image:
                    photo.delete()
            if free_form.is_valid() and photo_form.is_valid():
                free = free_form.save(commit=False)
                free.user = request.user
                if len(images):
                    for image in images:
                        image_instance = Photo(free=free, image=image)
                        free.save()
                        image_instance.save()
                else:
                    free.save()
                return redirect("free:detail", free.pk)
        else:
            free_form = FreeForm(instance=free)
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
                "free_form": free_form,
                "photo_form": photo_form,
                "instancetitle": instancetitle,
                "free": free,
            }
        else:
            context = {
                "free_form": free_form,
                "photo_form": photo_form,
                "instancetitle": instancetitle,
                "free": free,
            }
        return render(request, "free/update.html", context)
    else:
        return redirect("free:index")


def delete(request, free_pk):
    free = free.objects.get(pk=free_pk)
    free.delete()
    return redirect("free:index")


@login_required
def comment_create(request, free_pk):
    free = Free.objects.get(pk=free_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.free = free
        comment.user = request.user
        comment.save()
    return redirect("free:detail", free.pk)


def comment_delete(request, fcomment_pk, free_pk):
    comment = Comment.objects.get(pk=fcomment_pk)
    comment.delete()
    return redirect("free:detail", free_pk)


def comment_update(request, free_pk, fcomment_pk):
    comment = Comment.objects.get(pk=fcomment_pk)

    data = {"comment_content": comment.content}

    return JsonResponse(data)


def comment_update_complete(request, free_pk, fcomment_pk):
    comment = Comment.objects.get(pk=fcomment_pk)
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
def like(request, free_pk):
    free = get_object_or_404(free, pk=free_pk)
    # 만약에 로그인한 유저가 이 글을 좋아요를 눌렀다면,
    # if free.like_free.filter(id=request.user.id).exists():
    if request.user in free.like_free.all():
        # 좋아요 삭제하고
        free.like_free.remove(request.user)

    else:
        # 좋아요 추가하고
        free.like_free.add(request.user)

    # 상세 페이지로 redirect

    data = {
        "like_cnt": free.like_free.count(),
    }

    return JsonResponse(data)
