import sys
from csv_loader import load_companies,load_destinations,save_offers,load_offers
from pathlib import Path
from exceptions import InvalidCompanyError, InvalidDestinationError
from offer_generator import generate_offers
from offer_search import search_offers as filter_offers #because we have duplicate name
from datetime import datetime, date, timedelta
import math
from offer_ranking import rank_offers, rank_offers_by_profile, explain_offer
import re
from booking import Booking,generate_booking_reference,get_next_booking_number
from csv_loader import load_bookings, save_bookings
from logging_utils import log_call
import logging

#def valid_filter_menu_option(value):
#    valid_options = ["1", "2", "3", "4", "5", "6","7", "8", "9", "10", "11"]
#    return value in valid_options

def get_menu_choice(max_option, return_message="Returning to previous menu..."):
    def valid_option(value):
        valid_options = [str(i) for i in range(1, max_option + 1)]
        return value in valid_options

    return get_valid_input(
        f"\nEnter option (1-{max_option}), 'c' to go back, or 'e' to exit: ",
        valid_option,
        return_message)


def get_valid_input(prompt, validator, return_message="Returning to previous menu..."):
    while True:
        user_input = input(prompt).strip()
        # Cancel and return to previous menu
        if user_input.lower() in ("c", "back"):
            print(return_message)
            return None

        # Exit the entire application
        if user_input.lower() in ("e", "exit"):
            print("Exiting BusBidder Spain. Goodbye!")
            sys.exit()

        # Check whether input is valid
        if validator(user_input):
            return user_input

        # Invalid input - repeat the question
        print(
            "Invalid input. Please try again, "
            "enter 'c' to cancel, or 'e' to exit."
        )

def valid_price(value):
    if len(value) > 7:
        return False
    if not re.fullmatch(r"[0-9]+(\.[0-9]{1,2})?", value):
        return False
    
    price = float(value)

    if not math.isfinite(price) or not 1 <= price <= 9999:
        return False
    return True

def valid_time(value):
    try:
        time = datetime.strptime(value, "%H:%M")
        if time.strftime("%H:%M") == value:
            return True
    except ValueError:
        pass
    return False


def valid_percentage(value):
    try:
        percentage = float(value)
    except ValueError:
        return False
    if not math.isfinite(percentage):
        return False
    if not 0 <= percentage <= 100:
        return False
    return True

def valid_nonnegative_integer(value):
    if not value.isascii() or not value.isdecimal():
        return False
    if len(value) > 4:
        return False
    return True

def valid_passenger_name(value):
    return bool(value.strip())

def valid_booking_reference(value):
    return value.upper().startswith("B8") and len(value) == 9 and value[2:].isdigit()

def get_yes_no_filter(filter_name):
    user_input = get_valid_input(f"\nRequire {filter_name}? (y/n), 'c' to cancel, or 'e' to exit: ",
        valid_yes_no,return_message="Returning to Apply Filters menu...")
    
    if user_input is None:
        return None
    return user_input.lower() in ("y", "yes")

def valid_yes_no(value):
    return value.lower() in ("y", "n", "yes", "no")

def get_custom_weights():
    print("\n===== Custom Ranking Preferences =====")
    print("Distribute 100% between the four criteria.")
    print("Enter 'c' or 'back' to cancel, or 'e' or 'exit' to quit.\n")
    criteria = {
        "w_price": "Ticket price",
        "w_duration": "Journey duration",
        "w_time": "Departure convenience",
        "w_flexibility": "Ticket flexibility"}
    while True:
        # Reset all percentages when starting again
        weights = {}
        total = 0.0
        restart = False

        for key, name in criteria.items():
            while True:
                remaining = max(0.0, 100 - total)
                user_input = get_valid_input(
                    f"{name} (%) [{remaining:g}% remaining], "
                    "'c' to cancel, or 'e' to exit: ",
                    valid_percentage,
                    return_message="Custom preferences cancelled.")
                if user_input is None:
                    return None
                percentage = float(user_input)
                # Add the new percentage
                new_total = total + percentage
                # Restart if the total exceeds 100%
                if new_total > 100:
                    print(f"\nPercentage already exceeds 100% - "
                          f"you entered {new_total:g}%.")
                    print("Please try again, enter 'c' to cancel, or 'e' to exit.\n")

                    restart = True
                    break
                # Save valid percentage
                weights[key] = percentage / 100
                total = new_total
                break
            # Stop asking for the remaining criteria
            if restart:
                break
        # Restart from the first criterion
        if restart:
            continue
        # Check the total after all four inputs
        if abs(total - 100) > 0.000001:
            print(f"\nYour percentages add up to {total:g}%.")
            print("This does not add up to 100%.")
            print("Please try again, enter 'c' to cancel, or 'e' to exit.\n")
            continue
        print("\nTotal: 100%")
        print("Your preferences have been accepted!")
        return weights

def get_preferred_time():
    preferred_time = get_valid_input(
        "\nEnter preferred departure time (HH:MM), "
        "'c' to cancel, or 'e' to exit: ",
        valid_time,
        return_message="Preferred departure time selection cancelled.")
    return preferred_time

def display_offers(offers):
    if not offers:
        print("\nNo matching bus offers found.")
        return
    print(f"\n===== Matching Bus Offers ({len(offers)}) =====")

    for offer in offers:
        print(
            f"{offer.offer_id} | "
            f"{offer.company.name} | "
            f"{offer.destination.name} | "
            f"Departure: {offer.departure_time} | "
            f"Arrival: {offer.arrival_time} | "
            f"Duration: {offer.duration_time} min | "
            f"€{offer.price:.2f} | "
            f"Transfers: {offer.transfers} | "
            f"Seats: {offer.available_seats} | "
            f"Luggage: {'Yes' if offer.luggage_included else 'No'} | "
            f"Changeable: {'Yes' if offer.changeable else 'No'} | "
            f"Refundable: {'Yes' if offer.refundable else 'No'}")

def display_ranked_offers(ranked_offers):
    if not ranked_offers:
        print("\nNo bus offers available to rank.")
        return
    print("\n===== Ranked Bus Offers =====")

    for position, item in enumerate(ranked_offers, start=1):
        offer = item["offer"]
        print(
            f"{position}. {offer.offer_id} | "
            f"{offer.company.name} | "
            f"€{offer.price:.2f} | "
            f"Departure: {offer.departure_time} | "
            f"Duration: {offer.duration_time} min | "
            f"Price score: {item['price_score']:.2f}/100 | "
            f"Duration score: {item['duration_score']:.2f}/100 | "
            f"Departure score: {item['time_score']:.2f}/100 | "
            f"Flexibility score: {item['flexibility_score']:.2f}/100 |"            
            f"Score: {item['total_score']:.2f}/100")

    # Explain the highest-ranked offer
    best_offer = ranked_offers[0]
    explanation = explain_offer(best_offer)

    print("\n===== Why We Recommend the Top Offer =====")
    print(f"Offer: {best_offer['offer'].offer_id}")

    print("\nAdvantages:")
    if explanation["advantages"]:
        for advantage in explanation["advantages"]:
            print(f"  + {advantage}")
    else:
        print("  No particular advantages identified.")

    print("\nDisadvantages:")
    if explanation["disadvantages"]:
        for disadvantage in explanation["disadvantages"]:
            print(f"  - {disadvantage}")
    else:
        print("  No particular disadvantages identified.")


def choose_ticket(offers):
    if not offers:
        print("\nNo tickets available to select.")
        return None

    def valid_offer_id(value):
        return any(
            offer.offer_id.lower() == value.lower()
            for offer in offers)

    selected_id = get_valid_input(
        "\nEnter the offer ID (e.g. O128), "
        "'c' to cancel, or 'e' to exit: ",
        valid_offer_id,
        return_message="Ticket selection cancelled.")

    if selected_id is None:
        return None

    for offer in offers:
        if offer.offer_id.lower() == selected_id.lower():
            print("\n===== Selected Ticket =====")
            print(f"Offer ID: {offer.offer_id}")
            print(f"Company: {offer.company.name}")
            print(f"Destination: {offer.destination.name}")
            print(f"Travel date: {offer.travel_date}")
            print(f"Departure: {offer.departure_time}")
            print(f"Arrival: {offer.arrival_time}")
            print(f"Price: €{offer.price:.2f}")
            print(f"Available seats: {offer.available_seats}")

            return offer

def confirm_booking(offer,bookings,offers,bookings_path="data/bookings.csv",
    offers_path="data/offers.csv"):

    if offer.available_seats <= 0:
        print("\nSorry, this offer is sold out.")
        return None

    # Ask for passenger name
    passenger_name = get_valid_input(
        "\nEnter passenger name, 'c' to cancel, or 'e' to exit: ",
        valid_passenger_name,
        return_message="Booking cancelled.")

    if passenger_name is None:
        return None

    # Ask for confirmation
    print("\n===== Booking Confirmation =====")
    print(f"Passenger: {passenger_name}")
    print(f"Company: {offer.company.name}")
    print(f"Destination: {offer.destination.name}")
    print(f"Travel date: {offer.travel_date}")
    print(f"Departure: {offer.departure_time}")
    print(f"Price: €{offer.price:.2f}")

    confirmation = get_valid_input(
        "\nConfirm booking? (y/n), 'c' to cancel, or 'e' to exit: ",
        valid_yes_no,
        return_message="Booking cancelled."
    )

    if confirmation is None or confirmation.lower() in ("n", "no"):
        print("Booking was not confirmed.")
        return None

    # Generate the next booking reference
    next_number = get_next_booking_number(bookings)
    booking_reference = generate_booking_reference(next_number)

    booking = Booking(
        booking_reference,
        offer,
        passenger_name
    )

    # Save booking and update available seats
    bookings_file = Path(bookings_path)
    offers_file = Path(offers_path)

    # Keep copies of the original files
    old_bookings = bookings_file.read_bytes() if bookings_file.exists() else None
    old_offers = offers_file.read_bytes() if offers_file.exists() else None

    bookings.append(booking)
    offer.available_seats -= 1

    try:
        save_bookings(bookings, bookings_path)
        save_offers(offers, offers_path)

    except OSError as error:
        logging.error(f"Booking saving failed: {error}")

        # Restore the data in memory
        bookings.remove(booking)
        offer.available_seats += 1

        # Restore the original CSV files
        try:
            if old_bookings is None:
                bookings_file.unlink(missing_ok=True)
            else:
                bookings_file.write_bytes(old_bookings)

            if old_offers is None:
                offers_file.unlink(missing_ok=True)
            else:
                offers_file.write_bytes(old_offers)

        except OSError as restore_error:
            print(f"Error restoring CSV files: {restore_error}")

        print(f"\nError saving booking: {error}")
        print("Booking could not be completed.")
        return None

    logging.info(
        f"Booking confirmed: {booking.booking_reference}, "
        f"Offer: {offer.offer_id}, "
        f"Remaining seats: {offer.available_seats}")

    print("\n===== Booking Successful =====")
    print(f"Booking reference: {booking.booking_reference}")
    print(f"Passenger: {booking.passenger_name}")
    print(f"Remaining seats: {offer.available_seats}")

    return booking


def search_offers(offers, destinations, bookings):
    print("\n===== Search for bus offers =====")

    # Display available destinations
    print("\nAvailable destinations from Madrid:")

    for destination in destinations:
        print(f"- {destination.name}")

    # Find the actual date range in generated offers
    #available_dates = sorted({offer.travel_date for offer in offers})

    available_dates = sorted({
        offer.travel_date
        for offer in offers
        if offer.available_seats > 0
        and datetime.strptime(
            offer.travel_date + " " + offer.departure_time,
            "%Y-%m-%d %H:%M"
        ) > datetime.now()})

    if not available_dates:
        print("\nNo future bus offers are currently available.")
        return

    first_date = datetime.strptime(available_dates[0], "%Y-%m-%d")
    last_date = datetime.strptime(available_dates[-1], "%Y-%m-%d")

    print("\nAvailable travel dates:")
    print("From:", first_date.strftime("%d %B %Y"))
    print("To:  ", last_date.strftime("%d %B %Y"))

    # Validate destination
    while True:
        destination_name = input(
            "\nEnter destination name, '1' to view destinations, "
            "'back' to return, or 'exit' to quit: "
        ).strip()

        if destination_name.lower() == "back":
            return

        elif destination_name.lower() == "exit":
            print("Exiting BusBidder Spain.")
            sys.exit()

        elif destination_name == "1":
            print("\nAvailable destinations from Madrid:")

            for destination in destinations:
                print(f"- {destination.name}")
            continue

        # Check whether the destination exists
        matching_destination = None

        for destination in destinations:
            if destination.name.lower() == destination_name.lower():
                matching_destination = destination
                break

        if matching_destination is not None:
            destination_name = matching_destination.name
            break

        print("Invalid destination. Please choose a city from the list.")

    print("\nEnter travel date ('back' to return, 'exit' to quit):")

    # Step 1: Validate year
    available_years = {date[:4] for date in available_dates}

    while True:
        travel_date_year = input("Enter travel year (YYYY): ").strip().lower()

        if travel_date_year == "back":
            return
        elif travel_date_year == "exit":
            print("Exiting BusBidder Spain.")
            sys.exit()

        if travel_date_year in available_years:
            break

        print("Invalid year. Available years:", ", ".join(sorted(available_years)))

    # Step 2: Validate month
    available_months = {
        date[5:7] for date in available_dates
        if date[:4] == travel_date_year}

    while True:
        travel_date_month = input("Enter travel month (MM): ").strip().lower()

        if travel_date_month == "back":
            return
        elif travel_date_month == "exit":
            print("Exiting BusBidder Spain.")
            sys.exit()

        if travel_date_month.isdigit():
            travel_date_month = travel_date_month.zfill(2)

        if travel_date_month in available_months:
            break

        print("Invalid month. Available months:", ", ".join(sorted(available_months)))

    # Step 3: Validate day
    available_days = {
        date[8:10] for date in available_dates
        if date[:4] == travel_date_year
        and date[5:7] == travel_date_month}

    while True:
        travel_date_day = input("Enter travel day (DD): ").strip().lower()

        if travel_date_day == "back":
            return
        elif travel_date_day == "exit":
            print("Exiting BusBidder Spain.")
            sys.exit()

        if travel_date_day.isdigit():
            travel_date_day = travel_date_day.zfill(2)

        if travel_date_day in available_days:
            break

        print(
            "Invalid day. Available days:",
            ", ".join(sorted(available_days)))

    # Combine the validated values
    travel_date = f"{travel_date_year}-{travel_date_month}-{travel_date_day}"

    active_filters = {
        "max_price": None,
        "max_transfers": None,
        "max_duration": None,
        "required_luggage": None,
        "required_changeable": None,
        "required_refundable": None,
        "earliest_departure": None,
        "latest_departure": None}

    # Search for matching offers
    results = filter_offers(offers, destination_name, travel_date, **active_filters)

    # Display initial search results
    display_offers(results)

    # Search options menu
    while True:
        print("\n===== Search Options =====")
        print("1. Choose a ticket")
        print("2. Apply filters")
        print("3. Sort offers")
        print("4. Change destination or date")
        print("5. Back to main menu")
        print("6. Exit")

        #choice = input("Enter your option: ").strip().lower()
        choice = get_menu_choice(6,return_message="Returning to Main Menu...")

        if choice is None:
            return

        if choice == "1":
            selected_offer = choose_ticket(results)

            if selected_offer is not None:
                confirm_booking(selected_offer, bookings, offers)

        elif choice == "2":
            while True:
                print("\n===== Apply Filters =====")
                print("1. Maximum ticket price")
                print("2. Maximum number of transfers")
                print("3. Maximum journey duration")
                print("4. Luggage included")
                print("5. Changeable ticket")
                print("6. Refundable ticket")
                print("7. Departure time window")
                print("8. Remove a selected filter")
                print("9. Clear all filters")
                print("10. Show matching offers")
                print("11. Back to Search Options")

                #filter_choice = input("\nEnter your option: ").strip()

                filter_choice = get_menu_choice(11,return_message="Returning to Search Options...")

                if filter_choice is None:
                    break

                if filter_choice == "1":
                    user_input = get_valid_input(
                        "\nEnter maximum ticket price (€1–€9999), "
                        "'c' to cancel, or 'e' to exit: ",
                        valid_price,
                        return_message="Returning to Apply Filters menu...")
                    if user_input is None:
                        continue
                    max_price = float(user_input)
                    active_filters["max_price"] = max_price

                    results = filter_offers(
                        offers,
                        destination_name,
                        travel_date,
                        **active_filters)

                    print(f"\nMaximum ticket price set to €{max_price:.2f}.")
                    print(f"Matching offers: {len(results)}")

                elif filter_choice == "2":
                    user_input = get_valid_input(
                        "\nEnter maximum number of transfers, "
                        "'c' to cancel, or 'e' to exit: ",
                        valid_nonnegative_integer,
                        return_message="Returning to Apply Filters menu...")

                    if user_input is None:
                        continue

                    max_transfers = int(user_input)

                    active_filters["max_transfers"] = max_transfers

                    results = filter_offers(
                        offers,
                        destination_name,
                        travel_date,
                        **active_filters)

                    print(f"\nMaximum transfers set to {max_transfers}.")
                    print(f"Matching offers: {len(results)}")

                elif filter_choice == "3":
                    user_input = get_valid_input(
                        "\nEnter maximum journey duration in minutes, "
                        "'c' to cancel, or 'e' to exit: ",
                        valid_nonnegative_integer,
                        return_message="Returning to Apply Filters menu...")

                    if user_input is None:
                        continue

                    max_duration = int(user_input)

                    if max_duration == 0:
                        print("Journey duration must be greater than zero.")
                        continue

                    active_filters["max_duration"] = max_duration

                    results = filter_offers(
                        offers,
                        destination_name,
                        travel_date,
                        **active_filters)

                    print(f"\nMaximum journey duration set to {max_duration} minutes.")
                    print(f"Matching offers: {len(results)}")

                elif filter_choice in ("4", "5", "6"):
                    filter_options = {
                        "4": ("required_luggage", "luggage included"),
                        "5": ("required_changeable", "changeable ticket"),
                        "6": ("required_refundable", "refundable ticket")}
                    filter_key, filter_name = filter_options[filter_choice]

                    answer = get_yes_no_filter(filter_name)

                    if answer is None:
                        continue
                    if answer is True:
                        active_filters[filter_key] = True
                        print(f"\nFilter applied: {filter_name} required.")
                    else:
                        active_filters[filter_key] = None
                        print(f"\nRequirement removed: {filter_name}.")
                    results = filter_offers(
                        offers,
                        destination_name,
                        travel_date,
                        **active_filters)
                    print(f"Matching offers: {len(results)}")

                elif filter_choice == "7":
                    earliest = get_valid_input(
                        "\nEnter earliest departure time (HH:MM), "
                        "'c' to cancel, or 'e' to exit: ",
                        valid_time,
                        return_message="Departure time filter cancelled.")

                    if earliest is None:
                        continue

                    latest = get_valid_input(
                        "\nEnter latest departure time (HH:MM), "
                        "'c' to cancel, or 'e' to exit: ",
                        valid_time,
                        return_message="Departure time filter cancelled.")

                    if latest is None:
                        continue

                    active_filters["earliest_departure"] = earliest
                    active_filters["latest_departure"] = latest

                    results = filter_offers(
                        offers,
                        destination_name,
                        travel_date,
                        **active_filters)

                    print(f"\nDeparture time window set: {earliest} - {latest}")
                    print(f"Matching offers: {len(results)}")

                elif filter_choice == "8":
                    active = {
                        key: value
                        for key, value in active_filters.items()
                        if value is not None}

                    if not active:
                        print("\nThere are no active filters to remove.")
                        continue

                    print("\n===== Active Filters =====")

                    filter_names = {
                        "max_price": "Maximum ticket price",
                        "max_transfers": "Maximum transfers",
                        "max_duration": "Maximum journey duration",
                        "required_luggage": "Luggage included",
                        "required_changeable": "Changeable ticket",
                        "required_refundable": "Refundable ticket",
                        "earliest_departure": "Earliest departure",
                        "latest_departure": "Latest departure"}

                    active_keys = list(active.keys())

                    for number, key in enumerate(active_keys, start=1):
                        print(f"{number}. {filter_names[key]}: {active[key]}")

                    selection = get_menu_choice(
                        len(active_keys),
                        return_message="Returning to Apply Filters menu...")

                    if selection is None:
                        continue

                    selected_key = active_keys[int(selection) - 1]
                    active_filters[selected_key] = None

                    results = filter_offers(
                        offers,
                        destination_name,
                        travel_date,
                        **active_filters)

                    print(f"\nRemoved: {filter_names[selected_key]}")
                    print(f"Matching offers: {len(results)}")


                elif filter_choice == "9":
                    for key in active_filters:
                        active_filters[key] = None

                    results = filter_offers(
                        offers,
                        destination_name,
                        travel_date,
                        **active_filters)

                    print("\nAll filters have been cleared.")
                    print(f"Matching offers: {len(results)}")

                elif filter_choice == "10":
                    display_offers(results)

                elif filter_choice == "11":
                    break

                else:
                    print(
                        "Invalid input. Try again, enter 'c' to go back, "
                        "or 'exit' to quit.")

        elif choice == "3":

            while True:
                print("\n===== Sort Offers =====")
                print("1. Budget traveller")
                print("2. Business traveller")
                print("3. Flexible tourist")
                print("4. Custom ranking preferences")
                print("5. Back to Search Options")

                #sort_choice = input("Enter your option (number 1-5): ").strip().lower()
                sort_choice = get_menu_choice(5,return_message="Returning to Search Options...")

                if sort_choice is None:
                    break

                if sort_choice in ("1", "2", "3"):
                    profiles = {
                        "1": "budget",
                        "2": "business",
                        "3": "flexible_tourist"}

                    profile_name = profiles[sort_choice]

                    preferred_time = get_preferred_time()

                    if preferred_time is None:
                        print("Returning to Sort Offers menu...")
                        continue

                    ranked = rank_offers_by_profile(
                        results,
                        preferred_time,
                        profile_name)

                    if not ranked:
                        print("\nNo bus offers available to rank.")

                    else:
                        #print(f"\n===== Ranked Offers: {profile_name} =====")

                        #for position, item in enumerate(ranked, start=1):
                        #    offer = item["offer"]

                        #    print(
                        #        f"{position}. {offer.offer_id} | "
                        #        f"{offer.company.name} | "
                        #        f"€{offer.price:.2f} | "
                        #        f"Departure: {offer.departure_time} | "
                        #        f"Duration: {offer.duration_time} min | "
                        #        f"Score: {item['total_score']:.2f}/100"
                        #    )
                        display_ranked_offers(ranked)
                elif sort_choice == "4":
                    weights = get_custom_weights()

                    if weights is None:
                        print("Returning to Sort Offers menu...")
                        continue

                    preferred_time = get_preferred_time()

                    if preferred_time is None:
                        print("Returning to Sort Offers menu...")
                        continue

                    ranked = rank_offers(
                        results,
                        preferred_time,
                        **weights)

                    if not ranked:
                        print("\nNo bus offers available to rank.")

                    else:
                        #print("\n===== Ranked Bus Offers =====")

                        #for position, item in enumerate(ranked, start=1):
                        #    offer = item["offer"]

                        #    print(
                        #        f"{position}. {offer.offer_id} | "
                        #        f"{offer.company.name} | "
                        #        f"€{offer.price:.2f} | "
                        #        f"Departure: {offer.departure_time} | "
                        #        f"Duration: {offer.duration_time} min | "
                        #        f"Score: {item['total_score']:.2f}/100"
                        #    )
                        display_ranked_offers(ranked)

                elif sort_choice == "5" or sort_choice == "back":
                    break

                else:
                    print("Invalid option. Please try again.")

        elif choice == "4":
            print("Change destination or date selected.")

        elif choice == "5" or choice == "back":
            return

        elif choice == "6" or choice == "exit":
            print("Exiting BusBidder Spain.")
            sys.exit()

        else:
            print("Invalid option. Please try again.")

def view_destinations(destinations):
    print("\n===== Available Destinations =====")
    for destination in destinations:
        print(
            destination.destination_id,
            "-",
            destination.name,
            "-",
            destination.region)

    while True:
        choice = input("\nType 'back' to return, 'exit' to quit: ").strip().lower()

        if choice == "back":
            return

        elif choice == "exit":
            print("Exiting BusBidder Spain.")
            sys.exit()

        else:
            print("Invalid option. Please type 'back' or 'exit'.")



def load_data():
    try:
        companies = load_companies("data/companies.csv")
        destinations = load_destinations("data/destinations.csv")

    except FileNotFoundError:
        print("Error: Company file was not found.")

    except KeyError as error:
        print("Error: Missing CSV column:", error)

    except (InvalidCompanyError, InvalidDestinationError) as error:
        print("Error:", error)

    else:
        print("Successfully loaded", len(companies), "companies.")
        print("Successfully loaded", len(destinations), "destinations.")
        return companies, destinations

    return [], []

@log_call
def load_or_generate_offers(companies,destinations,file_path="data/offers.csv"):

    offers_path = Path(file_path)

    # First run: generate offers for 30 days
    if not offers_path.exists():
        offers = generate_offers(companies, destinations)
        save_offers(offers, offers_path)
        print("Generated and saved", len(offers), "bus offers.")
        return offers
    
    # Load previously saved offers
    offers = load_offers(companies, destinations, offers_path)

    if not offers:
        raise ValueError("The saved offers file is empty.")

    print("Loaded", len(offers), "saved bus offers.")

    # Find the last travel date already generated
    last_date = max(
        datetime.strptime(offer.travel_date, "%Y-%m-%d").date()
        for offer in offers)

    today = date.today()

    # Generate more offers when fewer than 3 future days remain
    if (last_date - today).days <= 2:
        start_date = last_date + timedelta(days=1)

        # If the application was not used for a long time,
        # skip expired dates
        start_date = max(
            start_date,
            today + timedelta(days=1))

        # Find the next unused offer number
        next_offer_number = max(
            int(offer.offer_id[1:])
            for offer in offers) + 1

        new_offers = generate_offers(
            companies,
            destinations,
            start_date=start_date,
            number_of_days=28,
            starting_offer_id=next_offer_number)

        offers.extend(new_offers)
        save_offers(offers, offers_path)
        print("Generated and saved", len(new_offers), "additional offers.")

    return offers

def view_bookings(bookings):

    if not bookings:
        print("\nNo bookings found.")
        return

    def valid_existing_booking(value):
        return (
            valid_booking_reference(value)
            and any(
                booking.booking_reference.upper() == value.upper()
                for booking in bookings
            )
        )

    booking_reference = get_valid_input(
        "\nEnter booking reference, 'c' to cancel, or 'e' to exit: ",
        valid_existing_booking,
        return_message="Booking search cancelled."
    )

    if booking_reference is None:
        return

    for booking in bookings:
        if booking.booking_reference.upper() == booking_reference.upper():
            print("\n===== Booking Details =====")
            print(booking)
            return



def main_menu(companies, destinations, offers, bookings):
    while True:
        # Display the menu
        print("\n===== BusBidder Spain =====")
        print("1. Search for bus offers")
        print("2. View available destinations")
        print("3. View bookings")
        print("4. Exit")

        # Get the user's choice
        #choice = input("Enter your option: ").strip().lower()
        choice = get_menu_choice(4,return_message="Already at the Main Menu.")

        if choice is None:
            continue

        # Check the choice
        if choice == "1":
            search_offers(offers, destinations, bookings)

        elif choice == "2":
            view_destinations(destinations)

        elif choice == "3":
            view_bookings(bookings)

        elif choice == "4" or choice == "exit":
            print("Exiting BusBidder Spain.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    companies, destinations = load_data()
    if companies and destinations:
        try:
            offers = load_or_generate_offers(companies,destinations)
        except (ValueError, KeyError, OSError) as error:
            print(f"Error loading or generating offers: {error}")
            sys.exit(1)

        #main_menu(companies, destinations, offers)
        try:
            bookings = load_bookings(offers)
        except (ValueError, KeyError, OSError) as error:
            print(f"Error loading bookings: {error}")
            sys.exit(1)

        print("Successfully loaded", len(bookings), "bookings.")

        main_menu(companies, destinations, offers, bookings)

    else:
        print("Cannot start BusBidder Spain without company and destination data.")