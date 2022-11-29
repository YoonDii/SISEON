from django.db import models
from SS.settings import AUTH_USER_MODEL
# Create your models here.

class Gathering(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    OfflineMoim = "오프라인 모임"
    OnlineMoim = "온라인 모임"
    OfflineStudy = "오프라인 스터디"
    OnlineStudy = "온라인 스터디"
    CATEGORIES = [
        (OfflineMoim,'오프라인 모임'),
        (OnlineMoim,'온라인 모임'),
        (OfflineStudy,'오프라인 스터디'),
        (OnlineStudy,'온라인 스터디'),
    ]

    category = models.CharField(choices=CATEGORIES, max_length=10, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(AUTH_USER_MODEL, related_name="like_gathering")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, verbose_name="조회수")
    image = models.ImageField(upload_to=None, blank=True)
    

class GatheringComment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    gathering = models.ForeignKey(Gathering, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Vote(models.Model):
    expiration = models.DateTimeField()
    gathering = models.ForeignKey(Gathering, on_delete=models.CASCADE)

class VoteContent(models.Model):
    content = models.CharField(max_length=100)
    user = models.ManyToManyField(AUTH_USER_MODEL, related_name="vote_user")
    