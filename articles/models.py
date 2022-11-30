from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.


class Articles(models.Model):
    title = models.CharField(max_length=50)
    category_position = [
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
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_articles"
    )
    unname = models.BooleanField(default=False)

class Photo(models.Model):
    article = models.ForeignKey(Articles, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)

class Comment(models.Model):
    content = models.TextField()
    articles = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="comment_user")
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)