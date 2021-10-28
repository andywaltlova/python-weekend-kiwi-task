from core import Flight

import argparse


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Process csv with flighs.')
    parser.add_argument('data', type=str,
                        help='Name(s) or path(s) to dataset(s) with available flights.')
    parser.add_argument('origin', type=str, help='Origin airport code.')
    parser.add_argument('destination', type=str,
                        help='Destination airport code.')
    parser.add_argument('--bags', type=int, required=False, default=0,
                        help='Number of requested bags.')
    parser.add_argument('--return', action='store_true', dest='return_requested',
                        required=False, help='Is it a return flight?')
    parser.add_argument('--max-trip-price', type=int, required=False,
                        help='Number representing maximal price of trip.')
    parser.add_argument('--max-bag-price', type=int, required=False,
                        help='Number representing maximal price of bag.')
    parser.add_argument('--passengers', type=int, required=False,
                        help='Number of passengers for trip.')
    parser.add_argument('--max-stops', type=int, required=False,
                        help='Maximal number of stops for trip. If return is specified, this number is also applied to return journey.')
    parser.add_argument('--exclude', required=False,
                        help='Airports to exclude from trip.')
    # add stopover - default from assignment should not be less than 1 hour and more than 6 hours
    # add limit to days for traveling
    # add time from limit flights (flight not earlier than)

    return parser


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
