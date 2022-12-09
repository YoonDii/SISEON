from django.db import models
from django.conf import settings
from mdeditor.fields import MDTextField

# Create your models here.


class Free(models.Model):
    check = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = MDTextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    like_free = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_free"
    )
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")
    q = models.CharField(max_length=5, default="자유")


class Photo(models.Model):
    free = models.ForeignKey(Free, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)


class Comment(models.Model):
    content = models.TextField()
    free = models.ForeignKey(Free, on_delete=models.CASCADE, related_name="free_user")
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="free_com_user"
    )
    unname = models.BooleanField(default=True)


class ReComment1(models.Model):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="free_comment_user"
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField("답글", max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    unname = models.BooleanField(default=True)
