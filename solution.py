from trip_search.core import SearchEngine
from trip_search.utils import load_data,validate_args, init_parser


if __name__ == '__main__':
    parser = init_parser()
    args = parser.parse_args()
    validate_args(args)

    engine = SearchEngine(parameters=vars(args))

    flights = load_data(args.data)
    engine.search(flights, args.origin, args.destination)

    print(engine.get_output())
