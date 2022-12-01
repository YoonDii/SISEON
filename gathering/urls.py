from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "gathering"

urlpatterns = [
    # # 모임게시판
    path("", views.GatheringListView.as_view(), name="gathering-list"),
    path(
        "<int:gathering_id>/",
        views.GatheringDetailView.as_view(),
        name="gathering-detail",
    ),
    path("create/", views.GatheringCreateView.as_view(), name="gathering-create"),
    path(
        "<int:gathering_id>/update/",
        views.GatheringUpdateView.as_view(),
        name="gathering-update",
    ),
    path("meeting_offline/", views.meeting_offline, name="meeting_offline"),
    # path('<int:gathering_id>/delete', views.GatheringDeleteView.as_view(), name='gathering-delete'),
    # 투표
    # path('<int:gathering_id>/create', views.PollCreateView.as_view(), name='poll-create'),
    path("<int:gathering_id>/create", views.poll_add, name="poll-create"),
    # # 댓글
    # path('<int:gathering_id>/comments/create', views.CommentCreateView.as_view(), name='comment-create'),
]
