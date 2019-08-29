import smtplib
import ssl
import csv
from . import no_django_database_interactions
import time

# https://realpython.com/python-send-email/


def sender(clients):
    """ 
        Sends email to everyone that is a staff, is active, 
        and has an email about the changes in clients. 
        Clients with a dictionary key "reason" of 'ratings_dropped' 
        or 'low_velocity' will be tallied before the count of each is sent off.
    """
    message = ""
    clients_ratings = ""
    clients_velocity = ""
    for entry in clients:
        if entry["reason"] == "ratings_dropped":
            clients_ratings += entry["name"]
            clients_ratings += ", "
        if entry["reason"] == "low_velocity":
            clients_velocity += entry["name"]
            clients_velocity += ", "

    clients_ratings = clients_ratings[:-2]
    clients_velocity = clients_velocity[:-2]

    message = """Subject: Our weekly update!

    Hi {name}, 

    This is the weekly update:

    These clients' ratings have dropped: 
        {clients1}. 

    These clients' have had zero reviews over the past two months: 
        {clients2}.

    Thank you! This is an automated email.
    """
    from_address = "mail@mail.com"
    password = "password"

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_address, password)
            for user in no_django_database_interactions.get_users_email():
                if (
                    user["email"]
                    and user["is_staff"] == True
                    and user["is_active"] == True
                ):
                    full_name = user["first_name"] + " " + user["last_name"]
                    server.sendmail(
                        from_address,
                        user["email"],
                        message.format(
                            name=full_name,
                            clients1=clients_ratings,
                            clients2=clients_velocity,
                        ),
                    )

    except:
        # second time because google is weird and fails the first login attempt
        time.sleep(10)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(from_address, password)
            for user in no_django_database_interactions.get_users_email():
                if (
                    user["email"]
                    and user["is_staff"] == True
                    and user["is_active"] == True
                ):
                    full_name = user["first_name"] + " " + user["last_name"]
                    server.sendmail(
                        from_address,
                        user["email"],
                        message.format(
                            name=full_name,
                            clients1=clients_ratings,
                            clients2=clients_velocity,
                        ),
                    )
