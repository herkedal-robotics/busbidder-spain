from exceptions import InvalidCompanyError, InvalidReviewError

class Review:
    def __init__(self, price_rating, speed_rating,
                 comfort_rating, flexibility_rating):

        ratings = {
            "Price": price_rating,
            "Speed": speed_rating,
            "Comfort": comfort_rating,
            "Flexibility": flexibility_rating
        }

        for category, rating in ratings.items():
            if not isinstance(rating, int) or isinstance(rating, bool):
                raise InvalidReviewError(
                    f"{category} rating must be an integer"
                )

            if rating < 1 or rating > 5:
                raise InvalidReviewError(
                    f"{category} rating must be between 1 and 5"
                )

        self.price_rating = price_rating
        self.speed_rating = speed_rating
        self.comfort_rating = comfort_rating
        self.flexibility_rating = flexibility_rating