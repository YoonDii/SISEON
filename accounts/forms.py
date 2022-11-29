from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from django import forms


class CreateUser(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "nickname",
            "password1",
            "password2",
            "email",
            "image",
        ]

    labels = {
        "username": "로그인 아이디",
        "nickname": "닉네임",
        "password1": "비밀번호",
        "password2": "비밀번호 확인",
        "email": "이메일 ",
        "image": "프로필 이미지",
    }


class CustomUserChangeForm(UserChangeForm):
    # password = None

    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "nickname",
            "github_id",
            "profile_url",
            "introduce",
            "image",
        ]
        labels = {
            "email": "이메일 ",
            "nickname": "닉네임",
            "github_id": "깃허브아이디",
            "profile_url": "깃허브주소",
            "introduce": "한마디",
            "image": "프로필 이미지",
        }
