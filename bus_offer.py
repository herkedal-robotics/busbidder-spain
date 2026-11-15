from bus_company import BusCompany
from destination import Destination
from exceptions import InvalidOfferError
import re
import math
from datetime import datetime, timedelta

def validate_travel_date(travel_date):
    month = int(travel_date[5:7])

    if month < 1 or month > 12:
        raise InvalidOfferError("Month must be between 01 and 12")

    day = int(travel_date[8:10])

    if day < 1 or day > 31:
        raise InvalidOfferError("Day must be between 01 and 31")

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    year = int(travel_date[0:4])

    # If it is a leap year, February has 29 days
    # so we are checking if it is a leap year:
    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        days_in_month[1] = 29

    max_days = days_in_month[month - 1]

    if day > max_days:
        raise InvalidOfferError("Invalid day for selected month")

def validate_time(time_value, time_type):
    hours = int(time_value[0:2])
    minutes = int(time_value[3:5])

    if hours < 0 or hours > 23:
        raise InvalidOfferError(f"Invalid hours ({time_value}) for {time_type}.")

    if minutes < 0 or minutes > 59:
        raise InvalidOfferError(f"Invalid minutes ({time_value}) for {time_type}")


class BusOffer:
    def __init__(self, offer_id, company, destination,
                 travel_date, departure_time, arrival_time,
                 price, available_seats,
                 luggage_included, transfers, refundable, changeable):
        # checking if ID is empty or invalid:
        if not isinstance(offer_id, str) or not offer_id.strip():
            raise InvalidOfferError("Offer ID cannot be empty")
        if not re.fullmatch(r"O[0-9]{3,4}", offer_id):
            raise InvalidOfferError("Offer ID must follow O001 format")
        
        # checking if company and destination are Objects of type
        # BusCompany and Destination.
        if not isinstance(company, BusCompany):
            raise InvalidOfferError("Company must be a BusCompany object")
        if not isinstance(destination, Destination):
            raise InvalidOfferError("Destination must be a Destination object")

        # CHECKING THE travel_date input:
        if not isinstance(travel_date, str) or not travel_date.strip():
            raise InvalidOfferError("Travel date must be a non-empty string")

        if not re.fullmatch(r"2[0-9]{3}-[0-9]{2}-[0-9]{2}", travel_date):
            raise InvalidOfferError("Invalid travel date format")

        validate_travel_date(travel_date)

        # checking departure_time and arrival_time:
        if not isinstance(departure_time, str) or not departure_time.strip():
            raise InvalidOfferError("Departure time must be a non-empty string")

        if not re.fullmatch(r"[0-9]{2}:[0-9]{2}", departure_time):
            raise InvalidOfferError("Departure time must follow HH:MM format")

        if not isinstance(arrival_time, str) or not arrival_time.strip():
            raise InvalidOfferError("Arrival time must be a non-empty string")

        if not re.fullmatch(r"[0-9]{2}:[0-9]{2}", arrival_time):
            raise InvalidOfferError("Arrival time must follow HH:MM format")

        validate_time(departure_time, "departure_time")
        validate_time(arrival_time, "arrival_time")

        # checking price and available_seats:
        if not isinstance(price, (int, float)) or isinstance(price, bool):
            raise InvalidOfferError("Price must be a number")

        if not math.isfinite(price):
            raise InvalidOfferError("Price must be a finite number")
        
        if price < 0 or price > 5000:
            raise InvalidOfferError("Price must be between 0-5000 EUR")

        if not isinstance(available_seats, int) or isinstance(available_seats, bool):
            raise InvalidOfferError("Available seats must be an integer")

        if available_seats < 0 or available_seats > 500:
            raise InvalidOfferError("Number of seats must be between 0-500")

        # additional information check:
        if not isinstance(luggage_included, bool):
            raise InvalidOfferError("Luggage must be T (True) or F (False)")

        if not isinstance(transfers, int) or isinstance(transfers, bool):
            raise InvalidOfferError("Transfers must be an integer")

        if transfers < 0 or transfers > 2:
            raise InvalidOfferError("Transfers must be between 0 and 2")

        if not isinstance(refundable, bool):
            raise InvalidOfferError("Refundable must be T(True) or F(False)")

        if not isinstance(changeable, bool):
            raise InvalidOfferError("Changeable must be T(True) or F(False)")

        self.offer_id = offer_id
        self.company = company
        self.destination = destination
        self.travel_date = travel_date
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.price = price
        self.available_seats = available_seats
        self.luggage_included = luggage_included
        self.transfers = transfers
        self.refundable = refundable
        self.changeable = changeable

        self.duration_time = self.calculate_duration_time()
        self.arrival_date = self.calculate_arrival_date()

    def calculate_duration_time(self):
        if self.departure_time == self.arrival_time:
            raise InvalidOfferError("Departure and arrival times cannot be identical")
            
        departure_hours = int(self.departure_time[0:2])
        departure_minutes = int(self.departure_time[3:5])

        arrival_hours = int(self.arrival_time[0:2])
        arrival_minutes = int(self.arrival_time[3:5])

        # Checking if the bus arrives on the same day:
        if arrival_hours > departure_hours or (arrival_hours == departure_hours and arrival_minutes > departure_minutes):
            #print("Same day")

            hours = arrival_hours - departure_hours
            minutes = arrival_minutes - departure_minutes

            duration = hours * 60 + minutes

        # Otherwise, the bus arrives the next day:
        else:
            #print("Different day")

            hours = (24 - departure_hours) + arrival_hours
            minutes = arrival_minutes - departure_minutes

            duration = hours * 60 + minutes

        return duration

    def calculate_arrival_date(self):
        if self.departure_time == self.arrival_time:
            raise InvalidOfferError("Departure and arrival times cannot be identical")
        
        # Convert travel_date string into a date object
        date = datetime.strptime(self.travel_date, "%Y-%m-%d")
        
        # Check if the bus arrives on the same day
        if self.arrival_time > self.departure_time:
            arrival_date = date

        # Otherwise, the bus arrives the next day
        else:
            arrival_date = date + timedelta(days=1)

        # Convert the date back into a string
        return arrival_date.strftime("%Y-%m-%d")
