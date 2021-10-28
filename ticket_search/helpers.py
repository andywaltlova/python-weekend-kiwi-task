from core import Flight


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
