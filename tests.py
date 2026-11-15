from csv_loader import load_companies, load_destinations
from bus_company import BusCompany, Review
from exceptions import InvalidCompanyError
import tempfile
import os
from destination import Destination
from exceptions import InvalidDestinationError
from bus_offer import BusOffer
from exceptions import InvalidOfferError


def test_load_valid_companies():
    companies = load_companies("data/companies.csv")

    assert len(companies) == 5

    print("Valid companies loading test passed!")

test_load_valid_companies()

def test_empty_company_name():
    try:
        BusCompany("C006", "", "Test company")

    except InvalidCompanyError:
        print("Empty company name validation test passed!")
        return

    assert False, "Expected InvalidCompanyError was not raised"

test_empty_company_name()

def test_duplicate_company_name():
    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "companies.csv")

        with open(filename, "w", encoding="utf-8", newline="") as file:
            file.write("company_id,name,description\n")
            file.write("C001,SolRuta,Low-cost services\n")
            file.write("C002,SolRuta,Another company\n")

        try:
            load_companies(filename)

        except InvalidCompanyError:
            print("Duplicate company name test passed!")
            return

        assert False, "Expected InvalidCompanyError was not raised"

test_duplicate_company_name()

def test_duplicate_company_id():
    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "companies.csv")

        with open(filename, "w", encoding="utf-8", newline="") as file:
            file.write("company_id,name,description\n")
            file.write("C001,SolRuta,Low-cost services\n")
            file.write("C001,CostaLink,Another company\n")

        try:
            load_companies(filename)

        except InvalidCompanyError as error:
            assert "Duplicate company ID" in str(error)
            print("Duplicate company ID test passed!")
            return

        assert False, "Expected InvalidCompanyError was not raised"

test_duplicate_company_id()


def test_missing_company_file():
    try:
        load_companies("data/missing_companies.csv")

    except FileNotFoundError:
        print("Missing company file test passed!")
        return

    assert False, "Expected FileNotFoundError was not raised"

test_missing_company_file()

# wrong column name:
def test_missing_company_column():
    with tempfile.TemporaryDirectory() as folder:
        filename = os.path.join(folder, "companies.csv")

        with open(filename, "w", encoding="utf-8", newline="") as file:
            file.write("company_id,company_name,description\n")
            file.write("C001,SolRuta,Low-cost services\n")

        try:
            load_companies(filename)

        except KeyError as error:
            assert error.args[0] == "name"
            print("Missing/wrong company column test passed!")
            return

        assert False, "Expected KeyError was not raised"

test_missing_company_column()

def test_empty_company_id():
    try:
        BusCompany("", "SolRuta", "Low-cost buses")
    except InvalidCompanyError:
        print("Test passed: Empty company ID rejected.")
        return

    assert False, "Empty company ID was accepted"

test_empty_company_id()

def test_empty_company_description():
    try:
        BusCompany("C001", "SolRuta", "")
    except InvalidCompanyError:
        print("Test passed: Empty company description rejected.")
        return

    assert False, "Empty company description was accepted"
    
test_empty_company_description()

def test_invalid_company_id_format():
    try:
        BusCompany("C01", "SolRuta", "Low-cost buses")
    except InvalidCompanyError:
        print("Test passed: Invalid company ID rejected.")
        return

    assert False, "Invalid company ID was accepted"
    
test_invalid_company_id_format()



def test_empty_destination_id():
    try:
        Destination("", "Barcelona", "Catalonia")
    except InvalidDestinationError:
        print("Test passed: Empty destination ID rejected.")
        return

    assert False, "Empty destination ID was accepted"

test_empty_destination_id()

def test_empty_destination_name():
    try:
        Destination("D001", "", "Catalonia")
    except InvalidDestinationError:
        print("Test passed: Empty destination name rejected.")
        return

    assert False, "Empty destination name was accepted"

test_empty_destination_name()

def test_empty_destination_region():
    try:
        Destination("D001", "Barcelona", "")
    except InvalidDestinationError:
        print("Test passed: Empty destination region rejected.")
        return

    assert False, "Empty destination region was accepted"

test_empty_destination_region()

def test_invalid_destination_id_format():
    try:
        Destination("D1111", "Barcelona", "Catalonia")
    except InvalidDestinationError:
        print("Test passed: Invalid destination ID rejected.")
        return

    assert False, "Invalid destination ID was accepted"

test_invalid_destination_id_format()


def test_load_valid_destinations():
    destinations = load_destinations("data/destinations.csv")
    assert len(destinations) == 15
    print("Test passed: 15 destinations loaded successfully.")

test_load_valid_destinations()


def test_duplicate_destination_name():
    csv_content = (
        "destination_id,name,region\n"
        "D001,Barcelona,Catalonia\n"
        "D002,Barcelona,Catalonia\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
        newline=""
    ) as file:
        file.write(csv_content)
        filename = file.name

    try:
        try:
            load_destinations(filename)
        except InvalidDestinationError as error:
            assert "Duplicate destination name" in str(error)
            print("Test passed: Duplicate destination name rejected.")
            return

        assert False, "Duplicate destination name was accepted"

    finally:
        os.remove(filename)

test_duplicate_destination_name()




def test_duplicate_destination_id():
    csv_content = (
        "destination_id,name,region\n"
        "D001,Barcelona,Catalonia\n"
        "D001,Bilbao,Basque Country\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
        newline=""
    ) as file:
        file.write(csv_content)
        filename = file.name

    try:
        try:
            load_destinations(filename)
        except InvalidDestinationError as error:
            assert "Duplicate destination ID" in str(error)
            print("Test passed: Duplicate destination ID rejected.")
            return

        assert False, "Duplicate destination id was accepted"

    finally:
        os.remove(filename)

test_duplicate_destination_id()


def test_missing_destination_region():
    csv_content = (
        "destination_id,name,region\n"
        "D001,Barcelona\n"
    )

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".csv",
        delete=False,
        encoding="utf-8",
        newline=""
    ) as file:
        file.write(csv_content)
        filename = file.name

    try:
        try:
            load_destinations(filename)
        except InvalidDestinationError as error:
            assert "Destination region cannot be empty" in str(error)
            print("Test passed: Missing destination region rejected.")
            return

        assert False, "Missing destination region was accepted"

    finally:
        os.remove(filename)

test_missing_destination_region()


def test_valid_bus_offer():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    offer = BusOffer("O001", company, destination, "2026-11-15", "08:00", "16:00", 35.0, 20, True, 0, True, False)

    assert offer.offer_id == "O001"
    assert offer.company.name == "SolRuta"
    assert offer.destination.name == "Barcelona"

    print("Test passed: Valid bus offer created.")

test_valid_bus_offer()


def test_invalid_offer_id():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    try:
        BusOffer("O01", company, destination, "2026-11-15", "08:00", "16:00", 35.0, 20, True, 0, True, False)
    except InvalidOfferError:
        print("Test passed: Invalid offer ID rejected.")
        return

    assert False, "Invalid offer ID was accepted"

test_invalid_offer_id()


# Test an invalid company object:
def test_invalid_offer_company():
    destination = Destination("D001", "Barcelona", "Catalonia")

    try:
        BusOffer("O001", "SolRuta", destination, "2026-11-15", "08:00", "16:00", 35.0, 20, True, 0, True, False)
    except InvalidOfferError:
        print("Test passed: Invalid company object rejected.")
        return

    assert False, "Invalid company object was accepted"

test_invalid_offer_company()

# Test an invalid destination object:
def test_invalid_offer_destination():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")

    try:
        BusOffer("O001", company, "Barcelona", "2026-11-15", "08:00", "16:00", 35.0, 20, True, 0, True, False)
    except InvalidOfferError:
        print("Test passed: Invalid destination object rejected.")
        return

    assert False, "Invalid destination object was accepted"

test_invalid_offer_destination()


# TESTING FOR CORRECT travel_date FROM bus_offer.py:
def test_valid_travel_date():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    offer = BusOffer("O001", company, destination,
                     "2026-11-15", "08:00", "16:00", 35.0, 20, True, 0, True, False)

    assert offer.travel_date == "2026-11-15"
    print("Test passed: Valid travel date accepted.")


def test_invalid_travel_date_format():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    try:
        BusOffer("O001", company, destination,
                 "2026/11/15", "08:00", "16:00", 35.0, 20, True, 0, True, False)
    except InvalidOfferError:
        print("Test passed: Invalid date format rejected.")
        return

    assert False, "Invalid date format was accepted"


def test_invalid_travel_month():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    try:
        BusOffer("O001", company, destination,
                 "2026-13-15", "08:00", "16:00", 35.0, 20, True, 0, True, False)
    except InvalidOfferError:
        print("Test passed: Invalid month rejected.")
        return

    assert False, "Invalid month was accepted"


def test_invalid_day_for_month():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    try:
        BusOffer("O001", company, destination,
                 "2026-04-31", "08:00", "16:00", 35.0, 20, True, 0, True, False)
    except InvalidOfferError:
        print("Test passed: Invalid day for month rejected.")
        return

    assert False, "Invalid day for month was accepted"


def test_invalid_february_date():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    try:
        BusOffer("O001", company, destination,
                 "2026-02-29", "08:00", "16:00", 35.0, 20, True, 0, True, False)
    except InvalidOfferError:
        print("Test passed: February 29 rejected in non-leap year.")
        return

    assert False, "Invalid February date was accepted"


def test_valid_leap_year():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    offer = BusOffer("O001", company, destination,
                     "2028-02-29", "08:00", "16:00", 35.0, 20, True, 0, True, False)

    assert offer.travel_date == "2028-02-29"
    print("Test passed: February 29 accepted in leap year.")


def test_invalid_leap_year_day():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    try:
        BusOffer("O001", company, destination,
                 "2028-02-30", "08:00", "16:00", 35.0, 20, True, 0, True, False)
    except InvalidOfferError:
        print("Test passed: February 30 rejected in leap year.")
        return

    assert False, "Invalid leap year date was accepted"

print("-------travel_date test: -------")
test_valid_travel_date()
test_invalid_travel_date_format()
test_invalid_travel_month()
test_invalid_day_for_month()
test_invalid_february_date()
test_valid_leap_year()
test_invalid_leap_year_day()



# TESTING departure_time AND arrival_time

# Helper function:
def create_test_offer(departure_time="08:00", arrival_time="16:00",
                      price=35.0, available_seats=20,
                      travel_date="2026-11-15",
                      luggage_included=True, transfers=0,
                      refundable=True, changeable=False, offer_id="O001"):

    company = BusCompany("C001", "SolRuta", "Low-cost buses")
    destination = Destination("D001", "Barcelona", "Catalonia")

    return BusOffer(offer_id, company, destination,
                    travel_date, departure_time, arrival_time,
                    price, available_seats,
                    luggage_included, transfers,
                    refundable, changeable)

def test_valid_time():
    offer = create_test_offer("08:00", "16:00")

    assert offer.departure_time == "08:00"
    assert offer.arrival_time == "16:00"

    print("Test passed: Valid departure and arrival times accepted.")


def test_valid_overnight_time():
    offer = create_test_offer("22:00", "03:00")

    assert offer.departure_time == "22:00"
    assert offer.arrival_time == "03:00"

    print("Test passed: Overnight departure and arrival times accepted.")


def test_invalid_departure_hours():
    try:
        create_test_offer("25:00", "16:00")
    except InvalidOfferError as error:
        assert "Invalid hours" in str(error)
        print("Test passed: Invalid departure hours rejected.")
        return

    assert False, "Invalid departure hours were accepted"


def test_invalid_departure_minutes():
    try:
        create_test_offer("08:65", "16:00")
    except InvalidOfferError as error:
        assert "Invalid minutes" in str(error)
        print("Test passed: Invalid departure minutes rejected.")
        return

    assert False, "Invalid departure minutes were accepted"


def test_invalid_arrival_hours():
    try:
        create_test_offer("08:00", "24:00")
    except InvalidOfferError as error:
        assert "Invalid hours" in str(error)
        print("Test passed: Invalid arrival hours rejected.")
        return

    assert False, "Invalid arrival hours were accepted"


def test_invalid_arrival_minutes():
    try:
        create_test_offer("08:00", "16:99")
    except InvalidOfferError as error:
        assert "Invalid minutes" in str(error)
        print("Test passed: Invalid arrival minutes rejected.")
        return

    assert False, "Invalid arrival minutes were accepted"


def test_invalid_departure_format():
    try:
        create_test_offer("8:00", "16:00")
    except InvalidOfferError as error:
        assert "Departure time must follow HH:MM format" in str(error)
        print("Test passed: Invalid departure time format rejected.")
        return

    assert False, "Invalid departure time format was accepted"


def test_invalid_arrival_format():
    try:
        create_test_offer("08:00", "abc")
    except InvalidOfferError as error:
        assert "Arrival time must follow HH:MM format" in str(error)
        print("Test passed: Invalid arrival time format rejected.")
        return

    assert False, "Invalid arrival time format was accepted"


print("------- Time validation tests: -------")
test_valid_time()
test_valid_overnight_time()
test_invalid_departure_hours()
test_invalid_departure_minutes()
test_invalid_arrival_hours()
test_invalid_arrival_minutes()
test_invalid_departure_format()
test_invalid_arrival_format()



# TESTING PRICE AND AVAILABLE SEATS

def test_valid_price_and_seats():
    offer = create_test_offer(price=35.50, available_seats=20)

    assert offer.price == 35.50
    assert offer.available_seats == 20

    print("Test passed: Valid price and seats accepted.")


def test_zero_price_and_seats():
    offer = create_test_offer(price=0, available_seats=0)

    assert offer.price == 0
    assert offer.available_seats == 0

    print("Test passed: Zero price and seats accepted.")


def test_invalid_negative_price():
    try:
        create_test_offer(price=-10)
    except InvalidOfferError as error:
        assert "Price must be between" in str(error)
        print("Test passed: Negative price rejected.")
        return

    assert False, "Negative price was accepted"


def test_invalid_high_price():
    try:
        create_test_offer(price=5001)
    except InvalidOfferError as error:
        assert "Price must be between" in str(error)
        print("Test passed: Price above 5000 rejected.")
        return

    assert False, "Price above 5000 was accepted"


def test_invalid_price_type():
    try:
        create_test_offer(price="35.50")
    except InvalidOfferError as error:
        assert "Price must be a number" in str(error)
        print("Test passed: String price rejected.")
        return

    assert False, "String price was accepted"


def test_invalid_boolean_price():
    try:
        create_test_offer(price=True)
    except InvalidOfferError as error:
        assert "Price must be a number" in str(error)
        print("Test passed: Boolean price rejected.")
        return

    assert False, "Boolean price was accepted"


def test_invalid_nan_price():
    try:
        create_test_offer(price=float("nan"))
    except InvalidOfferError as error:
        assert "Price must be a finite number" in str(error)
        print("Test passed: NaN price rejected.")
        return

    assert False, "NaN price was accepted"


def test_invalid_infinite_price():
    try:
        create_test_offer(price=float("inf"))
    except InvalidOfferError as error:
        assert "Price must be a finite number" in str(error)
        print("Test passed: Infinite price rejected.")
        return

    assert False, "Infinite price was accepted"


def test_invalid_negative_seats():
    try:
        create_test_offer(available_seats=-1)
    except InvalidOfferError as error:
        assert "Number of seats must be between" in str(error)
        print("Test passed: Negative seats rejected.")
        return

    assert False, "Negative seats were accepted"


def test_invalid_high_seats():
    try:
        create_test_offer(available_seats=501)
    except InvalidOfferError as error:
        assert "Number of seats must be between" in str(error)
        print("Test passed: More than 500 seats rejected.")
        return

    assert False, "More than 500 seats were accepted"


def test_invalid_fractional_seats():
    try:
        create_test_offer(available_seats=12.5)
    except InvalidOfferError as error:
        assert "Available seats must be an integer" in str(error)
        print("Test passed: Fractional seats rejected.")
        return

    assert False, "Fractional seats were accepted"


def test_invalid_boolean_seats():
    try:
        create_test_offer(available_seats=True)
    except InvalidOfferError as error:
        assert "Available seats must be an integer" in str(error)
        print("Test passed: Boolean seats rejected.")
        return

    assert False, "Boolean seats were accepted"


def test_invalid_nan_seats():
    try:
        create_test_offer(available_seats=float("nan"))
    except InvalidOfferError as error:
        assert "Available seats must be an integer" in str(error)
        print("Test passed: NaN seats rejected.")
        return

    assert False, "NaN seats were accepted"


def test_invalid_infinite_seats():
    try:
        create_test_offer(available_seats=float("inf"))
    except InvalidOfferError as error:
        assert "Available seats must be an integer" in str(error)
        print("Test passed: Infinite seats rejected.")
        return

    assert False, "Infinite seats were accepted"


print("------- Price and seats validation tests: -------")
test_valid_price_and_seats()
test_zero_price_and_seats()
test_invalid_negative_price()
test_invalid_high_price()
test_invalid_price_type()
test_invalid_boolean_price()
test_invalid_nan_price()
test_invalid_infinite_price()
test_invalid_negative_seats()
test_invalid_high_seats()
test_invalid_fractional_seats()
test_invalid_boolean_seats()
test_invalid_nan_seats()
test_invalid_infinite_seats()



# TESTING JOURNEY DURATION CALCULATION

def test_duration_same_day():
    offer = create_test_offer("08:00", "16:00")

    assert offer.calculate_duration_time() == 480
    print("Test passed: Same-day journey duration.")


def test_duration_same_day_with_minutes():
    offer = create_test_offer("08:45", "12:20")

    assert offer.calculate_duration_time() == 215
    print("Test passed: Same-day journey with minutes.")


def test_duration_same_hour():
    offer = create_test_offer("08:15", "08:45")

    assert offer.calculate_duration_time() == 30
    print("Test passed: Same-hour journey duration.")


def test_duration_overnight():
    offer = create_test_offer("22:30", "03:15")

    assert offer.calculate_duration_time() == 285
    print("Test passed: Overnight journey duration.")


def test_duration_overnight_midnight():
    offer = create_test_offer("23:50", "00:10")

    assert offer.calculate_duration_time() == 20
    print("Test passed: Overnight journey across midnight.")


def test_duration_overnight_same_hour():
    offer = create_test_offer("08:45", "08:15")

    assert offer.calculate_duration_time() == 1410
    print("Test passed: Overnight journey with the same hour.")


def test_duration_one_minute():
    offer = create_test_offer("10:00", "10:01")

    assert offer.calculate_duration_time() == 1
    print("Test passed: One-minute journey.")


def test_duration_identical_times():
    try:
        offer = create_test_offer("08:00", "08:00")

    except InvalidOfferError as error:
        assert "Departure and arrival times cannot be identical" in str(error)
        print("Test passed: Identical departure and arrival times rejected.")
        return

    assert False, "Identical departure and arrival times were accepted"


print("------- Journey duration calculation tests: -------")
test_duration_same_day()
test_duration_same_day_with_minutes()
test_duration_same_hour()
test_duration_overnight()
test_duration_overnight_midnight()
test_duration_overnight_same_hour()
test_duration_one_minute()
test_duration_identical_times()


# TESTING ARRIVAL DATE CALCULATION

def test_arrival_date_same_day():
    offer = create_test_offer("08:00", "16:00")

    assert offer.calculate_arrival_date() == "2026-11-15"
    print("Test passed: Same-day arrival date.")


def test_arrival_date_overnight():
    offer = create_test_offer("22:30", "03:15")

    assert offer.calculate_arrival_date() == "2026-11-16"
    print("Test passed: Overnight arrival date.")


def test_arrival_date_same_hour():
    offer = create_test_offer("08:15", "08:45")

    assert offer.calculate_arrival_date() == "2026-11-15"
    print("Test passed: Same-hour arrival date.")


def test_arrival_date_overnight_same_hour():
    offer = create_test_offer("08:45", "08:15")

    assert offer.calculate_arrival_date() == "2026-11-16"
    print("Test passed: Overnight arrival with same hour.")


def test_arrival_date_month_change():
    offer = create_test_offer("23:30", "02:00",
                              travel_date="2026-11-30")

    assert offer.calculate_arrival_date() == "2026-12-01"
    print("Test passed: Month change handled correctly.")

def test_arrival_date_year_change():
    offer = create_test_offer("23:00", "02:00",
                              travel_date="2026-12-31")

    assert offer.calculate_arrival_date() == "2027-01-01"
    print("Test passed: Year change handled correctly.")


def test_arrival_date_leap_year():
    offer = create_test_offer("22:00", "04:00",
                              travel_date="2028-02-28")

    assert offer.calculate_arrival_date() == "2028-02-29"
    print("Test passed: Leap year handled correctly.")


def test_arrival_date_after_leap_day():
    offer = create_test_offer("22:00", "04:00",
                              travel_date="2028-02-29")

    assert offer.calculate_arrival_date() == "2028-03-01"
    print("Test passed: Arrival after leap day.")


def test_arrival_date_non_leap_year():
    offer = create_test_offer("22:00", "04:00",
                              travel_date="2027-02-28")

    assert offer.calculate_arrival_date() == "2027-03-01"
    print("Test passed: Non-leap year handled correctly.")


def test_arrival_date_identical_times():
    try:
        offer = create_test_offer("08:00", "08:00")

    except InvalidOfferError as error:
        assert "Departure and arrival times cannot be identical" in str(error)
        print("Test passed: Identical times rejected.")
        return

    assert False, "Identical departure and arrival times were accepted"


print("------- Arrival date calculation tests: -------")
test_arrival_date_same_day()
test_arrival_date_overnight()
test_arrival_date_same_hour()
test_arrival_date_overnight_same_hour()
test_arrival_date_month_change()
test_arrival_date_year_change()
test_arrival_date_leap_year()
test_arrival_date_after_leap_day()
test_arrival_date_non_leap_year()
test_arrival_date_identical_times()


# TESTING ADDITIONAL BUS OFFER ATTRIBUTES

def test_valid_additional_attributes():
    offer = create_test_offer(
        luggage_included=True,
        transfers=2,
        refundable=False,
        changeable=True
    )

    assert offer.luggage_included is True
    assert offer.transfers == 2
    assert offer.refundable is False
    assert offer.changeable is True

    print("Test passed: Valid additional attributes accepted.")


def test_valid_zero_transfers():
    offer = create_test_offer(transfers=0)

    assert offer.transfers == 0
    print("Test passed: Zero transfers accepted.")


def test_valid_one_transfer():
    offer = create_test_offer(transfers=1)

    assert offer.transfers == 1
    print("Test passed: One transfer accepted.")


def test_invalid_luggage_type():
    try:
        create_test_offer(luggage_included="True")
    except InvalidOfferError as error:
        assert "Luggage must be" in str(error)
        print("Test passed: Invalid luggage type rejected.")
        return

    assert False, "Invalid luggage type was accepted"


def test_invalid_negative_transfers():
    try:
        create_test_offer(transfers=-1)
    except InvalidOfferError as error:
        assert "Transfers must be between" in str(error)
        print("Test passed: Negative transfers rejected.")
        return

    assert False, "Negative transfers were accepted"


def test_invalid_high_transfers():
    try:
        create_test_offer(transfers=3)
    except InvalidOfferError as error:
        assert "Transfers must be between" in str(error)
        print("Test passed: More than two transfers rejected.")
        return

    assert False, "More than two transfers were accepted"


def test_invalid_fractional_transfers():
    try:
        create_test_offer(transfers=1.5)
    except InvalidOfferError as error:
        assert "Transfers must be an integer" in str(error)
        print("Test passed: Fractional transfers rejected.")
        return

    assert False, "Fractional transfers were accepted"


def test_invalid_boolean_transfers():
    try:
        create_test_offer(transfers=True)
    except InvalidOfferError as error:
        assert "Transfers must be an integer" in str(error)
        print("Test passed: Boolean transfers rejected.")
        return

    assert False, "Boolean transfers were accepted"


def test_invalid_string_transfers():
    try:
        create_test_offer(transfers="1")
    except InvalidOfferError as error:
        assert "Transfers must be an integer" in str(error)
        print("Test passed: String transfers rejected.")
        return

    assert False, "String transfers were accepted"


def test_invalid_refundable_type():
    try:
        create_test_offer(refundable="False")
    except InvalidOfferError as error:
        assert "Refundable must be" in str(error)
        print("Test passed: Invalid refundable type rejected.")
        return

    assert False, "Invalid refundable type was accepted"


def test_invalid_changeable_type():
    try:
        create_test_offer(changeable=1)
    except InvalidOfferError as error:
        assert "Changeable must be" in str(error)
        print("Test passed: Invalid changeable type rejected.")
        return

    assert False, "Invalid changeable type was accepted"


def test_valid_false_boolean_attributes():
    offer = create_test_offer(
        luggage_included=False,
        refundable=False,
        changeable=False
    )

    assert offer.luggage_included is False
    assert offer.refundable is False
    assert offer.changeable is False

    print("Test passed: False boolean attributes accepted.")


print("------- Additional BusOffer attributes tests: -------")
test_valid_additional_attributes()
test_valid_zero_transfers()
test_valid_one_transfer()
test_invalid_luggage_type()
test_invalid_negative_transfers()
test_invalid_high_transfers()
test_invalid_fractional_transfers()
test_invalid_boolean_transfers()
test_invalid_string_transfers()
test_invalid_refundable_type()
test_invalid_changeable_type()
test_valid_false_boolean_attributes()

from exceptions import InvalidReviewError


# TESTING CUSTOMER REVIEWS

def test_valid_review():
    review = Review(5, 3, 4, 2)

    assert review.price_rating == 5
    assert review.speed_rating == 3
    assert review.comfort_rating == 4
    assert review.flexibility_rating == 2

    print("Test passed: Valid review created.")


def test_invalid_review_rating():
    try:
        Review(5, 6, 4, 2)
    except InvalidReviewError as error:
        assert "Speed rating must be between 1 and 5" in str(error)
        print("Test passed: Rating above 5 rejected.")
        return

    assert False, "Invalid rating was accepted"


def test_invalid_negative_review_rating():
    try:
        Review(-1, 3, 4, 2)
    except InvalidReviewError as error:
        assert "Price rating must be between 1 and 5" in str(error)
        print("Test passed: Rating below 1 rejected.")
        return

    assert False, "Invalid rating was accepted"


def test_invalid_review_type():
    try:
        Review(5, "3", 4, 2)
    except InvalidReviewError as error:
        assert "Speed rating must be an integer" in str(error)
        print("Test passed: String rating rejected.")
        return

    assert False, "String rating was accepted"


def test_invalid_boolean_review():
    try:
        Review(5, 3, True, 2)
    except InvalidReviewError as error:
        assert "Comfort rating must be an integer" in str(error)
        print("Test passed: Boolean rating rejected.")
        return

    assert False, "Boolean rating was accepted"


def test_add_valid_reviews():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")

    company.add_review(Review(5, 3, 4, 2))
    company.add_review(Review(3, 5, 4, 4))

    assert len(company.reviews) == 2

    print("Test passed: Two reviews added successfully.")


def test_add_invalid_review_object():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")

    try:
        company.add_review("Good journey")
    except InvalidReviewError:
        print("Test passed: Invalid review object rejected.")
        return

    assert False, "Invalid review object was accepted"


def test_average_ratings():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")

    company.add_review(Review(5, 3, 4, 2))
    company.add_review(Review(3, 5, 4, 4))

    averages = company.get_average_ratings()

    assert averages["price"] == 4.0
    assert averages["speed"] == 4.0
    assert averages["comfort"] == 4.0
    assert averages["flexibility"] == 3.0

    print("Test passed: Average ratings calculated correctly.")


def test_no_reviews():
    company = BusCompany("C001", "SolRuta", "Low-cost buses")

    assert company.get_average_ratings() is None

    print("Test passed: Company without reviews handled correctly.")


print("------- Customer review tests: -------")
test_valid_review()
test_invalid_review_rating()
test_invalid_negative_review_rating()
test_invalid_review_type()
test_invalid_boolean_review()
test_add_valid_reviews()
test_add_invalid_review_object()
test_average_ratings()
test_no_reviews()


from offer_generator import generate_offers
def test_offer_generator():
    companies = load_companies("data/companies.csv")
    destinations = load_destinations("data/destinations.csv")

    offers = generate_offers(companies, destinations)

    # Test 1: number of offers
    assert 1350 <= len(offers) <= 2700
    print("PASS: Total generated offers between 1350 and 2700")

    # Test 2: Unique offer IDs
    offer_ids = [offer.offer_id for offer in offers]

    assert len(offer_ids) == len(set(offer_ids))
    print("PASS: All offer IDs are unique")

    # Test 3: Every destination has 3–6 trips per day
    travel_dates = set(offer.travel_date for offer in offers)

    assert len(travel_dates) == 30

    for date in travel_dates:
        for destination in destinations:

            count = sum(
                1 for offer in offers
                if offer.travel_date == date
                and offer.destination.destination_id == destination.destination_id
            )

            assert 3 <= count <= 6

    print("PASS: Every destination has 3–6 trips per day for 30 days")

    # Test 4: Available seats between 0 and 100
    for offer in offers:
        assert 0 <= offer.available_seats <= 100

    print("PASS: Available seats are between 0 and 100")

    # Test 5: Price is positive
    for offer in offers:
        assert 0 < offer.price <= 5000

    print("PASS: All generated prices are valid")

    # Test 6: Duration between 1 minute and 24 hours
    for offer in offers:
        assert 0 < offer.duration_time < 1440

    print("PASS: All generated durations are valid")
    
    # Test 7: Transfers follow company rules
    allowed_transfers = {
        "C001": [0, 1, 2],
        "C002": [0],
        "C003": [0, 1, 2],
        "C004": [0, 1],
        "C005": [0, 1]
    }

    for offer in offers:
        assert offer.transfers in allowed_transfers[offer.company.company_id]

    print("PASS: Transfers follow company rules")

    # Test 8: SolRuta departure hours
    for offer in offers:
        if offer.company.company_id == "C001":
            hour = int(offer.departure_time[:2])
            assert 6 <= hour <= 21

    print("PASS: SolRuta departure hours are valid")

    # Test 9: Camino Express departure hours
    for offer in offers:
        if offer.company.company_id == "C002":
            hour = int(offer.departure_time[:2])
            assert 5 <= hour <= 23

    print("PASS: Camino Express departure hours are valid")

    # Test 10: NocheVia departure hours
    for offer in offers:
        if offer.company.company_id == "C005":
            hour = int(offer.departure_time[:2])
            assert hour >= 20 or hour <= 5

    print("PASS: NocheVia departure hours are valid")

    # Test 11: VerdeBus always includes luggage
    for offer in offers:
        if offer.company.company_id == "C004":
            assert offer.luggage_included is True

    print("PASS: VerdeBus always includes luggage")

    # Test 12: No duplicate trips
    trip_keys = [
        (
            offer.company.company_id,
            offer.destination.destination_id,
            offer.travel_date,
            offer.departure_time
        )
        for offer in offers
    ]

    assert len(trip_keys) == len(set(trip_keys))

    print("PASS: No duplicate trips generated")


    print("\nAll 11 offer generator tests passed!")


test_offer_generator()




from offer_search import search_offers
def test_offer_search():

    companies = load_companies("data/companies.csv")
    destinations = load_destinations("data/destinations.csv")
    offers = generate_offers(companies, destinations)

    test_date = offers[0].travel_date

    # Test 1: Basic destination and date search
    results = search_offers(offers, "Barcelona", test_date)

    assert all(
        offer.destination.name == "Barcelona"
        and offer.travel_date == test_date
        and offer.available_seats > 0
        for offer in results
    )

    print("PASS: Basic destination and date search")

    # Test 2: Maximum price
    results = search_offers(
        offers, "Barcelona", test_date, max_price=50
    )

    assert all(offer.price <= 50 for offer in results)

    print("PASS: Maximum price filter")

    # Test 3: Maximum transfers
    results = search_offers(
        offers, "Barcelona", test_date, max_transfers=0
    )

    assert all(offer.transfers == 0 for offer in results)

    print("PASS: Maximum transfers filter")

    # Test 4: Normal departure window
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="08:00",
        latest_departure="18:00"
    )

    assert all(
        "08:00" <= offer.departure_time <= "18:00"
        for offer in results
    )

    print("PASS: Normal departure window")

    # Test 5: Overnight departure window
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="20:00",
        latest_departure="02:00"
    )

    assert all(
        offer.departure_time >= "20:00"
        or offer.departure_time <= "02:00"
        for offer in results
    )

    print("PASS: Overnight departure window")

    # Test 6: Only earliest departure
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="10:00"
    )

    assert all(
        offer.departure_time >= "10:00"
        for offer in results
    )

    print("PASS: Earliest departure filter")

    # Test 7: Only latest departure
    results = search_offers(
        offers, "Barcelona", test_date,
        latest_departure="14:00"
    )

    assert all(
        offer.departure_time <= "14:00"
        for offer in results
    )

    print("PASS: Latest departure filter")

    # Test 8: Combined filters
    results = search_offers(
        offers, "Barcelona", test_date,
        max_price=100,
        max_transfers=1,
        earliest_departure="08:00",
        latest_departure="18:00"
    )

    assert all(
        offer.price <= 100
        and offer.transfers <= 1
        and "08:00" <= offer.departure_time <= "18:00"
        for offer in results
    )

    print("PASS: Combined search filters")

    print("\nAll 8 offer search tests passed!")

test_offer_search()


def test_offer_id_validation():

    # Test valid offer IDs
    for offer_id in ["O001", "O999", "O1000", "O2700", "O9999"]:
        offer = create_test_offer(offer_id=offer_id)
        assert offer.offer_id == offer_id

    print("PASS: Valid 3- and 4-digit offer IDs")

    # Test invalid offer IDs
    for offer_id in ["O1", "O12", "O10000", "O123456789", "A001"]:
        try:
            create_test_offer(offer_id=offer_id)
            assert False, f"Expected InvalidOfferError for {offer_id}"
        except InvalidOfferError:
            pass

    print("PASS: Invalid offer IDs rejected")



def test_offer_search_fixed():

    # Create four offers with known values
    offers = [
        create_test_offer(
            offer_id="O001",
            departure_time="08:00",
            arrival_time="16:00",
            price=30,
            transfers=0,
            available_seats=20
        ),

        create_test_offer(
            offer_id="O002",
            departure_time="15:00",
            arrival_time="22:00",
            price=60,
            transfers=1,
            available_seats=10
        ),

        create_test_offer(
            offer_id="O003",
            departure_time="22:00",
            arrival_time="06:00",
            price=45,
            transfers=0,
            available_seats=15
        ),

        create_test_offer(
            offer_id="O004",
            departure_time="01:00",
            arrival_time="09:00",
            price=25,
            transfers=2,
            available_seats=0
        )
    ]

    test_date = "2026-11-15"

    # Test 1: Basic search excludes fully booked offers
    results = search_offers(offers, "Barcelona", test_date)

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001", "O002", "O003"}
    print("PASS: Fully booked offers excluded")

    # Test 2: Maximum price
    results = search_offers(
        offers, "Barcelona", test_date, max_price=50
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001", "O003"}
    print("PASS: Maximum price filter with fixed offers")

    # Test 3: Direct buses only
    results = search_offers(
        offers, "Barcelona", test_date, max_transfers=0
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001", "O003"}
    print("PASS: Direct buses filter with fixed offers")

    # Test 4: Normal departure window
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="08:00",
        latest_departure="18:00"
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001", "O002"}
    print("PASS: Normal departure window with fixed offers")

    # Test 5: Overnight departure window
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="20:00",
        latest_departure="02:00"
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O003"}
    print("PASS: Overnight departure window with fixed offers")

    # Test 6: Only earliest departure
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="10:00"
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O002", "O003"}
    print("PASS: Earliest departure with fixed offers")

    # Test 7: Only latest departure
    results = search_offers(
        offers, "Barcelona", test_date,
        latest_departure="14:00"
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001"}
    print("PASS: Latest departure with fixed offers")

    # Test 8: Combined filters
    results = search_offers(
        offers, "Barcelona", test_date,
        max_price=50,
        max_transfers=0,
        earliest_departure="08:00",
        latest_departure="18:00"
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001"}
    print("PASS: Combined filters with fixed offers")

    print("\nAll 8 fixed search tests passed!")


def test_max_duration_filter():

    offers = [
        create_test_offer(
            offer_id="O001",
            departure_time="08:00",
            arrival_time="12:00"
        ),

        create_test_offer(
            offer_id="O002",
            departure_time="08:00",
            arrival_time="14:00"
        ),

        create_test_offer(
            offer_id="O003",
            departure_time="08:00",
            arrival_time="17:00"
        )
    ]

    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-15",
        max_duration=360
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001", "O002"}

    print("PASS: Maximum duration filter with fixed offers")


def test_required_luggage_filter():

    offers = [
        create_test_offer(
            offer_id="O001",
            luggage_included=True
        ),

        create_test_offer(
            offer_id="O002",
            luggage_included=False
        ),

        create_test_offer(
            offer_id="O003",
            luggage_included=True
        )
    ]

    # Luggage is required
    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-15",
        required_luggage=True
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001", "O003"}
    print("PASS: Required luggage filter")

    # Luggage is not required
    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-15",
        required_luggage=False
    )

    result_ids = {offer.offer_id for offer in results}

    assert result_ids == {"O001", "O002", "O003"}
    print("PASS: Optional luggage allows all offers")

def test_ticket_flexibility_filters():

    offers = [
        create_test_offer(
            offer_id="O001",
            changeable=True,
            refundable=True
        ),

        create_test_offer(
            offer_id="O002",
            changeable=True,
            refundable=False
        ),

        create_test_offer(
            offer_id="O003",
            changeable=False,
            refundable=True
        ),

        create_test_offer(
            offer_id="O004",
            changeable=False,
            refundable=False
        )
    ]

    # Test 1: Changeable ticket required
    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-15",
        required_changeable=True
    )

    assert {offer.offer_id for offer in results} == {"O001", "O002"}
    print("PASS: Required changeable ticket filter")

    # Test 2: Refundable ticket required
    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-15",
        required_refundable=True
    )

    assert {offer.offer_id for offer in results} == {"O001", "O003"}
    print("PASS: Required refundable ticket filter")

    # Test 3: Both conditions required
    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-15",
        required_changeable=True,
        required_refundable=True
    )

    assert {offer.offer_id for offer in results} == {"O001"}
    print("PASS: Both ticket flexibility requirements")

    # Test 4: Neither condition required
    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-15",
        required_changeable=False,
        required_refundable=False
    )

    assert {offer.offer_id for offer in results} == {
        "O001", "O002", "O003", "O004"
    }
    print("PASS: No mandatory ticket flexibility requirements")


def test_travel_date_window():

    offers = [
        create_test_offer(
            offer_id="O001",
            travel_date="2026-11-12"
        ),
        create_test_offer(
            offer_id="O002",
            travel_date="2026-11-13"
        ),
        create_test_offer(
            offer_id="O003",
            travel_date="2026-11-14"
        ),
        create_test_offer(
            offer_id="O004",
            travel_date="2026-11-15"
        )
    ]

    # Test 1: Search between November 12 and 14
    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-12",
        end_date="2026-11-14"
    )

    assert {offer.offer_id for offer in results} == {
        "O001", "O002", "O003"
    }

    print("PASS: Travel date window")

    # Test 2: Search only one date
    results = search_offers(
        offers,
        "Barcelona",
        "2026-11-13"
    )

    assert {offer.offer_id for offer in results} == {"O002"}

    print("PASS: Exact travel date still works")



from offer_ranking import (
    calculate_price_score,
    calculate_duration_score,
    calculate_time_score,
    calculate_flexibility_score
)

def test_price_normalization():

    # Test 1: Cheapest ticket gets 100 points
    assert calculate_price_score(20, 20) == 100

    # Test 2: More expensive tickets get lower scores
    assert calculate_price_score(40, 20) == 50

    # Test 3: Check a decimal result
    assert abs(calculate_price_score(60, 20) - 33.3333) < 0.001

    # Test 4: Invalid price
    try:
        calculate_price_score(0, 20)
        assert False, "Expected ValueError for zero price"
    except ValueError:
        pass

    print("PASS: Price normalization tests")

def test_duration_normalization():

    # Shortest journey gets 100 points
    assert calculate_duration_score(240, 240) == 100

    # Longer journey gets a lower score
    assert abs(calculate_duration_score(360, 240) - 66.6667) < 0.001

    # Journey twice as long gets 50 points
    assert calculate_duration_score(480, 240) == 50

    # Invalid duration
    try:
        calculate_duration_score(0, 240)
        assert False, "Expected ValueError for zero duration"
    except ValueError:
        pass

    print("PASS: Duration normalization tests")

def test_time_normalization():

    assert calculate_time_score("10:00", "10:00") == 100
    assert calculate_time_score("09:00", "10:00") == 80
    assert calculate_time_score("12:00", "10:00") == 60
    assert calculate_time_score("15:00", "10:00") == 0
    assert calculate_time_score("18:00", "10:00") == 0
    # Overnight departures
    assert calculate_time_score("01:00", "23:00") == 60
    assert calculate_time_score("00:30", "23:30") == 80
    assert calculate_time_score("23:00", "01:00") == 60

    print("PASS: Departure-time normalization tests")


def test_flexibility_normalization():

    assert calculate_flexibility_score(True, True) == 100
    assert calculate_flexibility_score(True, False) == 50
    assert calculate_flexibility_score(False, True) == 50
    assert calculate_flexibility_score(False, False) == 0

    print("PASS: Ticket flexibility normalization tests")


from offer_ranking import validate_weights, calculate_weighted_score, rank_offers
def test_weighted_scoring():

    # Test 1: Valid weights
    assert validate_weights(0.40, 0.25, 0.15, 0.20) == True

    # Test 2: Weighted score calculation
    score = calculate_weighted_score(80, 90, 60, 100)

    assert abs(score - 83.5) < 0.000001

    # Test 3: Custom weights
    score = calculate_weighted_score(
        80, 90, 60, 100,
        w_price=0.60,
        w_duration=0.20,
        w_time=0.10,
        w_flexibility=0.10
    )

    assert abs(score - 82.0) < 0.000001

    # Test 4: Weights do not add up to 100%
    try:
        validate_weights(0.40, 0.20, 0.10, 0.10)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for invalid total weights"

    # Test 5: Negative weight
    try:
        validate_weights(-0.10, 0.50, 0.30, 0.30)
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError for negative weight"

    print("PASS: Weighted scoring and weight validation tests")

def test_ranking_empty_offers():

    results = rank_offers([], preferred_time="10:00")

    assert results == []

    print("PASS: Empty ranking handled correctly")

def test_ranking_fixed_offers():

    offers = [
        create_test_offer(
            offer_id="O001",
            price=20,
            departure_time="10:00",
            arrival_time="14:00",
            changeable=True,
            refundable=True
        ),

        create_test_offer(
            offer_id="O002",
            price=40,
            departure_time="12:00",
            arrival_time="18:00",
            changeable=False,
            refundable=False
        ),

        create_test_offer(
            offer_id="O003",
            price=30,
            departure_time="11:00",
            arrival_time="16:00",
            changeable=True,
            refundable=False
        )
    ]

    ranked = rank_offers(offers, preferred_time="10:00")

    # Check that all offers are included
    assert len(ranked) == 3

    # Check that offers are sorted by total score
    scores = [item["total_score"] for item in ranked]

    assert scores == sorted(scores, reverse=True)

    # Check that the expected offer ranks first
    assert ranked[0]["offer"].offer_id == "O001"

    # Check that all four criterion scores are stored
    for item in ranked:
        assert 0 <= item["price_score"] <= 100
        assert 0 <= item["duration_score"] <= 100
        assert 0 <= item["time_score"] <= 100
        assert 0 <= item["flexibility_score"] <= 100
        assert 0 <= item["total_score"] <= 100

    print("PASS: Fixed offer ranking tests")

def test_ranking_different_weights():

    offers = [
        create_test_offer(
            offer_id="O001",
            price=20,
            departure_time="08:00",
            arrival_time="16:00",
            changeable=False,
            refundable=False
        ),

        create_test_offer(
            offer_id="O002",
            price=50,
            departure_time="10:00",
            arrival_time="14:00",
            changeable=True,
            refundable=True
        )
    ]

    # Budget traveller: price is most important
    budget_ranking = rank_offers(
        offers,
        preferred_time="10:00",
        w_price=0.70,
        w_duration=0.10,
        w_time=0.10,
        w_flexibility=0.10
    )

    # Business traveller: duration and departure time matter more
    business_ranking = rank_offers(
        offers,
        preferred_time="10:00",
        w_price=0.10,
        w_duration=0.40,
        w_time=0.40,
        w_flexibility=0.10
    )

    assert budget_ranking[0]["offer"].offer_id == "O001"
    assert business_ranking[0]["offer"].offer_id == "O002"

    print("PASS: Different weights produce different recommendations")


from offer_ranking import TRAVELLER_PROFILES, rank_offers_by_profile, explain_offer
def test_traveller_profiles():
    offers = [
        create_test_offer(
            offer_id="O001",
            price=20,
            departure_time="08:00",
            arrival_time="16:00",
            changeable=False,
            refundable=False
        ),

        create_test_offer(
            offer_id="O002",
            price=50,
            departure_time="10:00",
            arrival_time="14:00",
            changeable=True,
            refundable=True
        )
    ]

    for profile_name in TRAVELLER_PROFILES:

        ranked = rank_offers_by_profile(
            offers,
            preferred_time="10:00",
            profile_name=profile_name
        )

        assert len(ranked) == 2

        print(
            f"Profile: {profile_name} | "
            f"Recommended offer: {ranked[0]['offer'].offer_id} | "
            f"Score: {ranked[0]['total_score']:.2f}"
        )

    print("PASS: Traveller profile ranking tests")


def test_three_traveller_recommendations():
    offers = [
        # Cheapest, but slow and not flexible
        create_test_offer(
            offer_id="O001",
            price=20,
            departure_time="06:00",
            arrival_time="14:00",
            changeable=False,
            refundable=False
        ),

        # Fastest and closest to preferred departure time
        create_test_offer(
            offer_id="O002",
            price=50,
            departure_time="10:00",
            arrival_time="13:00",
            changeable=False,
            refundable=False
        ),

        # Fully flexible, but more expensive and slower
        create_test_offer(
            offer_id="O003",
            price=60,
            departure_time="07:00",
            arrival_time="13:00",
            changeable=True,
            refundable=True
        )
    ]

    expected_winners = {
        "budget": "O001",
        "business": "O002",
        "flexible_tourist": "O003"
    }

    for profile_name, expected_id in expected_winners.items():
        ranked = rank_offers_by_profile(
            offers,
            preferred_time="10:00",
            profile_name=profile_name
        )

        winner = ranked[0]

        assert winner["offer"].offer_id == expected_id

        print(
            f"{profile_name}: "
            f"{winner['offer'].offer_id} "
            f"(score: {winner['total_score']:.2f})"
        )

    print("PASS: Three traveller profiles recommend different offers")


def test_offer_explanation():
    offer = create_test_offer(
        offer_id="O001",
        price=20,
        departure_time="06:00",
        arrival_time="14:00",
        changeable=False,
        refundable=False
    )

    ranked = rank_offers(
        [offer],
        preferred_time="10:00"
    )

    explanation = explain_offer(ranked[0])

    assert "Competitive ticket price" in explanation["advantages"]
    assert "Ticket cannot be changed" in explanation["disadvantages"]
    assert "Ticket is non-refundable" in explanation["disadvantages"]

    print("PASS: Offer explanation test")

def test_offer_explanation_multiple_offers():

    offers = [
        create_test_offer(
            offer_id="O001",
            price=20,
            departure_time="06:00",
            arrival_time="14:00",
            changeable=False,
            refundable=False
        ),

        create_test_offer(
            offer_id="O002",
            price=60,
            departure_time="10:00",
            arrival_time="13:00",
            changeable=True,
            refundable=True
        )
    ]

    ranked = rank_offers(
        offers,
        preferred_time="10:00"
    )

    # Find O002 in the ranked results
    ranked_offer = next(
        item for item in ranked
        if item["offer"].offer_id == "O002"
    )

    explanation = explain_offer(ranked_offer)

    assert "Relatively expensive ticket" in explanation["disadvantages"]
    assert "Short journey duration" in explanation["advantages"]
    assert "Convenient departure time" in explanation["advantages"]
    assert "Ticket can be changed" in explanation["advantages"]
    assert "Ticket is refundable" in explanation["advantages"]

    print("PASS: Explanation with competing offers")


from unittest.mock import patch
from main import get_custom_weights, get_preferred_time, load_or_generate_offers
from datetime import datetime, date, timedelta

def test_preferred_time_input():

    # Valid time
    with patch("builtins.input", side_effect=["09:30"]):
        assert get_preferred_time() == "09:30"

    # Invalid inputs followed by valid input
    with patch("builtins.input", side_effect=[
        "25:00", "hello", "9:30", "14:45"
    ]):
        assert get_preferred_time() == "14:45"

    # Cancellation
    with patch("builtins.input", side_effect=["c"]):
        assert get_preferred_time() is None

    print("PASS: Preferred departure time input tests")

def test_custom_weights_input():

    # Valid percentages
    with patch("builtins.input", side_effect=[
        "40", "20", "20", "20"
    ]):
        weights = get_custom_weights()

    assert weights == {
        "w_price": 0.40,
        "w_duration": 0.20,
        "w_time": 0.20,
        "w_flexibility": 0.20
    }

    # Invalid inputs, then valid percentages
    with patch("builtins.input", side_effect=[
        "hello", "-10", "40", "20", "20", "20"
    ]):
        weights = get_custom_weights()

    assert weights["w_price"] == 0.40

    # Exceeding 100% restarts the process
    with patch("builtins.input", side_effect=[
        "60", "60",
        "25", "25", "25", "25"
    ]):
        weights = get_custom_weights()

    assert weights["w_price"] == 0.25
    assert sum(weights.values()) == 1.0

    # Total below 100% restarts the process
    with patch("builtins.input", side_effect=[
        "20", "20", "20", "20",
        "40", "20", "20", "20"
    ]):
        weights = get_custom_weights()

    assert weights["w_price"] == 0.40

    # Cancellation
    with patch("builtins.input", side_effect=["40", "c"]):
        assert get_custom_weights() is None

    print("PASS: Custom ranking preferences input tests")


def test_past_departures_are_excluded():

    companies = load_companies("data/companies.csv")
    destinations = load_destinations("data/destinations.csv")

    company = companies[0]
    destination = destinations[0]

    #test_date = date(2026, 10, 30)
    test_date = "2026-10-30"

    past_offer = BusOffer(
        "O901", company, destination, test_date,
        "09:00", "12:00", 20.0, 10,
        True, 0, False, False
    )

    future_offer = BusOffer(
        "O902", company, destination, test_date,
        "15:00", "18:00", 30.0, 10,
        True, 0, False, False
    )

    offers = [past_offer, future_offer]

    results = search_offers(
        offers,
        destination.name,
        test_date,
        current_datetime=datetime(2026, 10, 30, 10, 0)
    )

    assert len(results) == 1
    assert results[0].offer_id == "O902"

    print("PASS: Past departures are excluded")


from contextlib import redirect_stdout
from io import StringIO
from main import display_ranked_offers

def test_display_ranked_offers_empty():

    output = StringIO()

    with redirect_stdout(output):
        display_ranked_offers([])

    printed_text = output.getvalue()

    assert "No bus offers available to rank." in printed_text

    print("PASS: Empty ranked offers display")


def test_display_ranked_offers_with_explanation():

    companies = load_companies("data/companies.csv")
    destinations = load_destinations("data/destinations.csv")

    company = companies[0]
    destination = destinations[0]

    offer = BusOffer(
        "O951", company, destination, "2026-11-15",
        "09:00", "12:00", 25.0, 10,
        True, 0, True, True
    )

    ranked = rank_offers(
        [offer],
        preferred_time="09:00"
    )

    output = StringIO()

    with redirect_stdout(output):
        display_ranked_offers(ranked)

    printed_text = output.getvalue()

    assert "O951" in printed_text
    assert "Score: 100.00/100" in printed_text
    assert "Why We Recommend the Top Offer" in printed_text

    assert "Competitive ticket price" in printed_text
    assert "Short journey duration" in printed_text
    assert "Convenient departure time" in printed_text
    assert "Ticket can be changed" in printed_text
    assert "Ticket is refundable" in printed_text

    print("PASS: Ranked offers display with explanation")

# TESTING THE MENU:
from offer_search import search_offers as filter_offers
from datetime import datetime


def create_filter_test_data():
    company = BusCompany(
        "C001",
        "SolRuta",
        "Very comfy")
    destination = Destination(
        "D001",
        "Barcelona",
        "Catalonia")

    offers = create_filter_test_offers(company, destination)

    return offers

def create_filter_test_offers(company, destination):
    return [
        BusOffer(
            "O901", company, destination,
            "2026-11-15", "08:00", "12:00",
            30, 10, True, 0, True, True),

        BusOffer(
            "O902", company, destination,
            "2026-11-15", "10:00", "15:00",
            50, 10, True, 1, False, False),

        BusOffer(
            "O903", company, destination,
            "2026-11-15", "14:00", "20:00",
            80, 10, False, 2, True, False),

        BusOffer(
            "O904", company, destination,
            "2026-11-15", "23:00", "03:00",
            40, 10, True, 0, True, True)]

def test_combined_filters():
    offers = create_filter_test_data()
    results = filter_offers(
        offers,
        "Barcelona",
        "2026-11-15",
        max_price=60,
        max_transfers=0,
        max_duration=300,
        required_luggage=True,
        required_changeable=True,
        required_refundable=True,
        earliest_departure="07:00",
        latest_departure="12:00",
        current_datetime=datetime(2026, 11, 1)
    )

    assert [offer.offer_id for offer in results] == ["O901"]


def test_remove_one_filter():
    offers = create_filter_test_data()

    active_filters = {
        "max_price": 35,
        "max_transfers": 0,
        "required_luggage": True
    }

    before = filter_offers(
        offers, "Barcelona", "2026-11-15",
        current_datetime=datetime(2026, 11, 1),
        **active_filters
    )

    assert [offer.offer_id for offer in before] == ["O901"]

    # Remove only the price filter
    active_filters["max_price"] = None

    after = filter_offers(
        offers, "Barcelona", "2026-11-15",
        current_datetime=datetime(2026, 11, 1),
        **active_filters
    )

    assert {offer.offer_id for offer in after} == {"O901", "O904"}
    assert active_filters["max_transfers"] == 0
    assert active_filters["required_luggage"] is True


def test_clear_all_filters():
    offers = create_filter_test_data()

    active_filters = {
        "max_price": 35,
        "max_transfers": 0,
        "required_luggage": True
    }

    for key in active_filters:
        active_filters[key] = None

    results = filter_offers(
        offers, "Barcelona", "2026-11-15",
        current_datetime=datetime(2026, 11, 1),
        **active_filters
    )

    assert {offer.offer_id for offer in results} == {
        "O901", "O902", "O903", "O904"
    }


def test_remove_earliest_departure():
    offers = create_filter_test_data()

    active_filters = {
        "earliest_departure": "09:00",
        "latest_departure": "15:00"
    }

    before = filter_offers(
        offers, "Barcelona", "2026-11-15",
        current_datetime=datetime(2026, 11, 1),
        **active_filters
    )

    assert {offer.offer_id for offer in before} == {"O902", "O903"}

    # Remove only earliest departure
    active_filters["earliest_departure"] = None

    after = filter_offers(
        offers, "Barcelona", "2026-11-15",
        current_datetime=datetime(2026, 11, 1),
        **active_filters
    )

    assert {offer.offer_id for offer in after} == {
        "O901", "O902", "O903"
    }

    assert active_filters["latest_departure"] == "15:00"


# SAVING AND LOADING THE TRIPS:
from csv_loader import save_offers, load_offers, load_bookings
from tempfile import TemporaryDirectory
from pathlib import Path
from main import confirm_booking

def test_save_and_load_offers():

    offers = create_filter_test_data()

    companies = [offers[0].company]
    destinations = [offers[0].destination]

    with TemporaryDirectory() as temp_dir:

        file_path = Path(temp_dir) / "offers.csv"

        save_offers(offers, file_path)
        loaded_offers = load_offers(
            companies,
            destinations,
            file_path
        )

        assert len(loaded_offers) == len(offers)

        for original, loaded in zip(offers, loaded_offers):
            assert original.offer_id == loaded.offer_id
            assert original.travel_date == loaded.travel_date
            assert original.price == loaded.price
            assert original.available_seats == loaded.available_seats
            assert original.company.name == loaded.company.name
            assert original.destination.name == loaded.destination.name
            assert original.luggage_included == loaded.luggage_included
            assert original.transfers == loaded.transfers
            assert original.refundable == loaded.refundable
            assert original.changeable == loaded.changeable

    print("PASS: Save and load bus offers")

def test_generate_offers_custom_dates():

    companies = [
        BusCompany("C001", "SolRuta", "Fictional Spanish bus company")
    ]

    destinations = [
        Destination("D001", "Barcelona", "Catalonia")
    ]

    offers = generate_offers(
        companies,
        destinations,
        start_date=date(2026, 12, 2),
        number_of_days=3,
        starting_offer_id=2501
    )

    assert len(offers) >= 9

    assert offers[0].offer_id == "O2501"

    assert offers[0].travel_date == "2026-12-02"

    assert offers[-1].travel_date == "2026-12-04"

    assert len({offer.offer_id for offer in offers}) == len(offers)

    print("PASS: Generate offers with custom dates and IDs")

import csv

def test_offer_generation_extension():

    companies = [
        BusCompany("C001", "SolRuta", "Fictional Spanish bus company")
    ]

    destinations = [
        Destination("D001", "Barcelona", "Catalonia")
    ]

    # Create an old batch ending tomorrow.
    # This should trigger the generation of 28 additional days.
    last_date = date.today() + timedelta(days=1)

    existing_offers = generate_offers(
        companies,
        destinations,
        start_date=last_date,
        number_of_days=1,
        starting_offer_id=100
    )

    original_count = len(existing_offers)
    original_ids = {offer.offer_id for offer in existing_offers}

    with TemporaryDirectory() as temp_dir:

        file_path = Path(temp_dir) / "offers.csv"

        save_offers(existing_offers, file_path)

        # Run the same function used by main.py
        updated_offers = load_or_generate_offers(
            companies,
            destinations,
            file_path=file_path
        )

        # Existing offers must remain
        assert len(updated_offers) > original_count

        updated_ids = {offer.offer_id for offer in updated_offers}

        assert original_ids.issubset(updated_ids)

        # Every offer must have a unique ID
        assert len(updated_ids) == len(updated_offers)

        # New offers must start after the old date
        new_offers = [
            offer for offer in updated_offers
            if offer.offer_id not in original_ids
        ]

        assert min(offer.travel_date for offer in new_offers) == (
            last_date + timedelta(days=1)
        ).isoformat()

        assert max(offer.travel_date for offer in new_offers) == (
            last_date + timedelta(days=28)
        ).isoformat()

        # New IDs must continue after the existing IDs
        highest_old_id = max(
            int(offer.offer_id[1:])
            for offer in existing_offers
        )

        lowest_new_id = min(
            int(offer.offer_id[1:])
            for offer in new_offers
        )

        assert lowest_new_id == highest_old_id + 1

        # Confirm that all updated offers were saved
        saved_offers = load_offers(
            companies,
            destinations,
            file_path
        )

        assert len(saved_offers) == len(updated_offers)

    print("PASS: Automatic 28-day offer generation extension")

from booking import Booking
from csv_loader import save_bookings


def test_save_bookings():

    offers = create_filter_test_data()

    booking = Booking(
        "B80000000",
        offers[0],
        "Test Passenger"
    )

    with TemporaryDirectory() as temp_dir:

        file_path = Path(temp_dir) / "bookings.csv"

        save_bookings([booking], file_path)

        assert file_path.exists()

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0]["booking_reference"] == "B80000000"
        assert rows[0]["offer_id"] == offers[0].offer_id
        assert rows[0]["passenger_name"] == "Test Passenger"

    print("PASS: Save bookings to CSV")


from csv_loader import load_bookings
from booking import get_next_booking_number, generate_booking_reference

def test_save_and_load_bookings():

    offers = create_filter_test_data()

    booking1 = Booking(
        "B80000000",
        offers[0],
        "Passenger One"
    )

    booking2 = Booking(
        "B80000001",
        offers[1],
        "Passenger Two"
    )

    with TemporaryDirectory() as temp_dir:

        file_path = Path(temp_dir) / "bookings.csv"

        save_bookings([booking1, booking2], file_path)

        loaded_bookings = load_bookings(offers, file_path)

        assert len(loaded_bookings) == 2

        assert loaded_bookings[0].booking_reference == "B80000000"
        assert loaded_bookings[0].passenger_name == "Passenger One"
        assert loaded_bookings[0].offer.offer_id == offers[0].offer_id

        assert loaded_bookings[1].booking_reference == "B80000001"
        assert loaded_bookings[1].passenger_name == "Passenger Two"
        assert loaded_bookings[1].offer.offer_id == offers[1].offer_id

    print("PASS: Save and load bookings")

def test_next_booking_number():

    offers = create_filter_test_data()

    # No existing bookings
    assert get_next_booking_number([]) == 0

    # Existing bookings
    bookings = [
        Booking("B80000000", offers[0], "Passenger One"),
        Booking("B80000005", offers[1], "Passenger Two"),
        Booking("B80000003", offers[2], "Passenger Three")
    ]

    next_number = get_next_booking_number(bookings)

    assert next_number == 6

    next_reference = generate_booking_reference(next_number)

    assert next_reference == "B80000006"

    print("PASS: Generate next booking reference")

def test_confirm_booking():

    offers = create_filter_test_data()
    offer = offers[0]

    companies = [offer.company]
    destinations = [offer.destination]

    bookings = []
    original_seats = offer.available_seats

    with TemporaryDirectory() as temp_dir:

        bookings_path = Path(temp_dir) / "bookings.csv"
        offers_path = Path(temp_dir) / "offers.csv"

        # TEST 1: Successful booking
        with patch("builtins.input", side_effect=["Anna Smith", "y"]):

            booking = confirm_booking(
                offer,
                bookings,
                offers,
                bookings_path,
                offers_path
            )

        assert booking is not None
        assert booking.booking_reference == "B80000000"
        assert booking.passenger_name == "Anna Smith"
        assert offer.available_seats == original_seats - 1
        assert len(bookings) == 1

        # Check that the booking was saved
        saved_bookings = load_bookings(offers, bookings_path)

        assert len(saved_bookings) == 1
        assert saved_bookings[0].booking_reference == "B80000000"

        # Check that the updated seats were saved
        saved_offers = load_offers(
            companies,
            destinations,
            offers_path
        )

        saved_offer = next(
            item for item in saved_offers
            if item.offer_id == offer.offer_id
        )

        assert saved_offer.available_seats == original_seats - 1

        # TEST 2: Cancel booking
        seats_before = offer.available_seats

        with patch("builtins.input", side_effect=["c"]):

            cancelled = confirm_booking(
                offer,
                bookings,
                offers,
                bookings_path,
                offers_path
            )

        assert cancelled is None
        assert offer.available_seats == seats_before
        assert len(bookings) == 1

        # TEST 3: Sold-out offer
        offer.available_seats = 0

        sold_out = confirm_booking(
            offer,
            bookings,
            offers,
            bookings_path,
            offers_path
        )

        assert sold_out is None
        assert len(bookings) == 1

    print("PASS: Booking confirmation, cancellation and sold-out checks")

def test_booking_save_error():

    offers = create_filter_test_data()
    offer = offers[0]
    bookings = []

    original_seats = offer.available_seats

    with patch("builtins.input", side_effect=["Anna Smith", "y"]):
        with patch("main.save_bookings", side_effect=OSError("Test saving error")):

            booking = confirm_booking(offer, bookings, offers)

    assert booking is None
    assert len(bookings) == 0
    assert offer.available_seats == original_seats

    print("PASS: Booking saving error handling")


def test_offer_save_error():

    offers = create_filter_test_data()
    offer = offers[0]
    bookings = []

    original_seats = offer.available_seats

    with patch("builtins.input", side_effect=["Anna Smith", "y"]):
        with patch("main.save_bookings"):
            with patch(
                "main.save_offers",
                side_effect=OSError("Test offers saving error")
            ):
                booking = confirm_booking(offer, bookings, offers)

    assert booking is None
    assert len(bookings) == 0
    assert offer.available_seats == original_seats

    print("PASS: Offer saving error handling")

# testing some invalid values
from csv_loader import parse_boolean
def test_parse_boolean():

    assert parse_boolean("True") is True
    assert parse_boolean("False") is False

    try:
        parse_boolean("unknown")
    except ValueError:
        pass
    else:
        assert False, "Invalid boolean value was accepted"

    print("PASS: Boolean CSV validation")

# testing duplicate ids
def test_duplicate_offer_ids():

    offers = create_filter_test_data()
    offer = offers[0]

    companies = [offer.company]
    destinations = [offer.destination]

    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "offers.csv"

        # Save the same offer twice
        save_offers([offer, offer], file_path)

        try:
            load_offers(companies, destinations, file_path)
        except ValueError as error:
            assert "Duplicate offer ID" in str(error)
        else:
            assert False, "Duplicate offer ID was accepted"

    print("PASS: Duplicate offer ID validation")

def test_invalid_offer_csv_row():

    offers = create_filter_test_data()
    offer = offers[0]

    companies = [offer.company]
    destinations = [offer.destination]

    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "offers.csv"

        save_offers([offer], file_path)

        # Change the price in the CSV to an invalid value
        content = file_path.read_text(encoding="utf-8")
        content = content.replace(
            str(offer.price),
            "invalid_price"
        )
        file_path.write_text(content, encoding="utf-8")

        try:
            load_offers(companies, destinations, file_path)
        except ValueError as error:
            assert "CSV row 2" in str(error)
        else:
            assert False, "Invalid CSV row was accepted"

    print("PASS: Invalid CSV row error message")

def test_booking_fare_conditions():

    offers = create_filter_test_data()
    offer = offers[0]

    booking = Booking(
        booking_reference="B80000001",
        offer=offer,
        passenger_name="Test Passenger"
    )

    # Remember the original conditions
    original_luggage = booking.luggage_included
    original_refundable = booking.refundable
    original_changeable = booking.changeable

    with TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "bookings.csv"

        save_bookings([booking], file_path)

        # Change the conditions of the original offer
        offer.luggage_included = not original_luggage
        offer.refundable = not original_refundable
        offer.changeable = not original_changeable

        loaded_bookings = load_bookings([offer], file_path)
        loaded_booking = loaded_bookings[0]

        assert loaded_booking.luggage_included == original_luggage
        assert loaded_booking.refundable == original_refundable
        assert loaded_booking.changeable == original_changeable

    print("PASS: Booking fare conditions preserved")

# some additional tests to make sure we meet the requirements:
def test_invalid_ranking_weights():
    from offer_ranking import validate_weights

    for invalid_weight in [float("nan"), float("inf")]:
        try:
            validate_weights(invalid_weight, 0.25, 0.25, 0.25)
        except ValueError:
            pass
        else:
            assert False, f"Invalid weight accepted: {invalid_weight}"

    print("PASS: Invalid ranking weights")

def test_explanation_edge_cases():
    from offer_ranking import explain_offer

    offers = create_filter_test_data()
    offer = offers[0]

    ranked_offer = {
        "offer": offer,
        "price_score": 60,
        "duration_score": 60,
        "time_score": 60
    }

    offer.changeable = False
    offer.refundable = False

    explanation = explain_offer(ranked_offer)

    assert len(explanation["advantages"]) > 0
    assert len(explanation["disadvantages"]) > 0

    print("PASS: Explanation edge cases")

if __name__ == "__main__":
    test_offer_id_validation()
    test_offer_search_fixed()
    test_max_duration_filter()
    test_required_luggage_filter()
    test_ticket_flexibility_filters()
    test_travel_date_window()
    test_price_normalization()
    test_duration_normalization()
    test_time_normalization()
    test_flexibility_normalization()
    test_weighted_scoring()
    test_ranking_empty_offers()
    test_ranking_fixed_offers()
    test_ranking_different_weights()
    test_traveller_profiles()
    test_three_traveller_recommendations()
    test_offer_explanation()
    test_offer_explanation_multiple_offers()
    
    # testing user input menu:
    test_preferred_time_input()
    test_custom_weights_input()

    # testing current time:
    test_past_departures_are_excluded()

    # testing explanations for the sorted tickets:
    test_display_ranked_offers_empty()
    test_display_ranked_offers_with_explanation()

    # testing interactive menu window:
    test_combined_filters()
    test_remove_one_filter()
    test_clear_all_filters()
    test_remove_earliest_departure()

    # saving and loading trips:
    test_save_and_load_offers()
    test_generate_offers_custom_dates()
    test_offer_generation_extension()
    test_save_bookings()
    test_save_and_load_bookings()
    test_next_booking_number()
    test_confirm_booking()
    test_booking_save_error()
    test_offer_save_error()

    test_parse_boolean()
    # duplicate ids
    test_duplicate_offer_ids()

    test_invalid_offer_csv_row()
    test_booking_fare_conditions()

    test_invalid_ranking_weights()
    test_explanation_edge_cases()