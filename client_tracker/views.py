from django.shortcuts import render
from django.http import HttpResponse
from . import controller
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Client
from rest_framework import viewsets
from . import update_daemon
from django.contrib.auth.decorators import login_required
import json


class IndexView(generic.ListView):
    template_name = "client_tracker/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Client.objects.order_by("-last_update")


@login_required
def all_businesses_no_competitors(request):
    response = controller.get_list_businesses_without_competitors(
        request.POST.get("sort_by_is_client", "")
    )
    return HttpResponse(response)


@login_required
def review_velocity(request):
    response = controller.get_list_businesses_review_velocity(
        request.POST.get("is_client", ""), request.POST.get("order_by", "")
    )
    return HttpResponse(response)


@login_required
def rating_dropped(request):
    response = controller.get_list_businesses_rating_dropped(
        request.POST.get("is_client", ""), request.POST.get("rating_change_order", "")
    )
    return HttpResponse(response)


@login_required
def all_businesses_competitors(request):
    response = controller.get_list_businesses_with_competitors(
        request.POST.get("is_client", "")
    )
    return HttpResponse(response)


@login_required
def delete_client(request):
    response = controller.remove_client(request.POST.get("place_id", ""))
    return HttpResponse(response)


@login_required
def toggle_client(request):
    response = controller.toggle_client(request.POST.get("place_id", ""))
    return HttpResponse(response)


@login_required
def business_competitors(request):
    response = controller.get_business_competitors(request.POST.get("place_id", ""))
    return HttpResponse(response)


@login_required
def get_clients_without_competitors(request):
    response = controller.get_clients_without_competitors(
        request.POST.get("place_id", "")
    )
    return HttpResponse(response)


@login_required
def get_clients_with_competitors(request):
    response = controller.get_clients_with_competitors(request.POST.get("place_id", ""))
    return HttpResponse(response)


@login_required
def remove_competitor(request):
    response = controller.remove_competitor(
        request.POST.get("place_id", ""), request.POST.get("competitor_place_id", "")
    )
    return HttpResponse(response)


@login_required
def add_competitor_to_client(request):
    response = controller.add_competitor_to_client(
        request.POST.get("place_id", ""), request.POST.get("competitor_place_id", "")
    )
    return HttpResponse(response)


@login_required
def add_new_place_ids(request):
    response = controller.add_new_place_ids(
        request.POST.get("new_place_ids", ""), request.POST.get("is_client", "")
    )
    return HttpResponse(response)


@login_required
def force_update(request):
    status = update_daemon.start()
    return HttpResponse(json.dumps(status))
