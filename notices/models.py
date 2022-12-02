from django.db import models
from django.conf import settings

# Create your models here.
class Notices(models.Model):
    title = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=1000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)


class Photo(models.Model):
    notice = models.ForeignKey(Notices, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", blank=True)