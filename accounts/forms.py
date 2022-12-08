from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
    PasswordChangeForm,
)
from django.contrib.auth import get_user_model

from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=(""),
        widget=forms.TextInput(
            attrs={
                "placeholder": "ID",
            }
        ),
    )
    password = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
            }
        ),
    )


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
            "username": "ID",
            "nickname": "Nickname",
            "password1": "",
            "password2": "",
            "email": "Email",
            "image": "",
        }

    password1 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
            }
        ),
    )

    password2 = forms.CharField(
        label=(""),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password confirmation",
            }
        ),
    )


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
            "email": "Email",
            "nickname": "Nickname",
            "github_id": "GitHub ID",
            "profile_url": "GitHub address",
            "introduce": "Bio",
            "image": "Profile image",
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Old password",
            }
        ),
    )

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New password",
            }
        ),
    )

    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New password confirmation",
            }
        ),
    )


class SNSUserSignupForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
            "social_id",
            "service_name",
            "is_social_account",
            "token",
            "social_profile_picture",
            "profile_url",
            "introduce",
            "github_id",

        )
        widgets = {
            "social_id": forms.HiddenInput,
            "service_name": forms.HiddenInput,
            "is_social_account": forms.HiddenInput,
            "token": forms.HiddenInput,
            "social_profile_picture": forms.HiddenInput,
            "profile_url": forms.HiddenInput,
            "introduce": forms.HiddenInput,
            "github_id":forms.HiddenInput,
        }
