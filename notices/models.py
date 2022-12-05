from django.db import models
from django.conf import settings
from mdeditor.fields import MDTextField

# Create your models here.
class Notices(models.Model):
    check = models.BooleanField(default=False)
    title = models.CharField(max_length=50)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = MDTextField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notices_user"
    )
    image = models.ImageField(upload_to="images/", blank=True)
