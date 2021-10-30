from trip_search.core import SearchEngine
from trip_search.helpers import load_data, init_parser


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    engine = SearchEngine(parameters=vars(args))

    flights = load_data(args.data)
    engine.search(flights, args.origin, args.destination)
    [print(t) for t in engine.paths]
    # print(engine.get_output())
