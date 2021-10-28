import json
import csv
from datetime import datetime


class Flight:
    """Class representing one flight."""

    def __init__(self, flight_no, origin, destination, departure,
                 arrival, base_price, bag_price, bags_allowed) -> None:
        self.flight_no: str = flight_no
        self.origin: str = origin
        self.destination: str = destination
        self.departure: datetime = datetime.strptime(
            departure, format='%Y-%m-%dT%H:%M:%S')
        self.arrival: datetime = datetime.strptime(
            arrival, format='%Y-%m-%dT%H:%M:%S')
        self.base_price: float = float(base_price)
        self.bag_price: float = float(bag_price)
        self.bags_allowed: int = int(bags_allowed)

    def to_JSON(self) -> str:
        return json.dumps(self, default=lambda f: f.__dict__, indent=4)


class Trip:
    """Class representing trip."""

    def __init__(self, origin, destination, bags_count=0) -> None:
        self.flighs: Flight = []
        self.origin: str = origin
        self.destination: str = destination
        self.bags_allowed: int = self._get_allowed_bags()
        self.bags_count: int = bags_count
        self.total_price = self._calculate_trip_price()
        self.travel_time = self._calculate_travel_time()

    def _get_allowed_bags(self):
        return min([f.bags_allowed for f in self.flighs])

    def _calculate_trip_price(self):
        return sum([f.base_price for f in self.flighs])

    def _calculate_travel_time(self):
        return sum([f.duration for f in self.flighs])

    def to_JSON(self) -> str:
        # must export flighs also as JSON
        return json.dumps(self, default=lambda f: f.__dict__, indent=4)


class SearchEngine:
    def __init__(self, flights) -> None:
        pass

    def search(self, origin, destination, bags, return_requested,
               max_trip_price, max_bag_price, passengers, max_stops,
               exclude):
        pass
        self.output = []

    def get_output(self):
        pass


class InvalidFlightDataError(Exception):
    """Exception raised for errors in the input dataset.

    Attributes:
        line -- line that caused error
    """

    def __init__(self, line):
        super().__init__(f'Missing or invalid value on line {line}.')


def load_data(paths: list[str]) -> list[Flight]:
    # TODO
    return []
