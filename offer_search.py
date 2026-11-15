from datetime import datetime

def search_offers(offers, destination_name, travel_date,
                  max_price=None, max_transfers=None,
                  earliest_departure=None, latest_departure=None,
                  max_duration=None, required_luggage=None,
                  required_changeable=None, required_refundable=None,
                  end_date=None, current_datetime=None):

    if current_datetime is None:
        current_datetime = datetime.now()

    if end_date is None:
        end_date = travel_date

    matching_offers = []

    for offer in offers:
        # Convert the date if it is stored as a string
        if isinstance(offer.travel_date, str):
            departure_date = datetime.strptime(
                offer.travel_date, "%Y-%m-%d"
            ).date()
        else:
            departure_date = offer.travel_date

        departure_datetime = datetime.combine(
            departure_date,
            datetime.strptime(offer.departure_time, "%H:%M").time()
        )
        if departure_datetime <= current_datetime:
            continue

        if (
            offer.destination.name.lower() == destination_name.lower()
            and travel_date <= offer.travel_date <= end_date
            and offer.available_seats > 0
        ):

            # Optional price filter
            if max_price is not None and offer.price > max_price:
                continue
            # if max_price = 300 and offer has a higher price -> skip this offer

            # Optional transfers filter
            if max_transfers is not None and offer.transfers > max_transfers:
                continue
            # Optional maximum journey duration filter
            if max_duration is not None and offer.duration_time > max_duration:
                continue

            # Optional required luggage filter
            if required_luggage is True and offer.luggage_included == False:
                continue

            # Optional required changeable ticket filter
            if required_changeable is True and offer.changeable == False:
                continue

            # Optional required refundable ticket filter
            if required_refundable == True and offer.refundable == False:
                continue

            # Both departure times provided
            if earliest_departure is not None and latest_departure is not None:

                if earliest_departure <= latest_departure:
                    # Normal window: 08:00 to 18:00
                    if not (earliest_departure <= offer.departure_time <= latest_departure):
                        continue

                else:
                    # Overnight window: 20:00 to 02:00
                    if not (
                        offer.departure_time >= earliest_departure
                        or offer.departure_time <= latest_departure
                    ):
                        continue

            # Only earliest departure provided
            elif earliest_departure is not None:
                if offer.departure_time < earliest_departure:
                    continue

            # Only latest departure provided
            elif latest_departure is not None:
                if offer.departure_time > latest_departure:
                    continue

            matching_offers.append(offer)

    return matching_offers



if __name__ == "__main__":
    from csv_loader import load_companies, load_destinations
    from offer_generator import generate_offers

    companies = load_companies("data/companies.csv")
    destinations = load_destinations("data/destinations.csv")

    offers = generate_offers(companies, destinations)

    # Use the first generated date
    test_date = offers[0].travel_date

    #results = search_offers(offers, "Barcelona", test_date)
    #results = search_offers(offers, "Barcelona", test_date, max_price=50)
    results = search_offers(
        offers,
        "Barcelona",
        test_date,
        max_price=100,
        max_transfers=2
    )

    print(f"\nAvailable buses to Barcelona on {test_date}:")
    print(f"Matching offers: {len(results)}\n")

    for offer in results:
        print(
            f"{offer.offer_id} | "
            f"{offer.company.name} | "
            f"{offer.departure_time} - {offer.arrival_time} | "
            f"€{offer.price:.2f} | "
            f"Seats: {offer.available_seats} | "
            f"Transfers: {offer.transfers}"
        )


    print("----------TEST 1------------")
    # Test 1: Normal daytime window
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="08:00",
        latest_departure="18:00"
    )


    for offer in results:
        print(
            f"{offer.offer_id} | "
            f"{offer.company.name} | "
            f"{offer.departure_time} - {offer.arrival_time} | "
            f"€{offer.price:.2f} | "
            f"Seats: {offer.available_seats} | "
            f"Transfers: {offer.transfers}"
        )

    # Test 2:Overnight window
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="20:00",
        latest_departure="02:00"
    )
    print("----------TEST 2------------")
    for offer in results:
        print(
            f"{offer.offer_id} | "
            f"{offer.company.name} | "
            f"{offer.departure_time} - {offer.arrival_time} | "
            f"€{offer.price:.2f} | "
            f"Seats: {offer.available_seats} | "
            f"Transfers: {offer.transfers}"
        )


    # Test 3: Only earliest departure
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure="10:00",
        latest_departure=None
    )

    print("----------TEST 3------------")
    for offer in results:
        print(
            f"{offer.offer_id} | "
            f"{offer.company.name} | "
            f"{offer.departure_time} - {offer.arrival_time} | "
            f"€{offer.price:.2f} | "
            f"Seats: {offer.available_seats} | "
            f"Transfers: {offer.transfers}"
        )

    print("----------TEST 4------------")
    # Test 4: Only latest departure
    results = search_offers(
        offers, "Barcelona", test_date,
        earliest_departure=None,
        latest_departure="14:00"
    )



    for offer in results:
        print(
            f"{offer.offer_id} | "
            f"{offer.company.name} | "
            f"{offer.departure_time} - {offer.arrival_time} | "
            f"€{offer.price:.2f} | "
            f"Seats: {offer.available_seats} | "
            f"Transfers: {offer.transfers}"
        )

    print("----------TEST 5: MAXIMUM DURATION------------")

    duration_results = search_offers(
        offers,
        "Barcelona",
        test_date,
        max_duration=480
    )

    for offer in duration_results:
        print(
            f"{offer.offer_id} | "
            f"{offer.company.name} | "
            f"Duration: {offer.duration_time} min"
        )

    assert all(offer.duration_time <= 480 for offer in duration_results)

    print("PASS: Maximum duration filter")