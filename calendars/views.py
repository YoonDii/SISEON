from django.shortcuts import render

# Create your views here.


def index(request):  # 일단 페이지만 뜨게
    return render(request, "calendars/index.html")
