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
    cost_estimate['food_price'] = food_price(to_city) * max(num_days, 0) * 2

    return cost_estimate

def build_parser():
    parser = argparse.ArgumentParser(description='Estimate trip cost with given cities and number of days')
    parser.add_argument('--from', dest='from_city', help='From City')
    parser.add_argument('--to', dest='to_city', help='To City')
    parser.add_argument('--days', dest='num_days', help='Number of days for staying')
    return parser

if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()

    from_city = args.from_city
    to_city = args.to_city
    num_days = int(args.num_days)

    if from_city is None or to_city is None or num_days is None:
        print('Invalid input!')
    else:
        print('Cost Estimate for travelling from {} to {} is: '.format(from_city, to_city))
        print(estimate_trip_cost(from_city, to_city, num_days))