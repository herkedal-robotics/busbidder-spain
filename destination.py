from exceptions import InvalidDestinationError
import re

class Destination:
    def __init__(self, destination_id, name, region):
        if not isinstance(destination_id, str) or not destination_id.strip():
            raise InvalidDestinationError("Destination ID cannot be empty")

        if not isinstance(name, str) or not name.strip():
            raise InvalidDestinationError("Destination name cannot be empty")

        if not isinstance(region, str) or not region.strip():
            raise InvalidDestinationError("Destination region cannot be empty")

        if not re.fullmatch(r"D[0-9]{3}", destination_id):
            raise InvalidDestinationError("Destination ID must follow D001 format")

        
        self.destination_id = destination_id
        self.name = name
        self.region = region