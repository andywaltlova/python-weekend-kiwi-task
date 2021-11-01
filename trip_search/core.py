import json
from datetime import datetime, timedelta


# Used to optimize search
NO_OPTIMIZATION_AVAILABLE = 0
SHOULD_SKIP_FLIGHT = 1
SHOULD_TERMINATE_SEARCH = -1


class Flight:
    def __init__(self, flight_no, origin, destination, departure,
                 arrival, base_price, bag_price, bags_allowed) -> None:
        self.flight_no = flight_no
        self.origin = origin
        self.destination = destination
        self.departure = datetime.strptime(departure, '%Y-%m-%dT%H:%M:%S')
        self.arrival = datetime.strptime(arrival, '%Y-%m-%dT%H:%M:%S')
        self.duration = self.arrival - self.departure
        self.base_price = float(base_price)
        self.bag_price = float(bag_price)
        self.bags_allowed = int(bags_allowed)

        self._attributes_are_valid()

    def __repr__(self) -> str:
        return f'<{self.flight_no} FROM: {self.origin}({self.departure}) TO: {self.destination}({self.arrival})>'

    def __eq__(self, o: object) -> bool:
        same_number = self.flight_no == o.flight_no
        same_direction = self.destination == o.destination and self.origin == o.origin
        same_time = self.arrival == o.arrival and self.departure == o.departure
        return same_number and same_direction and same_time
    
    def __hash__(self) -> int:
        return hash((self.flight_no, self.origin, self.destination, self.arrival, self.departure))

    def _attributes_are_valid(self):
        # Validation logic could be better with property and setters decorators
        # to avoid changing attributes to invalid values after init is done.
        msg = ''
        if self.origin == self.destination:
            msg = f'Origin ({self.origin}) cannot be same as destination ({self.destination}). Flight: {self}.'
        if self.departure >= self.arrival:
            msg = f'Departure time ({self.departure}) cannot be bigger than arrival time ({self.arrival}). Flight: {self}.'
        if msg:
            raise ValueError(msg)

    def is_time_travel(self, follow_up_flight: 'Flight') -> bool:
        '''Used to validating flights in trip search.'''
        return follow_up_flight.departure < self.arrival

    def assert_layover(self, follow_up_flight: 'Flight', max_layover: int) -> tuple[bool]:
        '''Determine if layover is too small or too big in compare to given limit.'''

        layover = follow_up_flight.departure - self.arrival
        min_layover = timedelta(hours=1.0)
        max_layover = timedelta(hours=max_layover)
        return layover < min_layover, layover > max_layover

    def to_JSON(self) -> str:
        json_repr = {
            'flight_no': self.flight_no,
            'origin': self.origin,
            'destination': self.destination,
            'departure': str(self.departure),
            'arrival': str(self.arrival),
            'base_price': self.base_price,
            'bag_price': self.bag_price,
            'bags_allowed': self.bags_allowed
        }
        return json_repr


class Trip:
    def __init__(self, origin: str, destination: str, flights: list[Flight], bags_count=0) -> None:
        self.flights = [f.to_JSON() for f in flights]
        self.origin = origin
        self.destination = destination
        self.bags_allowed = self._get_allowed_bags(flights)
        self.bags_count = bags_count
        self.total_price = self._calculate_trip_price(flights)
        self.travel_time = str(self._calculate_travel_time(flights))

    def _get_allowed_bags(self, flights: list[Flight]) -> int:
        return min([f.bags_allowed for f in flights])

    def _calculate_trip_price(self, flights: list[Flight]) -> float:
        flights_price = sum([f.base_price for f in flights])
        bags_price = sum([f.bag_price*self.bags_count for f in flights])
        return flights_price + bags_price

    def _calculate_travel_time(self, flights: list[Flight]) -> timedelta:
        return sum([f.duration for f in flights], timedelta())

    def to_JSON(self) -> str:
        return self.__dict__


class Airport:
    '''Represents node in graph used in SearchEngine.'''

    def __init__(self, code: str) -> None:
        self.code = code
        self.flights = []

    def __repr__(self) -> str:
        return f'<{self.code}>'

    def __eq__(self, o: object) -> bool:
        return self.code == o.code
    
    def __hash__(self) -> int:
        return hash(self.code)

    def add_flight(self, flight: Flight) -> None:
        self.flights.append(flight)


class SearchEngine:
    def __init__(self, parameters) -> None:
        self.parameters = parameters
        self.graph = {}
        self.paths = []

    def construct_routes(self, flights: list[Flight]) -> None:
        '''
        Generate 'multigraph' of airports with possible flights.
        Flights are sorted in ascending order for each airport.
        '''

        # Filter flights based on static parameters
        flights = self._filter_flights(flights)

        for flight in flights:
            origin = flight.origin
            dest = flight.destination

            # Add airports to graph if they are not there yet
            self.graph[origin] = self.graph.get(origin, Airport(origin))
            self.graph[dest] = self.graph.get(dest, Airport(dest))

            # Add flight from origin to destination
            self.graph[origin].add_flight(flight)

        self._sort_airport_flights()

    def _filter_flights(self, flights: list[Flight]) -> list[Flight]:
        '''
        Static filtering of floghs based on optional parameters.
        Flights are filtered before graph itself is constructed.
        '''
        bag_filter = lambda f: f.bags_allowed >= self.parameters['bags']

        exclude_airports = set(self.parameters['exclude'])
        exclude_filter = lambda f: not set([f.origin, f.destination]).intersection(exclude_airports)

        all_filters = [bag_filter, exclude_filter]

        max_bag_price = self.parameters.get('max_bag_price')
        if max_bag_price:
            all_filters.append(lambda f: f.bag_price <= self.parameters['max_bag_price'])

        trip_start = self.parameters.get('trip_start_time')
        trip_end = self.parameters.get('trip_return_time')
        if trip_end:
            trip_end = datetime.strptime(trip_end, '%Y-%m-%dT%H:%M:%S')
        if trip_start:
            trip_start = datetime.strptime(trip_start, '%Y-%m-%dT%H:%M:%S')

        return_time_limit = trip_end and self.parameters['return_trip']
        if trip_start and return_time_limit:
            all_filters.append(lambda f: f.arrival <= trip_end and f.departure >= trip_start)
        elif trip_start:
            all_filters.append(lambda f: f.departure >= trip_start)
        elif return_time_limit:
            all_filters.append(lambda f: f.arrival <= trip_end)

        return [f for f in flights if all(cond(f) for cond in all_filters)]

    def _sort_airport_flights(self) -> None:
        '''Sort flights in ascending order to optimize trip search.'''
        for airport in self.graph.values():
            airport.flights.sort(key=lambda k: k.departure)

    def search(self, flights, origin, destination) -> None:
        '''
        Public search method. Construct graph and filter flighs based on given
        parameters before calling recursive search.
        '''

        self.construct_routes(flights)

        airport_code_info = f'Please also make sure that ariport code exists (e.g on https://www.iata.org/en/publications/directories/code-search/).'
        if origin not in self.graph:
            print(f'There are no flights from {origin} for given search parameters.')
            print(f'{airport_code_info}')
            return
        if destination not in self.graph:
            print(f'There are no flights to {destination} for given search parameters.')
            print(f'{airport_code_info}')
            return

        origin = self.graph[origin]
        destination = self.graph[destination]
        return self._search(origin, destination, [], [])

    def _search(self, origin: Airport, destination: Airport,
                visited: list[Airport], path: list[Flight], 
                is_return=False, dest_index=None) -> None:
        '''Private search method (recursive DFS).'''
        
        # Mark the origin airport as visited
        visited.append(origin)

        # Search through all flights from origin airport
        for f in origin.flights:
            # Optimization of the search
            optimization = self._optimize_search(path, f, is_return, dest_index)
            if optimization == SHOULD_TERMINATE_SEARCH:
                return
            elif optimization == SHOULD_SKIP_FLIGHT:
                continue

            flight_dest = self.graph[f.destination]
            path.append(f)

            # If current flight directly leads to destination
            if destination == flight_dest:
                # If specified, search also for return part of trip
                if self.parameters['return_trip'] and not is_return:
                    # Index of flight reaching destination
                    dest_index = len(path) - 1
                    origin = self.graph[path[0].origin]
                    self._search(flight_dest, origin, 
                                 [], path.copy(), 
                                 is_return=True, dest_index=dest_index)
                else:
                    self.paths.append(path.copy())
                path.pop()
                continue

            # If current flight does not leads to destination search from its destination
            if flight_dest not in visited:
                self._search(flight_dest, destination, 
                             visited.copy(), path.copy(), 
                             is_return, dest_index)

            path.pop()

    def _optimize_search(self, path, next_flight, is_return, dest_index) -> int:
        '''
        Check if graph search can be terminated early or some branches can be skipped.
        Optimizes based on:
            flight cannot be follow up to last one
            max trip price reached
            layover limit is too big (flights are in ascending order)
            max stops limit is reached
        '''

        # cannot optimize without at least one previous flight
        if not path:
            return NO_OPTIMIZATION_AVAILABLE

        # skip if can't be follow up of last flight
        if path[-1].is_time_travel(next_flight):
            return SHOULD_SKIP_FLIGHT

        max_trip_price = self.parameters.get('max_trip_price')
        if max_trip_price:
            origin = self.parameters['origin']
            dest = self.parameters['destination']
            bags_count = self.parameters['bags']

            trip = Trip(origin, dest, path, bags_count)
            if trip.total_price >= max_trip_price:
                return SHOULD_TERMINATE_SEARCH

        # return if layover is too long (can't get any better with ascending order of flights)
        layover_limit = self.parameters['layover_limit']
        # terminate if too many flighs already in path
        max_steps = self.parameters['max_stops']

        layover_over_limit, too_many_stops = False, False
        if is_return and path[dest_index] == path[-1]:
            # First return flight
            days_in_dest = timedelta(days=self.parameters.get('days_in_destination'))
            flight_to_dest = path[-1].arrival
            return_flight = next_flight.departure
            if return_flight - flight_to_dest <= days_in_dest:
                return SHOULD_SKIP_FLIGHT

        elif is_return and not path[dest_index] == path[-1]:
            # Return flights (except the first)
            too_many_stops = len(path[dest_index:]) == max_steps
            _, layover_over_limit = path[-1].assert_layover(next_flight, layover_limit)

        else:
            too_many_stops = len(path) == max_steps
            _, layover_over_limit = path[-1].assert_layover(next_flight, layover_limit)

        if layover_over_limit or too_many_stops:
            return SHOULD_TERMINATE_SEARCH

        return NO_OPTIMIZATION_AVAILABLE

    def get_output(self) -> str:
        '''Convert all paths to Trips and exports them as JSON.'''

        origin = self.parameters['origin']
        dest = self.parameters['destination']
        bags_count = self.parameters['bags']

        trips = [Trip(origin, dest, flights, bags_count).to_JSON()
                 for flights in self.paths]
        trips.sort(key=lambda k: k['total_price'])
        return json.dumps(trips, indent=4)
