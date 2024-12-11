"""This module defines a middleare class, which sets the expiration date 
of the user session to the end of the day. That ensures that one device is
only counted once in the page view statistics.

"""

from datetime import datetime, timedelta

# from django.db import ProgrammingError


# class SessionExpiration:
#     """Sets the session expiration to the end of the current day
#
#     This middleware sets the session expiration of the session bound
#     to the current request to the end of the current day. This makes
#     it possible to count the website visits per day, just by counting
#     the number of sessions stored in the database. Thereby only anonymized
#     session data is stored in the database and no IP- or client information.
#
#     """
#
#     def __init__(self, get_response):
#         """Constructor of the middleware class."""
#         self.get_response = get_response
#
#     def __call__(self, request):
#         """Method is executed before requested view is called."""
#         response = self.get_response(request)
#
#         now = datetime.now()
#
#         # Calculate the end of the day
#         end_of_day = datetime.combine(
#             now.date() + timedelta(days=1), datetime.min.time()
#         )
#
#         # Calculate the number of seconds until the end of the day
#         seconds_until_end_of_day = (end_of_day - now).total_seconds()
#
#         # Set the session expiry
#         request.session.set_expiry(seconds_until_end_of_day)
#
#         return response
