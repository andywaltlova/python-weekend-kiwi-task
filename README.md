# :christmas_tree: Trip search :airplane: :baggage_claim:

            ______
            _\ _~-\___
    =  = ==(__________D
                \_____\___________________,-~~~~~~~`-.._
                /     o O o o o o O O o o o o o o O o  |\_
                `~-.__        ___..----..                  )
                      `---~~\___________/------------`````
                      =  ===(_________D

## How to run my solution?

Task solution is in `trip_search` package:

```
trip_search
├── core.py # core classes (Flight, Trip, Airport, SearchEngine)
└── utils.py # creation of parser, loading and validating of input data
```

`solution.py` in repository root imports all neccesary functions, takes care of argument parsing, data loading and calling search itself. 

Solution is implemented as CLI with help of `argparse` from standard library. For list of all possible arguments use `python3 solution.py --help`. 

Trip search logic is encapsulated in `SearchEngine` class, search itself is done with recursive DFS. Airports are representing nodes in graph, Flights are edges, for each airport sorted in ascending order. If optional arguments are specified, search is optimized accordingly -> e.g `max_stops` allowed, `layover_limit`, `max_trip_price`.

### Example search

Return trip from WUE to JBN, where I want to spend 4 days and I don't want to fly through NNB or ZRW:

`python3 solution.py examples3.csv WUE JBN --return --days-in-destination 4 --exclude NNB ZRW`

### CLI help

```
usage: solution.py [-h] [--return] [--max-stops MAX_STOPS]
                   [--days-in-destination DAYS_IN_DESTINATION]
                   [--max-trip-price MAX_TRIP_PRICE]
                   [--layover-limit LAYOVER_LIMIT] [--bags BAGS]
                   [--max-bag-price MAX_BAG_PRICE]
                   [--trip-start-time TRIP_START_TIME]
                   [--trip-return-time TRIP_RETURN_TIME]
                   [--exclude EXCLUDE [EXCLUDE ...]]
                   data [data ...] origin destination

Process parameters for trip search.

positional arguments:
  data                  Name(s) or path(s) to dataset(s) with available
                        flights.
  origin                Origin airport code.
  destination           Destination airport code.

optional arguments:
  -h, --help            show this help message and exit
  --return              Is it a return flight?
  --max-stops MAX_STOPS
                        Maximum number of stops for oneway trip. If --return
                        used, limit is also applied to return journey.
  --days-in-destination DAYS_IN_DESTINATION
                        Applicable only with --return. Indicates how many days
                        should be between arrival to destination and return
                        flight.
  --max-trip-price MAX_TRIP_PRICE
                        Number representing maximum trip price. If --return
                        used, then price limit is applied to whole trip
                        (including the flighs back).
  --layover-limit LAYOVER_LIMIT
                        Maximum hours spent in layover. Defaults to 6 hours
                        (minimum is 1 hour).
  --bags BAGS           Number of requested bags.
  --max-bag-price MAX_BAG_PRICE
                        Number representing maximum price for one bag in one
                        flight.
  --trip-start-time TRIP_START_TIME
                        Earliest datetime for departure from origin airport.
                        Input must be in datetime format ->
                        2021-09-09T20:10:00.
  --trip-return-time TRIP_RETURN_TIME
                        Earliest datime for departure from destination
                        airport. Input must be in datetime format ->
                        2021-09-09T20:10:00 This parameter works only in
                        combination with --return option.
  --exclude EXCLUDE [EXCLUDE ...]
                        Airports to exclude from trip. Input them as IATA
                        3-letter codes.
```
