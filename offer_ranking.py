from datetime import datetime
from math import isfinite

TRAVELLER_PROFILES = {
    "budget": {
        "w_price": 0.70,
        "w_duration": 0.10,
        "w_time": 0.10,
        "w_flexibility": 0.10
    },

    "business": {
        "w_price": 0.10,
        "w_duration": 0.40,
        "w_time": 0.40,
        "w_flexibility": 0.10
    },

    "flexible_tourist": {
        "w_price": 0.10,
        "w_duration": 0.10,
        "w_time": 0.10,
        "w_flexibility": 0.70
    }
}


def calculate_price_score(price, min_price):
    if price <= 0 or min_price <= 0:
        raise ValueError("Prices must be greater than zero.")

    score = 100 * (min_price / price)

    return score

def calculate_duration_score(duration, min_duration):
    if duration <= 0 or min_duration <= 0:
        raise ValueError("Durations must be greater than zero.")

    score = 100 * (min_duration / duration)

    return score

def calculate_time_score(departure_time, preferred_time):
    departure = datetime.strptime(departure_time, "%H:%M")
    preferred = datetime.strptime(preferred_time, "%H:%M")

    difference = abs((departure - preferred).total_seconds() / 60)

    # Handle departures around midnight
    difference = min(difference, 1440 - difference)

    score = 100 * max(0, 1 - difference / 300)

    return score

def calculate_flexibility_score(changeable, refundable):
    score = 0
    if changeable == True:
        score += 50
    if refundable == True:
        score += 50
    return score

def validate_weights(w_price, w_duration, w_time, w_flexibility):
    weights = [w_price, w_duration, w_time, w_flexibility]

    # Check that no weight is negative
    for weight in weights:
        if not isfinite(weight):
            raise ValueError("Weights must be finite numbers.")

        if weight < 0:
            raise ValueError("Weights cannot be negative.")

    # Check that the weights add up to 1.0 (100%)
    total = sum(weights)

    if abs(total - 1.0) > 0.000001:
        raise ValueError("Weights must add up to 1.0 (100%).")
    return True


def calculate_weighted_score(price_score, duration_score,
                             time_score, flexibility_score,
                             w_price=0.40, w_duration=0.25,
                             w_time=0.15, w_flexibility=0.20):

    validate_weights(w_price, w_duration, w_time, w_flexibility)

    total_score = (w_price * price_score + w_duration * duration_score
        + w_time * time_score + w_flexibility * flexibility_score)
    return total_score


def rank_offers(offers, preferred_time,
                w_price=0.40, w_duration=0.25,
                w_time=0.15, w_flexibility=0.20):
    # Validate weights, even if no offers are available
    validate_weights(w_price, w_duration, w_time, w_flexibility)

    # No acceptable offers
    if not offers:
        return []

    # Find minimum price and duration
    min_price = min(offer.price for offer in offers)
    min_duration = min(offer.duration_time for offer in offers)

    ranked_offers = []

    for offer in offers:
        price_score = calculate_price_score(offer.price, min_price)

        duration_score = calculate_duration_score(
            offer.duration_time, min_duration)

        time_score = calculate_time_score(
            offer.departure_time, preferred_time)

        flexibility_score = calculate_flexibility_score(
            offer.changeable, offer.refundable)

        total_score = calculate_weighted_score(
            price_score, duration_score, time_score, flexibility_score,
            w_price, w_duration, w_time, w_flexibility)

        ranked_offers.append({
            "offer": offer,
            "price_score": price_score,
            "duration_score": duration_score,
            "time_score": time_score,
            "flexibility_score": flexibility_score,
            "total_score": total_score})

    # Highest total score first; offer ID breaks ties
    ranked_offers.sort(
        key=lambda item: (-item["total_score"], item["offer"].offer_id))
    return ranked_offers


def rank_offers_by_profile(offers, preferred_time, profile_name):
    if profile_name not in TRAVELLER_PROFILES:
        raise ValueError("Unknown traveller profile.")

    weights = TRAVELLER_PROFILES[profile_name]

    return rank_offers(
        offers,
        preferred_time,
        **weights)  # dictionary unpacking


def explain_offer(ranked_offer):
    offer = ranked_offer["offer"]
    advantages = []
    disadvantages = []

    if ranked_offer["price_score"] >= 80:
        advantages.append("Competitive ticket price")
    elif ranked_offer["price_score"] < 50:
        disadvantages.append("Relatively expensive ticket")

    if ranked_offer["duration_score"] >= 80:
        advantages.append("Short journey duration")
    elif ranked_offer["duration_score"] < 50:
        disadvantages.append("Relatively long journey")

    if ranked_offer["time_score"] >= 80:
        advantages.append("Convenient departure time")
    elif ranked_offer["time_score"] < 50:
        disadvantages.append("Departure far from preferred time")

    if offer.changeable:
        advantages.append("Ticket can be changed")
    else:
        disadvantages.append("Ticket cannot be changed")

    if offer.refundable:
        advantages.append("Ticket is refundable")
    else:
        disadvantages.append("Ticket is non-refundable")

    if not advantages:
        advantages.append("Offer meets the selected search requirements")

    if not disadvantages:
        disadvantages.append("No significant disadvantages identified")

    return {
        "advantages": advantages,
        "disadvantages": disadvantages
    }

if __name__ == "__main__":

    print("TEST: PRICE NORMALIZATION")

    prices = [20, 40, 60]

    min_price = min(prices)

    for price in prices:
        score = calculate_price_score(price, min_price)

        print(f"Price: €{price} | Score: {score:.2f}")

    print("\nTEST: DURATION NORMALIZATION")

    durations = [240, 360, 480]

    min_duration = min(durations)

    for duration in durations:
        score = calculate_duration_score(duration, min_duration)

        print(f"Duration: {duration} min | Score: {score:.2f}")



    print("\nTEST: DEPARTURE TIME NORMALIZATION")

    preferred_time = "10:00"

    departure_times = ["10:00", "09:00", "12:00", "15:00"]

    for departure_time in departure_times:
        score = calculate_time_score(departure_time, preferred_time)

        print(f"Departure: {departure_time} | Score: {score:.2f}")


    print("\nTEST: TICKET FLEXIBILITY SCORING")

    conditions = [
        (True, True),
        (True, False),
        (False, True),
        (False, False)
    ]

    for changeable, refundable in conditions:
        score = calculate_flexibility_score(changeable, refundable)

        print(
            f"Changeable: {changeable} | "
            f"Refundable: {refundable} | "
            f"Score: {score}"
        )