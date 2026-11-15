from exceptions import InvalidCompanyError, InvalidReviewError
import re
from review import Review


class BusCompany:
    def __init__(self, company_id, name, description):
        if not isinstance(company_id, str) or not company_id.strip():
            raise InvalidCompanyError("Company ID cannot be empty")

        if not isinstance(name, str) or not name.strip():
            raise InvalidCompanyError("Company name cannot be empty")

        if not isinstance(description, str) or not description.strip():
            raise InvalidCompanyError("Company description cannot be empty")

        if not re.fullmatch(r"C[0-9]{3}", company_id):
            raise InvalidCompanyError("Company ID must follow C001 format")

        self.company_id = company_id
        self.name = name
        self.description = description

        # adding the rating:
        self.reviews = []

    def add_review(self, review):
        if not isinstance(review, Review):
            raise InvalidReviewError("It must be a Review object")
        self.reviews.append(review)

    def get_average_ratings(self):
        if len(self.reviews) == 0:
            return None

        price_sum = 0
        speed_sum = 0
        comfort_sum = 0
        flexibility_sum = 0

        for i in range(len(self.reviews)):
            price_sum += self.reviews[i].price_rating
            speed_sum += self.reviews[i].speed_rating
            comfort_sum += self.reviews[i].comfort_rating
            flexibility_sum += self.reviews[i].flexibility_rating

        count = len(self.reviews)

        averages = {
            "price": price_sum / count,
            "speed": speed_sum / count,
            "comfort": comfort_sum / count,
            "flexibility": flexibility_sum / count
        }

        return averages
            
