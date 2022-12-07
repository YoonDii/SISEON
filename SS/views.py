from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from free.models import Free
from articles.models import Articles
from notices.models import Notices
from gathering.models import Gatherings
from accounts.models import User


def main(request):
    return render(request, "main.html")


@login_required
def search(request):
    free = Free.objects.order_by("pk")
    articles = Articles.objects.order_by("pk")
    notices = Notices.objects.order_by("-pk")
    gatherings = Gatherings.objects.order_by("-pk")
    search = request.GET.get("search", "")
    all_data2 = []
    if search:
        search_list1 = free.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )
        search_list2 = articles.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(category__icontains=search)
            | Q(user_id__nickname__icontains=search)
        )
        search_list3 = gatherings.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(category__icontains=search)
            | Q(user_id__nickname__icontains=search)
        )
        search_list4 = notices.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(user_id__username__icontains=search)
        )
        if search_list1:
            all_data2.extend(search_list1)
        if search_list2:
            all_data2.extend(search_list2)
        if search_list3:
            all_data2.extend(search_list3)
        if search_list4:
            all_data2.extend(search_list4)
        page = request.GET.get("page", "1")  # 페이지
        paginator = Paginator(all_data2, 5)
        page_obj = paginator.get_page(page)
        context = {
            "search": search,
            "search_list": all_data2,
            "question_list": page_obj,
        }
    else:
        page = request.GET.get("page", "1")  # 페이지
        paginator = Paginator(all_data2, 5)
        page_obj = paginator.get_page(page)
        context = {
            "search": search,
            "search_list": all_data2,
            "question_list": page_obj,
        }
    return render(request, "search.html", context)
