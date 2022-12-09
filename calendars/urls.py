from django.conf.urls import url
from . import views

app_name = 'calendars'
urlpatterns = [
    url(r'^calendar/$', views.CalendarView.as_view(), name='index'),
    url(r'^event/new/$', views.event_new, name='event_new'),
    url(r'^event/detail/(?P<event_id>\d+)/$', views.event_detail, name='event_detail'),
	url(r'^event/edit/(?P<event_id>\d+)/$', views.event_edit, name='event_edit'),
	url(r'^event/delete/(?P<event_id>\d+)/$', views.event_delete, name='event_delete'),
]
