from django.urls import path
from django.views.generic import TemplateView 
from . import views

app_name = "gathering"

urlpatterns = [
    # # # 모임게시판
    # path('', views.GatheringListView.as_view(), name='gathering-list'),
    # path('<int:gathering_id>/',views.GatheringDetailView.as_view(), name='gathering-detail'),
    # path('create/', views.GatheringCreateView.as_view(), name='gathering-create'),
    # path('<int:gathering_id>/update/', views.GatheringUpdateView.as_view(), name='gathering-update'),
    # # path('<int:gathering_id>/delete', views.GatheringDeleteView.as_view(), name='gathering-delete'),
    # # 투표
    # path('<int:gathering_id>/create', views.PollCreateView.as_view(), name='poll-create'),

    # # path('<int:gathering_id>/create', views.poll_add, name='poll-create'),
    # # # 댓글
    # # path('<int:gathering_id>/comments/create', views.CommentCreateView.as_view(), name='comment-create'),
    path('list/', views.polls_list, name='gathering-list'),
    path('list/user/', views.list_by_user, name='list_by_user'),
    path('add/', views.polls_add, name='add'),
    path('edit/<int:poll_id>/', views.polls_edit, name='edit'),
    path('delete/<int:poll_id>/', views.polls_delete, name='delete_poll'),
    path('end/<int:poll_id>/', views.endpoll, name='end_poll'),
    path('edit/<int:poll_id>/choice/add/', views.add_choice, name='add_choice'),
    path('edit/choice/<int:choice_id>/', views.choice_edit, name='choice_edit'),
    path('delete/choice/<int:choice_id>/',
         views.choice_delete, name='choice_delete'),
    path('<int:poll_id>/', views.poll_detail, name='detail'),
    path('<int:poll_id>/vote/', views.poll_vote, name='vote'),

    # 댓글
    # 댓글
    path("<int:poll_id>/comments/", views.comment_create, name="comment_create"),
    path(
        "<int:poll_id>/comments/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path(
        "<int:poll_id>/comments/<int:comment_pk>/update/",
        views.comment_update,
        name="comment_update",
    ),
    path(
        "<int:poll_id>/comments/<int:comment_pk>/update/complete/",
        views.comment_update_complete,
        name="comment_update_complete",
    ),
    path("<int:poll_id>/like/", views.like, name="like"),

    path('<int:gathering_id>/create', views.poll_add, name='poll-create'),
    path('meeting_offline/', views.meeting_offline, name='meeting_offline'),
    # # 댓글
    # path('<int:gathering_id>/comments/create', views.CommentCreateView.as_view(), name='comment-create'),

]
