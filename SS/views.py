from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from free.models import Free
from articles.models import Articles
from notices.models import Notices
from gathering.models import Gatherings


def main(request):
    return render(request, "main.html")


def search(request):

    return render(request, "search.html")


# @login_required
# def search(request):
#     free = Free.objects.order_by("-pk")
#     articles = Articles.objects.order_by("-pk")
#     notices = Notices.objects.order_by("-pk")
#     gatherings = Gatherings.objects.order_by("-pk")
#     search = request.GET.get("search", "")
#     frees = []
#     all_data = []
#     search_list = free.filter(Q(title__icontains=search) | Q(content__icontains=search))
#     print(search)
#     if search_list:
#         for i in search_list:
#              = { }

#     return render(request, "search.html")
