from decimal import Decimal
import decimal
from datetime import date
import json
from .models import Client, ClientSerializer, ClientSerializerWithCompetitors
from django.forms.models import model_to_dict
from django.forms import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Model
from . import add_client
from . import database_interactions
from . import mailer


class ExtendedEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, Model):
            return model_to_dict(o)
        return super().default(o)


def get_list_businesses_without_competitors(sort_by_is_client=None):
    """ Returns a list of businesses without competitors. """
    businesses = sorted(
        Client.objects.all(), key=lambda business: business.business_name, reverse=False
    )
    if sort_by_is_client == "True":
        businesses = sorted(
            Client.objects.filter(is_client=False),
            key=lambda business: business.business_name,
            reverse=False,
        )
        businesses += sorted(
            Client.objects.filter(is_client=True),
            key=lambda business: business.business_name,
            reverse=False,
        )
    serializer = ClientSerializer(businesses, many=True)
    my_json = serializer.data
    return json.dumps(my_json)


def get_list_businesses_review_velocity(is_client, review_delta_order):
    """ Returns a list of businesses in order of thier review velocity. 
        review_delta_order is either "ascending" or not. 
    """
    review_delta_order_bool = False
    if review_delta_order == "ascending":
        review_delta_order_bool = True

    businesses = sorted(
        Client.objects.all().filter(is_client=is_client),
        key=lambda business: business.days_since_last_review,
        reverse=review_delta_order_bool,
    )
    serializer = ClientSerializer(businesses, many=True)
    my_json = serializer.data
    return json.dumps(my_json)


def get_list_businesses_rating_dropped(is_client, rating_change_order):
    """ Returns a list of businesses whose ratings have dropped. 
        rating_change_order is either "descending" or not. 
    """
    rating_change_order_bool = False
    if rating_change_order == "descending":
        rating_change_order_bool = True

    businesses = sorted(
        Client.objects.all().filter(is_client=is_client),
        key=lambda business: business.rating_delta,
        reverse=rating_change_order_bool,
    )
    # remove the positive rating deltas
    businesses[:] = [business for business in businesses if business.rating_delta <= 0]

    serializer = ClientSerializer(businesses, many=True)
    my_json = serializer.data
    return json.dumps(my_json)


def get_list_businesses_with_competitors(is_client):
    """ Returns a list of business with their competitors. """
    businesses = sorted(
        Client.objects.all().filter(is_client=is_client),
        key=lambda business: business.business_name,
        reverse=False,
    )
    serializer = ClientSerializerWithCompetitors(businesses, many=True)
    my_json = serializer.data
    return json.dumps(my_json)


def remove_client(client_id):
    """ Removes a client from the database. """
    Client.objects.filter(place_id=client_id).delete()
    return json.dumps({"status": "OK"})


def toggle_client(client_id):
    """ Toggles the is_client atribute of a client. """
    client = Client.objects.get(place_id=client_id)
    client.is_client = not client.is_client
    client.save()
    return json.dumps({"status": "OK"})


def get_business_competitors(place_id):
    """ Returns a single client with its competitors for a given place id. """
    clients = sorted(
        Client.objects.filter(place_id=place_id),
        key=lambda business: business.review_delta,
        reverse=True,
    )
    serializer = ClientSerializerWithCompetitors(clients, many=True)
    my_json = serializer.data
    return json.dumps(my_json)


def get_clients_without_competitors(place_id):
    """ Returns a list of clients without the given client and its competitors. """
    competitors = Client.objects.filter(place_id=place_id).values(
        "competitor_1", "competitor_2", "competitor_3", "competitor_4", "competitor_5"
    )
    comp_1 = ""
    comp_2 = ""
    comp_3 = ""
    comp_4 = ""
    comp_5 = ""

    if competitors[0]["competitor_1"]:
        comp_1 = competitors[0]["competitor_1"]
    if competitors[0]["competitor_2"]:
        comp_2 = competitors[0]["competitor_2"]
    if competitors[0]["competitor_3"]:
        comp_3 = competitors[0]["competitor_3"]
    if competitors[0]["competitor_4"]:
        comp_4 = competitors[0]["competitor_4"]
    if competitors[0]["competitor_5"]:
        comp_5 = competitors[0]["competitor_5"]

    clients = sorted(
        Client.objects.all(), key=lambda business: business.business_name, reverse=False
    )
    # filter
    clients[:] = [
        business
        for business in clients
        if business.place_id != comp_1
        and business.place_id != comp_2
        and business.place_id != comp_3
        and business.place_id != comp_4
        and business.place_id != comp_5
        and business.place_id != place_id
    ]
    serializer = ClientSerializer(clients, many=True)
    my_json = serializer.data
    return json.dumps(my_json)


def get_clients_with_competitors(place_id):
    """ Returns a list of clients without the given client. 
        The competitors' ids are replaced with the client's row. 
    """
    competitors = Client.objects.filter(place_id=place_id).values(
        "competitor_1", "competitor_2", "competitor_3", "competitor_4", "competitor_5"
    )
    comp_1 = ""
    comp_2 = ""
    comp_3 = ""
    comp_4 = ""
    comp_5 = ""

    if competitors[0]["competitor_1"]:
        comp_1 = competitors[0]["competitor_1"]
    if competitors[0]["competitor_2"]:
        comp_2 = competitors[0]["competitor_2"]
    if competitors[0]["competitor_3"]:
        comp_3 = competitors[0]["competitor_3"]
    if competitors[0]["competitor_4"]:
        comp_4 = competitors[0]["competitor_4"]
    if competitors[0]["competitor_5"]:
        comp_5 = competitors[0]["competitor_5"]

    clients = sorted(
        Client.objects.all(), key=lambda business: business.business_name, reverse=False
    )
    # filter
    clients[:] = [
        business
        for business in clients
        if business.place_id == comp_1
        or business.place_id == comp_2
        or business.place_id == comp_3
        or business.place_id == comp_4
        or business.place_id == comp_5
        and business.place_id != place_id
    ]
    serializer = ClientSerializer(clients, many=True)
    my_json = serializer.data
    return json.dumps(my_json)


def remove_competitor(client_id, competitor_id):
    """ Removes the attachment between a client and one of its competitors. """
    client = Client.objects.get(place_id=client_id)

    if client.competitor_1 is not None and client.competitor_1 == Client.objects.get(
        place_id=competitor_id
    ):
        client.competitor_1 = None
    elif client.competitor_2 is not None and client.competitor_2 == Client.objects.get(
        place_id=competitor_id
    ):
        client.competitor_2 = None
    elif client.competitor_3 is not None and client.competitor_3 == Client.objects.get(
        place_id=competitor_id
    ):
        client.competitor_3 = None
    elif client.competitor_4 is not None and client.competitor_4 == Client.objects.get(
        place_id=competitor_id
    ):
        client.competitor_4 = None
    elif client.competitor_5 is not None and client.competitor_5 == Client.objects.get(
        place_id=competitor_id
    ):
        client.competitor_5 = None
    client.save()

    competitor = Client.objects.get(place_id=competitor_id)

    if (
        competitor.competitor_1 is not None
        and competitor.competitor_1 == Client.objects.get(place_id=competitor_id)
    ):
        competitor.competitor_1 = None
    elif (
        competitor.competitor_2 is not None
        and competitor.competitor_2 == Client.objects.get(place_id=competitor_id)
    ):
        competitor.competitor_2 = None
    elif (
        competitor.competitor_3 is not None
        and competitor.competitor_3 == Client.objects.get(place_id=competitor_id)
    ):
        competitor.competitor_3 = None
    elif (
        competitor.competitor_4 is not None
        and competitor.competitor_4 == Client.objects.get(place_id=competitor_id)
    ):
        competitor.competitor_4 = None
    elif (
        competitor.competitor_5 is not None
        and competitor.competitor_5 == Client.objects.get(place_id=competitor_id)
    ):
        competitor.competitor_5 = None
    competitor.save()

    return json.dumps({"status": "OK"})


def add_competitor_to_client(client_id, comp_id):
    """ Attaches two clients together as competitors. """
    client = Client.objects.get(place_id=client_id)

    if client.competitor_1 is None:
        client.competitor_1 = Client.objects.get(place_id=comp_id)
    elif client.competitor_2 is None and client.competitor_1 != Client.objects.get(
        place_id=comp_id
    ):
        client.competitor_2 = Client.objects.get(place_id=comp_id)
    elif client.competitor_3 is None and client.competitor_2 != Client.objects.get(
        place_id=comp_id
    ):
        client.competitor_3 = Client.objects.get(place_id=comp_id)
    elif client.competitor_4 is None and client.competitor_3 != Client.objects.get(
        place_id=comp_id
    ):
        client.competitor_4 = Client.objects.get(place_id=comp_id)
    elif client.competitor_5 is None and client.competitor_4 != Client.objects.get(
        place_id=comp_id
    ):
        client.competitor_5 = Client.objects.get(place_id=comp_id)
    client.save()

    competitor = Client.objects.get(place_id=comp_id)
    if competitor.competitor_1 is None:
        competitor.competitor_1 = Client.objects.get(place_id=client_id)
    elif (
        competitor.competitor_2 is None
        and competitor.competitor_1 != Client.objects.get(place_id=client_id)
    ):
        competitor.competitor_2 = Client.objects.get(place_id=client_id)
    elif (
        competitor.competitor_3 is None
        and competitor.competitor_2 != Client.objects.get(place_id=client_id)
    ):
        competitor.competitor_3 = Client.objects.get(place_id=client_id)
    elif (
        competitor.competitor_4 is None
        and competitor.competitor_3 != Client.objects.get(place_id=client_id)
    ):
        competitor.competitor_4 = Client.objects.get(place_id=client_id)
    elif (
        competitor.competitor_5 is None
        and competitor.competitor_4 != Client.objects.get(place_id=client_id)
    ):
        competitor.competitor_5 = Client.objects.get(place_id=client_id)
    competitor.save()

    return json.dumps({"status": "OK"})


def add_new_place_ids(new_ids, is_client):
    """ 
        For each place_id, 
        the google api is called to get rating information and that is inserted into the database.
    """
    return json.dumps(add_client.add_clients(new_ids, is_client), cls=ExtendedEncoder)


######################## unused ##################
"""

def myconverter(arg):
    if isinstance(arg, decimal.Decimal):
        return "{0:f}".format(arg)
    return arg.__str__()


def my_json_encoder(to_json):
    inter_json = json.dumps(to_json, cls=ExtendedEncoder)
    to_json = json.loads(inter_json)
    return json.dumps(to_json, default=myconverter)


def get_business(place_id):
    client = list(Client.objects.filter(place_id=place_id))
    return json.dumps(client, cls=ExtendedEncoder) 


def get_list_businesses():
    businesses = sorted(
        Client.objects.all(), key=lambda business: business.business_name
    )
    return json.dumps(businesses, cls=ExtendedEncoder)

"""
