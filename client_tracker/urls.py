from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view()),
    path("all-businesses/", views.all_businesses_no_competitors, name="all-businesses"),
    path("review-velocity/", views.review_velocity, name="review-velocity"),
    path("negative-reviews/", views.rating_dropped, name="negative-reviews"),
    path(
        "all-businesses-with-competitors/",
        views.all_businesses_competitors,
        name="all-businesses-with-competitors",
    ),
    path("delete-client/", views.delete_client, name="delete-client"),
    path("toggle-client/", views.toggle_client, name="toggle-client"),
    path(
        "get-business-competitors/",
        views.business_competitors,
        name="get-business-competitors",
    ),
    path(
        "get-not-competitors-on-client/",
        views.get_clients_without_competitors,
        name="get-not-competitors-on-client",
    ),
    path(
        "get-competitors-on-client/",
        views.get_clients_with_competitors,
        name="get-competitors-on-client",
    ),
    path("remove-competitor/", views.remove_competitor, name="remove-competitor"),
    path(
        "add-a-new-competitor/",
        views.add_competitor_to_client,
        name="add-a-new-competitor",
    ),
    path("sumbmitNewPlaceIDs/", views.add_new_place_ids, name="add-new-place-ids"),
    path("force-update/", views.force_update, name="force-update"),
]
