from django.shortcuts import render
from accounts.models import User, Notification
from django.db.models import Count
from django.db.models import Q
# Create your views here.


def index(request):  # 일단 페이지만 뜨게
    if request.user.is_authenticated:
        new_message = Notification.objects.filter(Q(user=request.user) & Q(check=False))
        message_count = len(new_message)
        return render(request, "calendars/index.html", context = {"count": message_count})
    else:
        return render(request, "calendars/index.html")
