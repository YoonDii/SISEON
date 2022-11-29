from django.urls import path
from . import views

app_name = "free"

urlpatterns = [
    # 자유게시글
    path("", views.index, name="index"),
]
