from bus_offer import BusOffer
from bus_company import BusCompany
from destination import Destination
from csv_loader import load_companies, load_destinations
import random
from datetime import datetime, timedelta



def generate_offers(
    companies,
    destinations,
    start_date=None,
    number_of_days=30,
    starting_offer_id=1):

    offers = []
    offer_number = starting_offer_id
    existing_trips = set()

    if start_date is None:
        start_date = datetime.today().date() + timedelta(days=1)

    # CREATE MORE REALISTIC DURATION HOURS:
    duration_ranges = {
        "Barcelona": (7, 9),
        "Valencia": (4, 6),
        "Seville": (6, 8),
        "Malaga": (6, 8),
        "Granada": (5, 7),
        "Cordoba": (4, 6),
        "Bilbao": (4, 6),
        "San Sebastian": (5, 7),
        "Zaragoza": (3, 5),
        "Alicante": (4, 6),
        "Murcia": (4, 6),
        "Salamanca": (2, 4),
        "Toledo": (1, 2),
        "Santiago de Compostela": (7, 10),
        "Cadiz": (7, 9)
    }

    company_rules = {
        "C001": {"price": 0.75, "duration": 1.15},
        "C002": {"price": 1.30, "duration": 0.80},
        "C003": {"price": 1.00, "duration": 1.00},
        "C004": {"price": 1.10, "duration": 1.05},
        "C005": {"price": 0.90, "duration": 1.10}
    }


    transfer_options = {
        "C001": [0, 1, 2],
        "C002": [0],
        "C003": [0, 1, 2],
        "C004": [0, 1],
        "C005": [0, 1]
    }

    #available_seats = random.randint(0, 100)

    attribute_probabilities = {
        "C001": {"luggage": 0.30, "refundable": 0.15, "changeable": 0.30},
        "C002": {"luggage": 0.80, "refundable": 0.70, "changeable": 0.85},
        "C003": {"luggage": 0.70, "refundable": 0.50, "changeable": 0.60},
        "C004": {"luggage": 1.00, "refundable": 0.65, "changeable": 0.75},
        "C005": {"luggage": 0.85, "refundable": 0.45, "changeable": 0.65}
    }

    departure_hours = {
        "C001": list(range(6, 22)),
        "C002": list(range(5, 24)),
        "C003": list(range(0, 24)),
        "C004": list(range(0, 24)),
        "C005": list(range(20, 24)) + list(range(0, 6))
    }

    # Generate offers for the next 30 days
    #for day in range(1, 31):
        #travel_date = (datetime.today() + timedelta(days=day)).strftime("%Y-%m-%d")

    # Generate offers for the requested date range
    for day in range(number_of_days):
        travel_date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")

        # Every destination must have at least one offer per day
        #daily_destinations = destinations.copy()

        # Add between 5 and 15 additional offers
        #extra_offers = random.randint(5, 15)

        #for i in range(extra_offers):
        #    daily_destinations.append(random.choice(destinations))

        # Generate offers for this day
        #for destination in daily_destinations:

        #    company = random.choice(companies)


        # Generate 3–6 trips for every destination each day
        for destination in destinations:

            number_of_trips = random.randint(3, 6)

            for trip in range(number_of_trips):
                company = random.choice(companies)
                # The remaining offer generation code continues here
                available_seats = random.randint(0, 100)
                transfers = random.choice(transfer_options[company.company_id])
                probabilities = attribute_probabilities[company.company_id]

                luggage_included = random.random() < probabilities["luggage"]
                refundable = random.random() < probabilities["refundable"]
                changeable = random.random() < probabilities["changeable"]

                offer_id = f"O{offer_number:03d}"

                offer_number += 1

                #travel_date = "2026-11-15"
                #days_ahead = random.randint(1, 30)
                #travel_date = (datetime.today() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
                #departure_time = "08:00"
                #departure_hour = random.randint(0, 23)

                #departure_hour = random.choice(departure_hours[company.company_id])
                #departure_minute = random.choice([0, 15, 30, 45])
                #departure_time = f"{departure_hour:02d}:{departure_minute:02d}"

                # MAKING SURE THAT WE ARE NOT CREATING DUPLCIATES:
                while True:
                    departure_hour = random.choice(departure_hours[company.company_id])
                    departure_minute = random.choice([0, 15, 30, 45])

                    departure_time = f"{departure_hour:02d}:{departure_minute:02d}"

                    trip_key = (
                        company.company_id,
                        destination.destination_id,
                        travel_date,
                        departure_time
                    )

                    if trip_key not in existing_trips:
                        existing_trips.add(trip_key)
                        break


                #arrival_time = "16:00"
                #duration_hours = random.randint(2, 12)

                min_hours, max_hours = duration_ranges[destination.name]
                #duration_hours = random.randint(min_hours, max_hours)
                base_duration = random.randint(min_hours, max_hours)

                duration_multiplier = company_rules[company.company_id]["duration"]

                random_factor = random.uniform(0.9, 1.1)

                final_duration_minutes = round(
                    base_duration * 60 * duration_multiplier * random_factor)

                # Generate price based on destination and company
                base_price = base_duration * 7

                price_multiplier = company_rules[company.company_id]["price"]

                price_random_factor = random.uniform(0.9, 1.1)

                price = round(
                    base_price * price_multiplier * price_random_factor, 2
                )


                departure_datetime = datetime.strptime(
                    travel_date + " " + departure_time, "%Y-%m-%d %H:%M")

                arrival_datetime = departure_datetime + timedelta(minutes=final_duration_minutes)
                arrival_time = arrival_datetime.strftime("%H:%M")

                offer = BusOffer(
                    offer_id, company, destination,
                    travel_date, departure_time, arrival_time,
                    price, available_seats,
                    luggage_included, transfers,
                    refundable, changeable
                )

                offers.append(offer)

    return offers


if __name__ == "__main__":
    companies = load_companies("data/companies.csv")
    destinations = load_destinations("data/destinations.csv")

    offers = generate_offers(companies, destinations)

    print("Total generated offers:", len(offers))

    first_date = offers[0].travel_date

    print(f"\nOffers for {first_date}:")

    for offer in offers:
        if offer.travel_date == first_date:
            print(
                offer.offer_id,
                offer.company.name,
                offer.destination.name,
                offer.departure_time,
                f"€{offer.price:.2f}"
            )