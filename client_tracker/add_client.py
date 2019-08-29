from __future__ import annotations
from . import api_requests
from . import database_interactions
from datetime import date


def _get_place_ids_():
    """ 
        returns the Google Places ids in a list.
        put the ids in private/new_place_ids_to_be_added.txt.
    """
    f = open("private/new_place_ids_to_be_added.txt", "r")
    ids = list()
    for x in f:
        ids.append(x.rstrip())
    f.close()
    return ids


def _format_clients_(clients):
    return clients.split()


def add_clients(clients: str = None, is_client=None):
    """
        Adds new clients to the database for every placeid in private/new_place_ids_to_be_added.txt
        if none are supplied.
    """
    status = {"status": "OK"}
    if clients is None:
        clients = _get_place_ids_()
    else:
        clients = _format_clients_(clients)
    for (index, client_id) in enumerate(clients):
        client_info = api_requests.get_all_info(client_id)
        if client_info["status"] == "OK":
            database_interactions.add_business(
                client_id,
                client_info["business_name"],
                client_info["total_reviews"],
                client_info["rating"],
                date.today(),
                is_client,
            )
        else:
            status = {
                "status": "ERROR",
                "error": f"Bad placeid: '{client_id}' on line {index + 1}.",
            }
    return status
