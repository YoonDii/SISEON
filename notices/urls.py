from django.urls import path
from . import views

app_name = "notices"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:notices_pk>/", views.detail, name="detail"),
    path("<int:notices_pk>/update/", views.update, name="update"),
    path("<int:notices_pk>/delete/", views.delete, name="delete"),
]
