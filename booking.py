def generate_booking_reference(booking_number):
    if not isinstance(booking_number, int) or isinstance(booking_number, bool):
        raise ValueError("Booking number must be an integer.")

    if booking_number < 0 or booking_number > 9999999:
        raise ValueError("Booking number must be between 0 and 9999999.")

    return f"B8{booking_number:07d}"

def get_next_booking_number(bookings):
    if not bookings:
        return 0

    highest_number = max(
        int(booking.booking_reference[2:])
        for booking in bookings)

    return highest_number + 1


class Booking:
    def __init__(self, booking_reference, offer, passenger_name,
                         luggage_included=None,refundable=None,changeable=None):
        self.booking_reference = booking_reference
        self.offer = offer
        self.passenger_name = passenger_name

        # Store the fare conditions at booking time
        self.luggage_included = (offer.luggage_included if luggage_included is None else luggage_included)
        self.refundable = (offer.refundable if refundable is None else refundable)
        self.changeable = (offer.changeable if changeable is None else changeable)

    def __str__(self):
        return (
            f"Booking reference: {self.booking_reference}\n"
            f"Passenger: {self.passenger_name}\n"
            f"Company: {self.offer.company.name}\n"
            f"Destination: {self.offer.destination.name}\n"
            f"Travel date: {self.offer.travel_date}\n"
            f"Departure: {self.offer.departure_time}\n"
            f"Price: €{self.offer.price:.2f}\n"
            f"Luggage included: {self.luggage_included}\n"
            f"Refundable: {self.refundable}\n"
            f"Changeable: {self.changeable}")