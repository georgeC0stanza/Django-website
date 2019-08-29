# http://www.postgresqltutorial.com/

import psycopg2
from . import config
from datetime import date
from .models import Client

"""
    This is the interface for the database.
"""


def add_business(
    place_id,
    business_name,
    total_reviews,
    rating,
    last_update,
    is_client,
    reviews_this_week=None,
):
    sql_statement = """INSERT INTO client_tracker_client (
                        place_id 
                    ,   business_name
                    ,   total_reviews
                    ,   rating
                    ,   last_update
                    ,   review_delta
                    ,   previous_total_reviews
                    ,   rating_delta
                    ,   previous_rating
                    ,   is_client
                    ,   reviews_this_week
                    )
                    VALUES (
                        %s
                    ,   %s
                    ,   %s
                    ,   %s
                    ,   %s
                    ,   0
                    ,   0
                    ,   0
                    ,   0
                    ,   %s
                    ,   0
                    ); """
    sql_argument = (
        place_id,
        business_name,
        total_reviews,
        rating,
        last_update,
        is_client,
    )
    _process_statement(sql_statement, sql_argument)


def update_business_rating(
    place_id,
    new_total_reviews,
    new_rating,
    rating_delta=None,
    review_delta=None,
    is_client=None,
    reviews_this_week=None,
):
    """
        Updates a business entry based on the given place_id.
        It will set the old to the current and the current to the new.
        It will auto-calculate the deltas.
    """
    business = dict(Client.objects.filter(place_id=place_id))
    previous_rating = business["rating"]
    if rating_delta is None:
        rating_delta = business["rating"] - business["previous_rating"]

    previous_total_reviews = business["total_reviews"]
    if review_delta is None:
        review_delta = business["total_reviews"] - business["previous_total_reviews"]

    if reviews_this_week is None:
        reviews_this_week = review_delta
    else:
        reviews_this_week = 0

    modify_business(
        place_id,
        None,  # new_place_id
        None,  # name
        new_total_reviews,
        new_rating,
        previous_rating,
        rating_delta,
        previous_total_reviews,
        review_delta,
        date.today(),
        is_client,
        reviews_this_week,
    )


def modify_business(
    old_place_id,
    new_place_id=None,
    new_business_name=None,
    new_total_reviews=None,
    new_rating=None,
    new_previous_rating=None,
    new_rating_delta=None,
    new_previous_total_reviews=None,
    new_review_delta=None,
    new_last_update=None,
    new_is_client=None,
    new_reviews_this_week=None,
):
    """
        Modify a given business' entry in the database.
        If data is not to be changed, pass NONE for that argument.
        - Requires old_place_id.
    """
    business = dict(Client.objects.filter(place_id=old_place_id))

    business["old_place_id"] = business["place_id"]
    if new_place_id is not None:
        business["new_place_id"] = new_place_id
    else:
        business["new_place_id"] = business["old_place_id"]
    if new_business_name is not None:
        business["business_name"] = new_business_name
    if new_total_reviews is not None:
        business["total_reviews"] = new_total_reviews
    if new_rating is not None:
        business["rating"] = new_rating
    if new_previous_rating is not None:
        business["previous_rating"] = new_previous_rating
    if new_rating_delta is not None:
        business["rating_delta"] = new_rating_delta
    if new_previous_total_reviews is not None:
        business["previous_total_reviews"] = new_previous_total_reviews
    if new_review_delta is not None:
        business["rating_review_delta"] = new_review_delta
    if new_last_update is not None:
        business["last_update"] = new_last_update
    if new_is_client is not None:
        business["is_client"] = new_is_client
    if new_reviews_this_week is not None:
        business["reviews_this_week"] = new_reviews_this_week

    # execute the update statement
    sql_statement = """
            UPDATE client_tracker_client 
            SET 
                place_id = %s
            ,   business_name = %s
            ,   total_reviews = %s
            ,   previous_total_reviews = %s
            ,   review_delta =%s
            ,   rating = %s
            ,   previous_rating = %s
            ,   rating_delta = %s
            ,   last_update = %s
            ,   is_client = %s
            ,   reviews_this_week = %s
            WHERE place_id = %s;
            """
    sql_argument = (
        business["new_place_id"],
        business["business_name"],
        business["total_reviews"],
        business["previous_total_reviews"],
        business["review_delta"],
        business["rating"],
        business["previous_rating"],
        business["rating_delta"],
        business["last_update"],
        business["is_client"],
        business["reviews_this_week"],
        business["old_place_id"],
    )
    _process_statement(sql_statement, sql_argument)


def get_all_competitors(place_id):
    """
        returns a dict of a business with dicts of businesses for each comptetitor 
        compare to get_business that the competitors are only id references
    """
    businesses = list()
    business = Client.objects.get(place_id=place_id)
    competitor = Client.objects.filter(place_id=business.competitor_1)
    businesses.append(competitor)
    competitor = Client.objects.filter(place_id=business.competitor_2)
    businesses.append(competitor)
    competitor = Client.objects.filter(place_id=business.competitor_3)
    businesses.append(competitor)
    competitor = Client.objects.filter(place_id=business.competitor_4)
    businesses.append(competitor)
    competitor = Client.objects.filter(place_id=business.competitor_5)
    businesses.append(competitor)
    return businesses


def _process_statement(
    sql_statement, sql_argument, callback=None, callback_arguments=None, fetchall=False
):
    """ 
        the heavy lifter, not for public access
        takes in an sql statement to execute,
        if a callback is given, this will send one row and the callback_arguments to callback to be processed
        and will send callback's result to our callee
        if no callback then we will wont do it or check for results. 
    """
    conn = None
    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql_statement, sql_argument)
        if callback is None:
            conn.commit()
            results = {"status": "OK"}

        if callback is not None:
            if fetchall is True:
                db_rows = cur.fetchall()
                results = callback(db_rows, callback_arguments)
            else:
                db_row = cur.fetchone()
                results = callback(db_row, callback_arguments)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        str_error = f"database error: {error}"
        results = {"status": "ERROR", "error": str_error}
    finally:
        if conn is not None:
            conn.close()
            return results
