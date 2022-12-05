from django.urls import path
from . import views

app_name = "free"

urlpatterns = [
    # 자유게시글
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:free_pk>/", views.detail, name="detail"),
    path("<int:free_pk>/update/", views.update, name="update"),
    path("<int:free_pk>/delete/", views.delete, name="delete"),
    path("fail/", views.fail, name="fail"),
    # 댓글
    path("<int:free_pk>/comments_create/", views.comment_create, name="comment_create"),
    path("<int:free_pk>/comment_delete/<int:comment_pk>/delete/",views.comment_delete,name="comment_delete"),
    path("<int:free_pk>/comment_update/<int:comment_pk>/update/",views.comment_update,name="comment_update"),
    path('<int:free_pk>/recomments_create',views.recomments_create, name='recomments_create'),
    path('<int:free_pk>/detail/<int:comment_pk>/delete/<int:recomment_pk>', views.recomments_delete, name="recomments_delete"),
    path("<int:free_pk>/like/", views.like, name="like"),
    path("search/", views.search, name="search"),
]
