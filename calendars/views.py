from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from accounts.models import *
from .models import *
from django.db.models import Count, Q
from .utils import Calendar
from .forms import EventForm


class CalendarView(generic.ListView):
    model = Event
    template_name = "calendars/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        context["k"] = message_count(self.request)
        return context


def message_count(request):
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.pk)
        new_message = Notification.objects.filter(Q(user=user.pk) & Q(check=False))
        message_count = len(new_message)
    return message_count


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


def event_detail(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, "calendars/event_detail.html", {"event": event})


def event_new(request, event_id=None):
    instance = Event()
    if event_id and request.user.is_superuser:
        instance = get_object_or_404(Event, pk=event_id)
    elif event_id and not request.user.is_superuser:
        return redirect("calendars:event_detail", pk=event_id)

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("calendars:index"))
    return render(request, "calendars/event_form.html", {"form": form})


def event_edit(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("calendars:event_detail", event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, "calendars/event_form.html", {"form": form})


def event_delete(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect("calendars:index")
