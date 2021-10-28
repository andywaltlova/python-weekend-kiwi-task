from trip_search.core import SearchEngine
from trip_search.helpers import load_data, init_parser


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    # print(args)

    flights = load_data(args.data)
    engine = SearchEngine(flights, **vars(args))
    engine.search()
    print(engine.get_output())
