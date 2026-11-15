class InvalidCompanyError(Exception):
    """Raised when company name is empty, or is a duplicate, or it has duplicate IDs"""
    pass

class InvalidDestinationError(Exception):
    """Raised when destination information is invalid."""
    pass

class InvalidOfferError(Exception):
    """Raised when bus offer information is invalid."""
    pass

class InvalidReviewError(Exception):
    pass