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
    path("fail/", views.fail, name="fail"),
    # 댓글
    path("<int:articles_pk>/comment_create/", views.comment_create, name="comment_create"),
    path("<int:articles_pk>/comment_delete/<int:comment_pk>/delete/",views.comment_delete,name="comment_delete",),
    path("<int:articles_pk>/comment_update/<int:comment_pk>/update/",views.comment_update,name="comment_update",),
    path("<int:articles_pk>/recomment_create/<int:comment_pk>/", views.recomment_create, name='recomment_create'),
    path("<int:articles_pk>/recomment_delete/<int:comment_pk>/delete/<int:recomment_pk>/", views.recomment_delete, name="recomment_delete"),
    path("<int:articles_pk>/like/", views.like, name="like"),
    path("search/", views.search, name="search"),
]
