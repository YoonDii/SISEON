from django.urls import path
from . import views

app_name = "gathering"

urlpatterns = [
    # # 모임게시판
    path('', views.GatheringListView.as_view(), name='gathering-list'),
    path('<int:gathering_id>/',views.GatheringDetailView.as_view(), name='gathering-detail'),
    path('meeting_offline/', views.meeting_offline, name="meeting_offline"),
    # path('create/', views.GatheringCreateView.as_view(), name='gathering-create'),
    # path('<int:gathering_id>/update/', views.GatheringUpdateView.as_view(), name='gathering-update'),
    # path('<int:gathering_id>/delete', views.GatheringDeleteView.as_view(), name='gathering-delete'),
    # # 투표

    # # 댓글
    # path('<int:gathering_id>/comments/create', views.CommentCreateView.as_view(), name='comment-create'),
]
