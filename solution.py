from ticket_search.parser import init_parser
from ticket_search.core import SearchEngine
from ticket_search.helpers import load_data


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    # print(args)

    flights = load_data(args.data)
    engine = SearchEngine(flights, **vars(args))
