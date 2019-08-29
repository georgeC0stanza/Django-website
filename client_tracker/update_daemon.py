import time
from decimal import Decimal
from datetime import date
from . import mailer
from . import no_django_database_interactions
from . import api_requests


def start():
    """
        Updates the database with new google data and 
        notifies if there are changes.
    """
    today = date.today()
    things_to_send = list()
    businesses = list(no_django_database_interactions.get_all_businesses())

    for business in businesses:
        place_id = business["place_id"]
        # try:
        new_results = api_requests.google_places_get(
            place_id
        )  # we need some error handling here
        new_rating = new_results["rating"]
        new_total_reviews = new_results["user_rating_total"]

        # rating dropped
        status = None
        if new_total_reviews > business["total_reviews"]:
            no_django_database_interactions.update_business_rating(
                place_id, new_total_reviews, new_rating
            )
            if new_rating < business["rating"]:
                temp = dict()
                temp["reason"] = "ratings_dropped"
                temp["name"] = business["business_name"]
                things_to_send.append(temp)
        else:
            status = no_django_database_interactions.modify_business(
                place_id, None, None, None, None, None, None, None, None, None, None, 0
            )

        # low review velocity
        if business["last_update"] is None:
            business["last_update"] = today

        if (
            new_total_reviews == business["total_reviews"]
            and (today - business["last_update"]).days > 60
        ):
            temp = dict()
            temp["reason"] = "low_velocity"
            temp["name"] = business["business_name"]
            things_to_send.append(temp)

    # send emails
    if things_to_send:
        mailer.sender(things_to_send)
    return status


if __name__ == "__main__":
    start()
