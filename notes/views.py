from django.shortcuts import render, redirect, get_object_or_404
from .models import Notes
from accounts.models import User, Notification
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import NotesForm
from django.http import JsonResponse


@login_required
def index(request):
    notes = request.user.user_to.order_by("-created_at")
    to_notes = request.user.user_from.order_by("-created_at")

    return render(
        request,
        "notes/index.html",
        {"notes": notes, "to_notes": to_notes},
    )

@login_required
def send(request, pk):
    to_user = get_object_or_404(get_user_model(), pk=pk)
    form = NotesForm(request.POST or None)
    # print(to_user, to_user.username, to_user.pk, pk, request.user)
    if form.is_valid():
        temp = form.save(commit=False)
        temp.from_user = request.user
        temp.to_user = to_user
        temp.save()
        message = f"{request.user}님이 {to_user}님에게 쪽지를 보냈습니다."
        Notification.objects.create(
            user=to_user, message=message, category="쪽지", nid=temp.id
        )
        return redirect("notes:index")
    context = {
        "form": form,
        "to_user": to_user,
    }
    return render(request, "notes/send.html", context)


def detail(request, pk):
    note = get_object_or_404(Notes, pk=pk)

    if request.user == note.to_user:
        if not note.read:
            note.read = True
            note.save()
        if not request.user.user_to.filter(read=False).exists():
            request.user.notice_note = True
            request.user.save()
        return render(request, "notes/detail.html", {"note": note})
    elif request.user == note.from_user:
        return render(request, "notes/detail.html", {"note": note})
    else:
        return redirect("notes:index")


def delete(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    if request.user == note.to_user and request.method == "POST":
        note.delete()
        return JsonResponse({"pk": pk})
    else:
        return redirect("notes:index")