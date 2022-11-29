from django.shortcuts import render, redirect
from .models import Articles
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ArticlesForm

# Create your views here.


def index(request):
    articles = Articles.objects.order_by("-pk")  # 최신순으로나타내기
    all_articles = Articles.objects.all()
    context = {"articles": articles, "all_articles": all_articles}
    return render(request, "articles/index.html", context)


# @login_required
def create(request):
    if request.method == "POST":
        form = ArticlesForm(request.POST, request.FILES)
        print(request.POST)
        print(form.is_valid)
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            return redirect("articles:index")
    else:
        form = ArticlesForm()
    context = {
        "form": form,
    }

    return render(request, "articles/create.html", context)
