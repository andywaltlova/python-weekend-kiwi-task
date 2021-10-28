from trip_search.core import SearchEngine
from trip_search.helpers import load_data, init_parser


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    print(args)

    flights = load_data(args.data)
    print(flights)
    # engine = SearchEngine(flights, **vars(args))

    # engine.construct_routes(args.origin)
    # engine.search(args.origin, args.destination)
    # print(engine.get_output())
