from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from django.contrib.auth import get_user_model, login as my_login, logout as my_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import *
from gathering.models import *
from articles.models import Comment as Comment1, Articles
from free.models import Comment as Comment2, Free
from notes.models import Notes
from django.db.models import Q
from .models import User
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage
from .forms import *
from notes.forms import *
import os, requests

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
    # print(request)
    # if request.method == "POST":
    #     form = CreateUser(request.POST, request.FILES)
    #     print(1)
    #     if form.is_valid():
    #         user = form.save()
    #         my_login(request, user)
    #         print(2)
    #         return redirect("accounts:index")
    #     else:
    #         messages.warning(request, "이미 존재하는 ID입니다.")

    # else:
    #     form = CreateUser()
    #     print(3)
    # context = {
    #     "form": form,
    # }
    # print(form.errors)

    # return render(request, "accounts/signup.html", context)
    if request.method == "POST":
        signup_form = CreateUser(request.POST, request.FILES)
        sns_signup_form = SNSUserSignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            print(request.POST)
            # 소셜 서비스 구분
            user.social_id = (
                request.POST["social_id"] if "social_id" in request.POST else None
            )
            user.service_name = (
                request.POST["service_name"] if "service_name" in request.POST else None
            )
            user.is_social_account = (
                True if "is_social_account" in request.POST else False
            )
            user.social_profile_picture = (
                request.POST["social_profile_picture"]
                if "social_profile_picture" in request.POST
                else None
            )
            user.profile_url = (
                request.POST["profile_url"]
                if "profile_url" in request.POST
                else None
            )
            user.introduce = (
                request.POST["introduce"]
                if "introduce" in request.POST
                else None
            )
            user.github_id = (
                request.POST["github_id"]
                if "github_id" in request.POST
                else None
            )
            # 유저 토큰
            user.token = request.POST["token"] if "token" in request.POST else None
            user.save()
            my_login(request, user)
            if user.is_social_account:
                return redirect("main")
            else:
                return redirect("main")
    else:
        signup_form = CreateUser()
    context = {
        "form": signup_form,
    }
    return render(request, "accounts/signup.html", context)


# 회원탈퇴
def delete(request, pk):
    user = get_user_model().objects.get(pk=pk)
    if request.user == user:
        user.delete()
    return redirect("main")


# 로그인
def login(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
        message_count = len(new_message)
    else:
        message_count = 0
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        print(1)
        if form.is_valid():
            my_login(request, form.get_user())
            print(2)
            return redirect(request.GET.get("next") or "main")
        else:
            print(3)
            form = LoginForm()
            context = {"form": form,"count":message_count}
            return render(request, "accounts/login.html", context)
    else:
        form = LoginForm()
        
    context = {"form": form, "count":0,}
    return render(request, "accounts/login.html", context)


# 로그아웃
@login_required
def logout(request):
    my_logout(request)
    return redirect("accounts:login")

@login_required
def message_delete(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    print(note.to_user)
    if request.user == note.to_user and request.method == "POST":
        note.delete()
        return JsonResponse({"pk": pk})
    else:
        return redirect("accounts:detail", request.user.pk)
@login_required
def send(request, pk):
    to_user = get_object_or_404(get_user_model(), pk=pk)
    form = NotesForm(request.POST or None)
    # print(to_user, to_user.username, to_user.pk, pk, request.user)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.from_user = request.user
        temp.to_user = to_user
        temp.save()
        print(request.user, to_user, 99999)
        message = f"{request.user}님이 {to_user}님에게 쪽지를 보냈습니다."
        Notification.objects.create(
            user=to_user, message=message, category="쪽지", nid=temp.id
        )
        return redirect("accounts:detail", request.user.pk)
    context = {
        "form": form,
        "to_user": to_user,
    }
    return redirect("accounts:detail", request.user.pk)
# 디테일
@login_required
def detail(request, pk):
    user = get_user_model().objects.get(pk=pk)
    comments1 = Comment1.objects.filter(user_id=pk).order_by("-pk")  # 질문게시판 댓글
    articles = Articles.objects.filter(user_id=pk).order_by("-pk")  # 질문게시판 글

    comments2 = Comment2.objects.filter(user_id=pk).order_by("-pk")  # 자유게시판 댓글
    frees = Free.objects.filter(user_id=pk).order_by("-pk")  # 자유게시판 글

    comments3 = GatheringsComment.objects.filter(user_id=pk).order_by("-pk") # 모임게시판 댓글
    gatherings = Gatherings.objects.filter(user_id=pk).order_by("-pk") # 모임게시판 글
    
    notes = Notes.objects.filter(Q(from_user_id = request.user.pk) | Q(to_user_id = request.user.pk)) # 받은쪽지, 보낸쪽지
    form = NotesForm(request.POST or None)
    if form.is_valid():
        
        temp = form.save(commit=False)
        temp.from_user = request.user
        temp.to_user = user
        temp.save()
        message = f"{request.user}님이 {user}님에게 쪽지를 보냈습니다."
        Notification.objects.create(
            user=user, message=message, category="쪽지", nid=temp.id
        )
        return redirect("accounts:detail", request.user.pk)
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
            "comments3":comments3,
            "gatherings":gatherings,
            "notes":notes,
            "form": form,
        }
    else:
        context = {
            "user": user,
            "form": form,
        }
    return render(request, "accounts/detail.html", context)


# 프로필 수정
@login_required
def edit_profile(request, pk):
    user = User.objects.get(pk=pk)
    new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
    message_count = len(new_message)
    if request.user == user:
        if request.method == "POST":
            form = CustomUserChangeForm(
                request.POST, request.FILES, instance=request.user
            )
            if form.is_valid():
                form.save()
                return redirect("accounts:detail", user.pk)
        else:
            form = CustomUserChangeForm(instance=request.user)
        context = {
            "form": form,
            "count":message_count,
        }
        return render(request, "accounts/edit_profile.html", context)
    else:
        return redirect("accounts:index")


@login_required
def change_password(request, pk):
    user = get_user_model().objects.get(pk=pk)
    new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
    message_count = len(new_message)
    if request.user == user:
        if request.method == "POST":
            form = CustomPasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                
                return redirect("accounts:edit_profile", user.pk)
        else:
            form = CustomPasswordChangeForm(request.user)

        context = {
            "form": form,
            "count":message_count,
        }

        return render(request, "accounts/change_password.html", context)
    else:
        return render(request, "accounts/index.html")


@login_required
def message(request, pk):
    noti = Notification.objects.get(pk=pk)
    noti.check = True
    noti.save()
    id = noti.nid
    if noti.category == "자유":
        if Free.objects.filter(id=id).exists():
            return redirect("free:detail", id)
        else:
            return redirect("free:fail")
    elif noti.category == "질문":
        if Articles.objects.filter(id=id).exists():
            return redirect("articles:detail", id)
        else:
            return redirect("articles:fail")
    elif noti.category == "모임":
        if Gatherings.objects.filter(id=id).exists():
            return redirect("gathering:gathering-detail", id)
        else:
            return redirect("gathering:fail")
    elif noti.category == "쪽지":
        if Notes.objects.filter(id=id).exists():
            return redirect("accounts:detail", request.user.pk)
        else:
            return redirect("notes:fail")


@login_required
def follow(request, pk):
    if request.user.is_authenticated:
        user = get_user_model().objects.get(pk=pk)
        if request.user != user:
            if user.followers.filter(pk=request.user.pk).exists():
                user.followers.remove(request.user)
                is_followed = False
                # 상대방이 나를 팔로우
            else:
                user.followers.add(request.user)
                is_followed = True
                # 상대방이 나를 팔로우
            followers = user.followers.all()
            f_datas = []
            for follower in followers:
                f_datas.append(
                    {
                        "follower_pk": follower.pk,
                        "follower_img": str(follower.image),
                        "follower_name": follower.username,
                    }
                )
            data = {
                "is_followed": is_followed,
                "followers_count": user.followers.count(),
                "followings_count": user.followings.count(),
                "f_datas": f_datas,
            }
            return JsonResponse(data)
        return redirect("accounts:detail", user.username)
    return redirect("accounts:login")

def social_signup_request(request):
    if "github" in request.path:
        service_name = "github"
    services = {
        "github": {
            "base_url": "https://github.com/login/oauth/authorize",
            "client_id": "addba30b16251115a79c",
            "redirect_uri": "http://127.0.0.1:8000/accounts/login/github/callback",
            "scope": "read:user",
        },
    }
    for k, v in services[service_name].items():
        if k == "base_url":
            res = f"{v}?"
        else:
            res += f"{k}={v}&"
    return redirect(res)


def social_signup_callback(request):
    if "github" in request.path:
        service_name = "github"
    services = {
        "github": {
            "data": {
                "redirect_uri": "http://127.0.0.1:8000/accounts/login/github/callback",
                "client_id": "addba30b16251115a79c",
                "client_secret": "60e071cf669b351b3cad4bffe929bd79eaf5476b",
                "code": request.GET.get("code"),
            },
            "api": "https://github.com/login/oauth/access_token",
            "user_api": "https://api.github.com/user",
        },
    }
    if service_name == "github":
        headers = {
            "accept": "application/json",
        }
        token = requests.post(
            services[service_name]["api"],
            data=services[service_name]["data"],
            headers=headers,
        ).json()
    # ================================== 액세스 토큰 발급 ==================================
    access_token = token["access_token"]
    print(access_token, 555)
    # ================================== 액세스 토큰 발급 ==================================
    payload = {
        "github": {"Authorization": f"token {access_token}"},
    }
    if service_name == "github":
        headers = payload[service_name]
        u_info = requests.get(
            services[service_name]["user_api"], headers=headers
        ).json()
    # print(
    #     u_info, 111111111111111111111111111111111111111111111111111111111111111111111111
    # )
    if service_name == "github":
        login_data = {
            "github": {
                "social_id": u_info["id"],
                "username": u_info["login"],
                "social_profile_picture": u_info["avatar_url"],
                "nickname": u_info["login"],
                "email": u_info["email"],
                "html_url":u_info["html_url"],
                "bio":u_info["bio"],
                "github_id":u_info["login"],
                ### 깃허브에서만 가져오는 항목 ###
                "git_username": u_info["login"],
                ### 깃허브에서만 가져오는 항목 ###
            },
        }
    user_info = login_data[service_name]
    # print(
    #     user_info,
    #     222222222222222222222222222222222222222222222222222222222222222222222222,
    # )
    if get_user_model().objects.filter(social_id=user_info["social_id"]).exists():
        user = get_user_model().objects.get(social_id=user_info["social_id"])
        my_login(request, user)
        return redirect(request.GET.get("next") or "main")
    else:
        social_data = {
            # 소셜 서비스 구분
            "social_profile_picture": user_info["social_profile_picture"],
            "social_id": str(user_info["social_id"]),
            "service_name": service_name,
            "is_social_account": True,
            "profile_url":user_info["html_url"],
            "introduce":user_info["bio"],
            "github_id":user_info["nickname"],
            # 유저 토큰 가져오기
            "token": access_token,
        }
        data = {
            # 일반 정보
            "username": user_info["git_username"],
            "nickname": user_info["nickname"],
            "email": user_info["email"],
            "profile_url":user_info["html_url"],
            "introduce":user_info["bio"],
            # 깃허브에서만 가져오는 항목
            "git_username": (u_info["login"] if service_name == "github" else None),
        }
        signup_form = CreateUser(initial=data)
        sns_signup_form = SNSUserSignupForm(initial=social_data)
        context = {
            "form": signup_form,
            "sns_signup_form": sns_signup_form,
        }
    return render(request, "accounts/signup.html", context)
