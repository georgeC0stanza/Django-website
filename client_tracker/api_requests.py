## https://www.geeksforgeeks.org/get-post-requests-using-python/

import requests
import decimal


def get_api_key():
    """ returns the Google Places API key """

    f = open("./private/API_KEY.txt", "r")
    key = f.readline()
    f.close()
    return f


def google_places_get(placeid):
    """
        Calls the google places api on a given placeid.
        Returns a dictionary with rating and user_ratings_total.
    """
    api_fields = "rating,user_ratings_total"
    return google_places_get_helper(placeid, api_fields, get_api_key())


def google_places_get_helper(placeid, fields, key):
    """
        Helper function that does the heavy lifting.
        See google_places_get.
    """
    URL = "https://maps.googleapis.com/maps/api/place/details/json"
    PARAMS = {"placeid": placeid, "fields": fields, "key": key}
    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    if data["status"] == "OK":
        rating = 0
        user_ratings_total = 0
        if rating in data["result"]:
            rating = decimal.Decimal(str(data["result"]["rating"]))
        if user_ratings_total in data["result"]:
            user_ratings_total = data["result"]["user_ratings_total"]
        results = dict()
        results["rating"] = rating
        results["user_rating_total"] = user_ratings_total
        return results
    else:
        return {"status": "ERROR", "error": "api data not good or something."}


def get_all_info(place_id):
    api_fields = "name,formatted_address,user_ratings_total,rating"
    return google_places_get_helper_all(place_id, api_fields, get_api_key())


def google_places_get_helper_all(placeid, fields, key):
    """
        Helper function that does the heavy lifting.
    """
    URL = "https://maps.googleapis.com/maps/api/place/details/json"
    PARAMS = {"placeid": placeid, "fields": fields, "key": key}

    r = requests.get(url=URL, params=PARAMS)
    data = r.json()

    results = {"status": "OK"}
    if data["status"] == "OK":

        if "rating" in data["result"]:
            results["rating"] = decimal.Decimal(str(data["result"]["rating"]))
        else:
            results["rating"] = 0

        if "user_ratings_total" in data["result"]:
            results["total_reviews"] = data["result"]["user_ratings_total"]
        else:
            results["total_reviews"] = 0

        if "name" in data["result"]:
            results["business_name"] = data["result"]["name"]
        else:
            "TODO: throw error!"

        if "formatted_address" in data["result"]:
            results["business_address"] = data["result"]["formatted_address"]
        else:
            results["business_address"] = 0

        return results
    else:
        return {"status": "ERROR", "error": "api data not good or something."}
