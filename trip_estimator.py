import sys
import argparse
from flight_price import flight_price
from hotel_price import hotel_price
from food_price import food_price

def estimate_trip_cost(from_city, to_city, num_days):

    cost_estimate = dict()
    cost_estimate['from'] = from_city
    cost_estimate['to'] = to_city
    cost_estimate['flight_cost'] = flight_price(from_city, to_city)
    cost_estimate['hotel_cost'] = hotel_price(to_city) * max(num_days, 0)
    cost_estimate['food_cost'] = food_price(to_city) * max(num_days, 0) * 2

    return cost_estimate

def build_parser():
    parser = argparse.ArgumentParser(description='Estimate trip cost with given cities and number of days')
    parser.add_argument('--from', '-f', dest='from_city', help='Trip from city')
    parser.add_argument('--to', '-t', dest='to_city', help='Trip to city')
    parser.add_argument('--days', '-d', dest='num_days', help='Number of days for staying')
    return parser

if __name__ == '__main__':
    parser = build_parser()

    if len(sys.argv) != 4:
        parser.print_help()
        exit()

    args = parser.parse_args()

    from_city = args.from_city
    to_city = args.to_city
    num_days = int(args.num_days)

    if from_city is None or to_city is None or num_days is None:
        print('Invalid input!')
    else:
        print('Cost Estimate for travelling from {} to {} is: '.format(from_city, to_city))
        d = estimate_trip_cost(from_city, to_city, num_days)
        total_price = sum([d[k] for k in d if isinstance(d[k], (int, float))])
        print('Total price: ${:.2f}'.format(total_price))
        print()
        # print(d)
        sys.stdout.flush()