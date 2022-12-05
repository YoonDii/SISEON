from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from mdeditor.fields import MDTextField

# Create your models here.


class Articles(models.Model):
    check = models.BooleanField(default=False)
    title = models.CharField(max_length=50, verbose_name="Title")
    category_position = [
        ("질문유형을 선택해 주세요.", "질문유형을 선택해 주세요."),
        ("CS", "CS"),
        ("알고리즘", "알고리즘"),
        ("진로", "진로"),
        ("오류", "오류"),
        ("기타", "기타"),
    ]
    category = models.CharField(
        max_length=50, choices=category_position, default="질문유형을 선택해 주세요."
    )
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = MDTextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_articles"
    )
    unname = models.BooleanField(default=False)
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")


class Photo(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)


class Comment(models.Model):
    content = models.TextField()
    articles = models.ForeignKey(
        Articles, on_delete=models.CASCADE, related_name="comment_user"
    )
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    unname = models.BooleanField(default=False)
