from .core import Flight

import argparse
import csv


def load_data(paths: list[str]) -> list[Flight]:
    '''Load flights from csv files.'''

    result = []
    for path in paths:
        with open(path, newline='') as file:
            reader = csv.DictReader(file)
            try:
                result += [Flight(**row) for row in reader]
            except ValueError:
                print(
                    f'[ERROR] Missing or invalid value in source file `{path}`.')
                exit(1)
    return result


def init_parser() -> argparse.ArgumentParser:
    '''Initialize simple CLI for inputting parameters for trip search.'''

    parser = argparse.ArgumentParser(
        description='Process parameters for trip search.')

    # Positional
    parser.add_argument('data', action='extend', nargs='+',
                        help='Name(s) or path(s) to dataset(s) with available flights.')
    parser.add_argument('origin', type=str, help='Origin airport code.')
    parser.add_argument('destination', type=str,
                        help='Destination airport code.')

    # TODO
    # Optional dynamic -> must be applied in search itself
    parser.add_argument('--return', action='store_true', dest='return_requested',
                        required=False, help='Is it a return flight?')
    parser.add_argument('--max-trip-price', type=int, required=False,
                        help='Number representing maximal price of trip.')
    parser.add_argument('--passengers', type=int, required=False,
                        help='Number of passengers for trip.')
    parser.add_argument('--max-stops', type=int, required=False,
                        help='Maximal number of stops for trip. If return is specified, this number is also applied to return journey.')
    parser.add_argument('--layover-limit', type=float, required=False, default=6.0,
                        help='Maximum hours spent in layover airport. Defaults to 6 hours (minimum is 1 hour).')

    # TODO
    # Optional static -> flights can be filtered before search
    parser.add_argument('--bags', type=int, required=False, default=0,
                        help='Number of requested bags.')
    parser.add_argument('--exclude', action='extend', nargs='+', required=False,
                        help='Airports to exclude from trip.')
    parser.add_argument('--max-bag-price', type=int, required=False,
                        help='Number representing maximal price for one bag in one flight for one passenger.')
    parser.add_argument('--days', action='extend', nargs='+', required=False, default=list(range(1, 8)),
                        help='Days in which you are willing to travel. Use 1-7 values to indicate day (1=Monday, 2=Tuesday ...).')
    parser.add_argument('--trip-start', required=False,
                        help='Earliest time for departure from origin airport. Input must be in `%Y-%m-%dT%H:%M:%S` format (e.g. 2021-09-09T20:10:00).')
    parser.add_argument('--trip-end', required=False,
                        help='Latest time for your arrival to destination airport. Input must be in `%Y-%m-%dT%H:%M:%S` format (e.g. 2021-09-09T20:10:00).')

    return parser
