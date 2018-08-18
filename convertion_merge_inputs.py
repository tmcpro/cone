import json
import sys
import argparse
from flight_price import flight_price
from hotel_price import hotel_price
from food_price import food_price
# import 

import auth
import requests
import ast
import webbrowser
import json
import urllib
import time

import sumRewards
import trip_estimator

#TO DO: 

#Parse the input JSON file 

#Add plotting for all graphs and estimates
#sally's function for authcode from Ivan
#ken's function for from, to, days from Ivan
#
def parse_and_convert(starting_city, ending_city, days, authentication):
	travel_cost_string = trip_estimator.estimate_trip_cost(starting_city, ending_city, days)
	intermediate_string = sumRewards.sumRewards(authentication)


	total_rewards = 0
	for account in intermediate_string:
		if "Cash_Equivalent" in intermediate_string[account]:

			total_rewards += intermediate_string[account]["Cash_Equivalent"]

	total_balance = 0
	for account in intermediate_string:
		
		if "Balance" in intermediate_string[account]:

			total_balance += intermediate_string[account]["Balance"]

		# for   in account:
	print("This is the account info: ", account)
	print("This is the total rewards worth: ", total_rewards)
	print("This is the total Balance we have: ", total_balance)
	account_info = {"total_balance": total_balance, "total_rewards": total_rewards}


	rewards_usable_expense_combined = travel_cost_string["flight_cost"] + travel_cost_string["hotel_cost"]
	total_rewards_available = account_info["total_rewards"]

	food_cost = travel_cost_string["food_cost"]
	total_balance_available = account_info["total_balance"]

	total_expense_everything_combined = rewards_usable_expense_combined + food_cost
	total_value_everything_combined = total_rewards_available + total_balance_available

	

	#can go with just rewards and enough for food
	if total_rewards_available >= rewards_usable_expense_combined and total_balance_available >= food_cost:
		return {"Return_code": 0, "rewards_usable_expense_combined": rewards_usable_expense_combined,"total_rewards_available": total_rewards_available,"food_cost": food_cost,"total_balance_available": total_balance_available,"total_expense_everything_combined": total_expense_everything_combined,"total_value_everything_combined": total_value_everything_combined}

	#can go with rewards but not enough for food
	elif total_rewards_available >= rewards_usable_expense_combined and total_balance_available < food_cost:
		return {"Return_code": 1, "rewards_usable_expense_combined": rewards_usable_expense_combined,"total_rewards_available": total_rewards_available,"food_cost": food_cost,"total_balance_available": total_balance_available,"total_expense_everything_combined": total_expense_everything_combined,"total_value_everything_combined": total_value_everything_combined}

	#cannot go with rewards but enough for food
	elif total_rewards_available < rewards_usable_expense_combined and total_balance_available >= food_cost:
		return {"Return_code": 2, "rewards_usable_expense_combined": rewards_usable_expense_combined,"total_rewards_available": total_rewards_available,"food_cost": food_cost,"total_balance_available": total_balance_available,"total_expense_everything_combined": total_expense_everything_combined,"total_value_everything_combined": total_value_everything_combined}

	#cannot go with rewards and not enough for food 
	elif total_rewards_available < rewards_usable_expense_combined and total_balance_available < food_cost:
		return {"Return_code": 3, "rewards_usable_expense_combined": rewards_usable_expense_combined,"total_rewards_available": total_rewards_available,"food_cost": food_cost,"total_balance_available": total_balance_available,"total_expense_everything_combined": total_expense_everything_combined,"total_value_everything_combined": total_value_everything_combined}


#FOR IVAN::::::::::::::::::::::::::::::::::::::::::::::::::::prompt the user for inputs


#input: dictionary: the comparison results, int: results from porompting the user for yearly rewards and yearly income
#output: a list of 2 elements [return code, num of days it would take]
def interpret(input_return_code_and_info, user_input_cash, user_input_cash_equivalent_rewards):


	#use up this much amount of rewards and balance
	if input_return_code_and_info["Return_code"] == 0:
		print("You will use up: " + str(rewards_usable_expense_combined/total_rewards_available) + "%" + " of your rewards and " + str(food_cost/total_balance_available) + "%" + " of your balance")
		return [0, 0]

	#how much cash you need and how much do you project to earn each year
	elif input_return_code_and_info["Return_code"] == 1:


		cash_per_day = user_input_cash/365

		cash_needed = input_return_code_and_info["food_cost"] - input_return_code_and_info["total_balance_available"]
		num_of_days_it_takes = int(cash_needed/cash_per_day)



		# int(in)
		return [1, num_of_days_it_takes]


	#check combined to see if enough. And if just want to use rewards, you need to wait for this long based on user input
	elif input_return_code_and_info["Return_code"] == 2:

		if(input_return_code_and_info["total_expense_everything_combined"] < input_return_code_and_info["total_value_everything_combined"]):
			print("You can go with your cash and rewards combined")


			print("If you only want to use your rewards, it would take: ")
			rewards_equivalent_per_day = user_input_cash_equivalent_rewards/365
			rewards_needed = input_return_code_and_info["rewards_usable_expense_combined"] - input_return_code_and_info["total_rewards_available"]
			num_of_days_it_takes = int(rewards_needed/rewards_equivalent_per_day)


		#with just rewards if combined is not enough
		else:
			rewards_equivalent_per_day = user_input_cash_equivalent_rewards/365
			rewards_needed = input_return_code_and_info["rewards_usable_expense_combined"] - input_return_code_and_info["total_rewards_available"]
			num_of_days_it_takes = int(rewards_needed/rewards_equivalent_per_day)

		return [2, num_of_days_it_takes]

	#check how much user earns for miles and balance amount each year, project how long it takes to use rewards and cash or just rewards
	elif input_return_code_and_info["Return_code"] == 3:


		cash_and_rewards_per_day = (user_input_cash + user_input_cash_equivalent_rewards)/365
		cash_and_rewards_combined_needed = input_return_code_and_info["total_expense_everything_combined"] - input_return_code_and_info["total_value_everything_combined"]
		num_of_days_it_takes = int(cash_and_rewards_combined_needed/cash_and_rewards_per_day)
		return [3, num_of_days_it_takes]



