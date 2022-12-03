from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, login as my_login, logout as my_logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from accounts.models import User
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserChangeForm, CreateUser
from django.contrib.auth.decorators import login_required
from accounts.models import Notification
from articles.models import Comment as Comment1, Articles
from free.models import Comment as Comment2, Free
from .models import User, Notification
from django.db.models import Q

# Create your views here.

# 임시메인
def index(request):
    context = {
        "datas": get_user_model().objects.all(),
        "user": request.user,
    }
    return render(request, "accounts/index.html", context)


# 회원가입
def signup(request):
    if request.method == "POST":
        form = CreateUser(request.POST, request.FILES)
        print(1)
        if form.is_valid():
            user = form.save()
            my_login(request, user)
            print(2)
            return redirect("accounts:index")
        else:
            messages.warning(request, "이미 존재하는 ID입니다.")

    else:
        form = CreateUser()
        print(3)
    context = {
        "form": form,
    }
    print(form.errors)

    return render(request, "accounts/signup.html", context)


# 회원탈퇴
def delete(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        user.delete()
    return redirect("accounts:index")


# 로그인
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print(1)
        if form.is_valid():
            my_login(request, form.get_user())
            return redirect(request.GET.get("next") or "accounts:index")
        else:
            form = AuthenticationForm()
            messages.warning(request, "ID가 존재하지 않거나 암호가 일치하지 않습니다.")
            context = {"form": form}
            return render(request, "accounts/login.html", context)
    else:
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)


# 로그아웃
@login_required
def logout(request):
    my_logout(request)
    return redirect("accounts:index")


# 디테일
@login_required
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    comments1 = Comment1.objects.filter(user_id=pk)  # 질문게시판 댓글
    articles = Articles.objects.filter(user_id=pk)  # 질문게시판 글

    comments2 = Comment2.objects.filter(user_id=pk)  # 자유게시판 댓글
    frees = Free.objects.filter(user_id=pk)  # 자유게시판 글
    if request.user.is_authenticated:
        new_message = Notification.objects.filter(

            Q(user_id=user.pk) & Q(check=False)

        )  # 알람있는지없는지 파악
        message_count = len(new_message)
        context = {
            "count": message_count,
            "user": user,
            "followers": user.followers.all(),
            "followings": user.followings.all(),
            "comments1": comments1,
            "articles": articles,
            "comments2": comments2,
            "frees": frees,
        }
    else:
        context = {
            "user": user,
        }
    return render(request, "accounts/detail.html", context)


# 프로필 수정
@login_required
def edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = CustomUserChangeForm(
                request.POST, request.FILES, instance=request.user
            )
            print(2)
            if form.is_valid():
                print(1)
                form.save()
                return redirect("accounts:detail", user.pk)
        else:
            form = CustomUserChangeForm(instance=request.user)
        context = {
            "form": form,
        }
        return render(request, "accounts/edit_profile.html", context)
    else:
        return redirect("accounts:index")


@login_required
def change_password(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        if request.method == "POST":
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, "Your password was successfully updated!")
                return redirect("accounts:edit_profile", user.pk)
            else:
                messages.error(request, "Please correct the error below.")
        else:
            form = PasswordChangeForm(request.user)

        context = {
            "form": form,
        }

        return render(request, "accounts/change_password.html", context)
    else:
        return render(request, "accounts/index.html")


def message(request, pk):
    noti = Notification.objects.get(pk=pk)
    noti.check = True
    noti.save()
    id = noti.nid
    if noti.category == "자유":
        print("자유", 1)
        return redirect("free:detail", id)
    elif noti.category == "질문":
        print("질문", 2)
        return redirect("articles:detail", id)
    elif noti.category == "모임":
        print("모임", 3)
        return redirect("gathering:detail", id)


@login_required
def follow(request, pk):
    user = get_user_model().objects.get(pk=pk)

    if request.user != user:
        if request.user not in user.followers.all():
            user.followers.add(request.user)
            is_following = True
        else:
            user.followers.remove(request.user)
            is_following = False

    data = {
        "isFollowing": is_following,
        "followers": user.followers.all().count(),
        "followings": user.followings.all().count(),
    }

    return JsonResponse(data)
