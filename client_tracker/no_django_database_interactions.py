# http://www.postgresqltutorial.com/

import psycopg2
from . import config
from datetime import date

"""
    This is the interface to the database for when the Django Model system is inaccessible.
"""


def get_all_businesses(competitors=False):
    """
        Returns a list of dicts from the database with all business entries.
    """

    sql_statement = "SELECT * FROM client_tracker_client"
    return _process_statement(
        sql_statement, None, __get_all_businesses_callback__, competitors, True
    )


def __get_all_businesses_callback__(results, competitors):
    business_list = list()
    business_entry = dict()
    if competitors == True:
        for business in results:
            business_entry = {
                "place_id": business[1],
                "business_name": business[2],
                "total_reviews": business[3],
                "rating": business[4],
                "last_update": business[5],
                "competitor_1": get_business(business[6]),
                "competitor_2": get_business(business[7]),
                "competitor_3": get_business(business[8]),
                "competitor_4": get_business(business[9]),
                "competitor_5": get_business(business[10]),
                "rating_delta": business[11],
                "previous_rating": business[12],
                "previous_total_reviews": business[13],
                "review_delta": business[14],
            }
            business_list.append(business_entry)
    else:
        for business in results:
            business_entry = {
                "place_id": business[1],
                "business_name": business[2],
                "total_reviews": business[3],
                "rating": business[4],
                "last_update": business[5],
                "competitor_1": business[6],
                "competitor_2": business[7],
                "competitor_3": business[8],
                "competitor_4": business[9],
                "competitor_5": business[10],
                "rating_delta": business[11],
                "previous_rating": business[12],
                "previous_total_reviews": business[13],
                "review_delta": business[14],
            }
            business_list.append(business_entry)
    return business_list


def get_business(place_id):
    """
        Returns a dictionary of all the data for a specific business.
    """
    sql_statement = "SELECT * FROM client_tracker_client WHERE place_id = %s"
    sql_argument = (place_id,)
    return _process_statement(
        sql_statement, sql_argument, __get_business_callback__, False, False
    )


def __get_business_callback__(results, arguments=None):
    print(results)
    return {
        "status": "OK",
        "place_id": results[1],
        "business_name": results[2],
        "total_reviews": results[3],
        "rating": results[4],
        "last_update": results[5],
        "competitor_1": results[6],
        "competitor_2": results[7],
        "competitor_3": results[8],
        "competitor_4": results[9],
        "competitor_5": results[10],
        "rating_delta": results[11],
        "previous_rating": results[12],
        "previous_total_reviews": results[13],
        "review_delta": results[14],
        "is_client": results[15],
        "reviews_this_week": results[16],
    }
    # TODO: we shouldn't be setting status here. that should be the job of process statement


def update_business_rating(
    place_id,
    new_total_reviews,
    new_rating,
    rating_delta=None,
    review_delta=None,
    reviews_this_week=None,
):
    """
        Updates a business entry based on the given place_id.
        It will set the old to the current and the current to the new.
        It will auto-calculate the deltas.
    """
    business = get_business(place_id)
    previous_rating = business["rating"]
    if rating_delta is None:
        rating_delta = new_rating - previous_rating

    previous_total_reviews = business["total_reviews"]
    if review_delta is None:
        review_delta = new_total_reviews - previous_total_reviews

    if reviews_this_week is None:
        reviews_this_week = review_delta
    else:
        reviews_this_week = 0

    return modify_business(
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
    business = dict(get_business(old_place_id))

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
        business["review_delta"] = new_review_delta
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
    return _process_statement(sql_statement, sql_argument)


def get_users_email():
    """
        Returns a list of dicts from the database with all users.
    """
    sql_statement = "SELECT * FROM auth_user"
    return _process_statement(
        sql_statement, None, __get_users_email_callback__, False, True
    )


def __get_users_email_callback__(results, arg=None):
    user_list = list()
    user_entry = dict()
    for user in results:
        user_entry = {
            "first_name": user[5],
            "last_name": user[6],
            "email": user[7],
            "is_staff": user[8],
            "is_active": user[9],
        }
        user_list.append(user_entry)
    return user_list


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
