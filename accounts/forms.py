from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from django import forms


class CreateUser(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'password1',
            'password2',
            'email',
            'first_name',
            'last_name',
            'image',
            "profile_url",
            "github_id",
            "introduce",
    ]

    labels = {
      'username' : '로그인 아이디',
      'password1' : '비밀번호',
      'password2' : '비밀번호 확인',
      'email' : '이메일 ',
      'first_name' : '이름',
      'last_name' : '성',
      "github_id":"깃허브아이디",
      'image' : '프로필 이미지',
      "profile_url":"깃허브 주소",
      "introduce":"introduce",
    }


class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = get_user_model()
        fields = [
            "email",
            "first_name",
            "last_name",
            "image",
            "github_id",
            "profile_url",
            "introduce",
        ]
        labels = {
            'email' : '이메일 ',
            'first_name' : '이름',
            'last_name' : '성',
            'image' : '프로필 이미지',
            "github_id":"깃허브아이디",
            "profile_url":"깃허브 주소",
            "introduce":"introduce",
            }