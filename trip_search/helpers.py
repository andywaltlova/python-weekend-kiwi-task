from .core import Flight

import argparse
import csv
from datetime import datetime


def load_data(paths: list[str]) -> list[Flight]:
    '''Load flights from csv files.'''

    result = []
    for path in paths:
        result += load_one_file(path)
    return result

def load_one_file(path) -> list[Flight]:
    with open(path, newline='') as file:
        reader = csv.DictReader(file)
        try:
            return [Flight(**row) for row in reader]
        except ValueError as error:
            print(
                f'[ERROR] Missing or invalid value in source file `{path}`.')
            print(f'  -> {error}')
            exit(1)

def validate_args(args: argparse.Namespace) -> None:
    if args.origin in args.exclude or args.destination in args.exclude:
        print('Cannot exclude origin or destination airports.')
        exit(1)

    trip_start = args.trip_start_time
    trip_end = args.trip_return_time
    try:
        if trip_start:
            trip_start = datetime.strptime(trip_start, '%Y-%m-%dT%H:%M:%S')
        if trip_end:
            trip_end = datetime.strptime(trip_end, '%Y-%m-%dT%H:%M:%S')
        if trip_start and trip_end and trip_start >= trip_end:
            print(f'--trip-start-time cannot be bigger than --trip-return-time.')
            exit(1)
    except ValueError as error:
        print(f'Invalid format of datetime arguments: {error}.')
        exit(1)
    
def init_parser() -> argparse.ArgumentParser:
    '''Initialize simple CLI for inputting parameters for trip search.'''

    parser = argparse.ArgumentParser(description='Process parameters for trip search.')

    # Positional
    parser.add_argument('data', action='extend', nargs='+', help='Name(s) or path(s) to dataset(s) with available flights.')
    parser.add_argument('origin', type=str, help='Origin airport code.')
    parser.add_argument('destination', type=str, help='Destination airport code.')

    # Optional dynamic -> must be applied during search
    # TODO solve infinite loop on third example file
    parser.add_argument('--return', action='store_true', dest='return_trip', required=False, help='Is it a return flight?')
    parser.add_argument('--max-trip-price', type=int, required=False, help='Number representing maximal price of trip. If --return used, then price limit is applied to whole trip (including the flighs back).')
    # TODO combine with return
    parser.add_argument('--max-stops', type=int, required=False, help='Maximal number of stops for oneway trip. If --return used, limit is also applied to return journey.')
    # TODO combine with return
    parser.add_argument('--layover-limit', type=float, required=False, default=6.0, help='Maximum hours spent in layover airport. Defaults to 6 hours (minimum is 1 hour).')
    # TODO availabe time in destination
    
    # Optional static -> flights can be filtered before search
    # TODO (look how it works on kiwi)
    parser.add_argument('--days', action='extend', nargs='+', required=False, default=list(range(1, 8)), help='Days in which you are willing to travel. Use 1-7 values to indicate day (1=Monday, 2=Tuesday ...).')
    parser.add_argument('--bags', type=int, required=False, default=0, help='Number of requested bags.')
    parser.add_argument('--exclude', action='extend', nargs='+', default=[], required=False, help='Airports to exclude from trip.')
    parser.add_argument('--max-bag-price', type=int, required=False, help='Number representing maximal price for one bag in one flight.')
    

    input_format = 'Input must be in `%Y-%m-%dT%H:%M:%S` format (e.g. 2021-09-09T20:10:00).'
    parser.add_argument('--trip-start-time', required=False,
                        help=f'Earliest datetime for departure from origin airport. {input_format}.')
    ignore_if_oneway = 'This parameter works only in combination with --return option.'
    parser.add_argument('--trip-return-time', required=False,
                        help=f'Earliest datime for departure from destination airport. {input_format} {ignore_if_oneway}')

    return parser
