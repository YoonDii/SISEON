from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    # 질문게시글
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:articles_pk>/", views.detail, name="detail"),
    path("<int:articles_pk>/update/", views.update, name="update"),
    path("<int:articles_pk>/delete/", views.delete, name="delete"),
    # 댓글
    path("<int:articles_pk>/comments/", views.comment_create, name="comment_create"),
    path(
        "<int:articles_pk>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path(
        "<int:articles_pk>/comments/<int:comment_pk>/update/",
        views.comment_update,
        name="comment_update",
    ),
    path(
        "<int:articles_pk>/comments/<int:comment_pk>/update/complete/",
        views.comment_update_complete,
        name="comment_update_complete",
    ),
    path("<int:articles_pk>/like/", views.like, name="like"),
]
