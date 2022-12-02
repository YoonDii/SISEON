from django.shortcuts import render
from .forms import NoticesForm,  PhotoForm

# Create your views here.
def index(request):
    return render(request, "notices/index.html")


def create(request):
    return render(request, "notices/create.html")

def update(request):
    return render(request, "notices/update.html")