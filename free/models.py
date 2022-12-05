from django.db import models
from django.conf import settings


# Create your models here.


class Free(models.Model):
    check = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    like_free = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_free"
    )
    hits = models.PositiveIntegerField(default=0, verbose_name="조회수")


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
