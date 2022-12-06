from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from SS.settings import AUTH_USER_MODEL

# Create your models here.


class User(AbstractUser):
    nickname = models.CharField(max_length=20)
    github_id = models.CharField(max_length=50, blank=True)
    profile_url = models.CharField(max_length=50, blank=True)
    image = ProcessedImageField(
        upload_to="media/",
        blank=True,
        processors=[ResizeToFill(100, 100)],
        format="JPEG",
        options={"quality": 80},
    )
    is_social_account = models.BooleanField(default=False)
    social_id = models.CharField(null=True, blank=True, max_length=100)
    token = models.CharField(max_length=150, null=True, blank=True)
    service_name = models.CharField(null=True, max_length=20)
    social_profile_picture = models.CharField(null=True, blank=True, max_length=150)
    introduce = models.CharField(max_length=50, blank=True)
    notice = models.BooleanField(default=False)
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )


class Notification(models.Model):
    message = models.CharField(max_length=100)
    check = models.BooleanField(default=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=10)
    nid = models.IntegerField(default=0)
