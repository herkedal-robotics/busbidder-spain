import csv
from bus_company import BusCompany
from exceptions import InvalidCompanyError
from destination import Destination
from exceptions import InvalidDestinationError, InvalidOfferError
from pathlib import Path
from bus_offer import BusOffer
from booking import Booking

def load_companies(filename):
    list_companies = []
    set_companies_names = set()
    set_company_ids = set()

    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file) # reads each CSV row as a dictionary, 
                                      # using the column headers as keys.

        for row in reader:
            #name = row["name"].strip().lower()
            #company_id = row["company_id"].strip()
            try:
                name = row["name"].strip().lower()
            except AttributeError as error:
                raise InvalidCompanyError("Company name is missing or invalid") from error
            try:
                company_id = row["company_id"].strip()
            except AttributeError as error:
                raise InvalidCompanyError("Company ID is missing or invalid") from error

            if name in set_companies_names:
                raise InvalidCompanyError("Duplicate company name: " + name)

            if company_id in set_company_ids:
                raise InvalidCompanyError("Duplicate company ID: " + company_id)
            
            list_companies.append(BusCompany(row["company_id"], row["name"], row["description"]))
            set_companies_names.add(name)
            set_company_ids.add(company_id)

    return list_companies


def load_destinations(filename):
    list_destinations = []
    set_destination_names = set()
    set_destination_ids = set()

    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                name = row["name"].strip().lower()
            except AttributeError as error:
                raise InvalidDestinationError("Destination name invalid or missing") from error
            try:
                destination_id = row["destination_id"].strip()
            except AttributeError as error:
                raise InvalidDestinationError("Destination ID invalid or missing") from error

            if name in set_destination_names:
                raise InvalidDestinationError("Duplicate destination name: " + name)
            if destination_id in set_destination_ids:
                raise InvalidDestinationError("Duplicate destination ID: " + destination_id)
            # Check for invalid or empty values first
            destination = Destination(row["destination_id"], row["name"], row["region"])

            list_destinations.append(destination)
            set_destination_names.add(name)
            set_destination_ids.add(destination_id)

    return list_destinations


def save_offers(offers, file_path="data/offers.csv"):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "offer_id",
        "company_id",
        "destination_id",
        "travel_date",
        "departure_time",
        "arrival_time",
        "price",
        "available_seats",
        "luggage_included",
        "transfers",
        "refundable",
        "changeable"
    ]

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for offer in offers:
            writer.writerow({
                "offer_id": offer.offer_id,
                "company_id": offer.company.company_id,
                "destination_id": offer.destination.destination_id,
                "travel_date": offer.travel_date,
                "departure_time": offer.departure_time,
                "arrival_time": offer.arrival_time,
                "price": offer.price,
                "available_seats": offer.available_seats,
                "luggage_included": offer.luggage_included,
                "transfers": offer.transfers,
                "refundable": offer.refundable,
                "changeable": offer.changeable
            })

def parse_boolean(value):
    if value == "True":
        return True

    if value == "False":
        return False

    raise ValueError(f"Invalid boolean value: {value}")

def load_offers(companies, destinations, file_path="data/offers.csv"):
    path = Path(file_path)

    if not path.exists():
        return []

    company_lookup = {
        company.company_id: company
        for company in companies
    }

    destination_lookup = {
        destination.destination_id: destination
        for destination in destinations
    }

    offers = []
    offer_ids = set()

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            try:
                offer_id = row["offer_id"]

                if offer_id in offer_ids:
                    raise ValueError(f"Duplicate offer ID: {offer_id}")

                company = company_lookup[row["company_id"]]
                destination = destination_lookup[row["destination_id"]]

                offer = BusOffer(
                    offer_id=offer_id,
                    company=company,
                    destination=destination,
                    travel_date=row["travel_date"],
                    departure_time=row["departure_time"],
                    arrival_time=row["arrival_time"],
                    price=float(row["price"]),
                    available_seats=int(row["available_seats"]),
                    luggage_included=parse_boolean(row["luggage_included"]),
                    transfers=int(row["transfers"]),
                    refundable=parse_boolean(row["refundable"]),
                    changeable=parse_boolean(row["changeable"])
                )

                offers.append(offer)
                offer_ids.add(offer_id)

            except (ValueError, KeyError, TypeError, InvalidOfferError) as error:
                raise ValueError(
                    f"Invalid offer in CSV row {row_number}: {error}"
                ) from error

    return offers


def save_bookings(bookings, file_path="data/bookings.csv"):

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "booking_reference",
        "offer_id",
        "passenger_name",
        "luggage_included",
        "refundable",
        "changeable"]

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()

        for booking in bookings:
            writer.writerow({
                "booking_reference": booking.booking_reference,
                "offer_id": booking.offer.offer_id,
                "passenger_name": booking.passenger_name,
                "luggage_included": booking.luggage_included,
                "refundable": booking.refundable,
                "changeable": booking.changeable})


def load_bookings(offers, file_path="data/bookings.csv"):
    path = Path(file_path)

    if not path.exists():
        return []

    offer_lookup = {
        offer.offer_id: offer
        for offer in offers
    }

    bookings = []

    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:

            offer = offer_lookup[row["offer_id"]]

            booking = Booking(
                booking_reference=row["booking_reference"],
                offer=offer,
                passenger_name=row["passenger_name"],
                luggage_included=(
                    parse_boolean(row["luggage_included"])
                    if "luggage_included" in row
                    else offer.luggage_included),
                refundable=(
                    parse_boolean(row["refundable"])
                    if "refundable" in row
                    else offer.refundable),
                changeable=(
                    parse_boolean(row["changeable"])
                    if "changeable" in row
                    else offer.changeable))

            bookings.append(booking)

    return bookings


if __name__ == "__main__":
    try:
        companies = load_companies("data/companies.csv")
        
        for company in companies:
            print(company.company_id, company.name, company.description)

    except FileNotFoundError:
        print("Error: Company file was not found.")

    except KeyError as error:
        print("Error: Missing CSV column:", error)

    except InvalidCompanyError as error:
        print("Error:", error)

    else:
        print("Number of companies:", len(companies))

