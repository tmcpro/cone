
import json

import matplotlib.pyplot as plt
plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
plt.show()

# import account_info


#TO DO: 

#Parse the input JSON file 

#Add plotting for all graphs and estimates
#Add if they wanna plan for all cases where they do not have enough
#Add create accounts if they want to
#Check for "points", "miles", "cash", "cash equivalent"



with open('travel_expense.json', 'r') as travel_cost:
	travel_cost_string = json.load(travel_cost)
	travel_cost.close()

with open('test_data.json', 'r') as intermediate:
	intermediate_string = json.load(intermediate)
	intermediate.close()



miles_convert_to_dollars = 0.014




def converter(input_json_data):

	total_mileage = 0
	for account in input_json_data:

		total_mileage += input_json_data[account]["Miles"]


	total_miles_convertion_value = total_mileage*miles_convert_to_dollars

	total_dollars = 0
	for account in input_json_data:

		total_dollars += input_json_data[account]["Dollars"]

		# for   in account:
	print("This is the total mileage available: ", account)
	print("This is the account data: ", total_dollars)
	print("This is the total miles we have: ", total_miles_convertion_value)

	return {"total_dollars": total_dollars, "total_mileage" : total_mileage, "total_miles_convertion_value": total_miles_convertion_value}



def comparison(account_info, travel_expense_info):

	flight_difference = account_info["total_miles_convertion_value"] - travel_expense_info["flight_cost"]
	food_hotel_difference = account_info["total_dollars"] - (travel_expense_info["hotel_cost"] + travel_expense_info["food_cost"])

	if flight_difference >= 0 and food_hotel_difference >= 0:
		print("You can fly with just your rewards and you can also afford housing and food")

		# food_hotel_difference = account_info["total_dollars"] - (travel_expense_info["hotel_cost"] + travel_expense_info["food_cost"])
		# if food_hotel_difference >= 0:

	elif flight_difference >= 0 and food_hotel_difference < 0:
		print("You can fly with just your rewards but you cannot afford housing and food. Please do not go")

	elif flight_difference < 0 and food_hotel_difference < 0:
		print("You cannot fly with just your rewards and you cannot afford housing and food. Please do not go")

	elif flight_difference < 0 and food_hotel_difference >= 0:
		print("You cannot fly with just your rewards but you can afford housing and food. Do you want to check if you can fly with your mileage and cash combined?")
		# print("Please enter 0 or 1, 0 for checking to combine mileage and cash, 1 for not checking")
		going_or_not = int(input("Please enter 0 or 1, 0 for checking to combine mileage and cash, 1 for not checking: "))
		if going_or_not == 0:
			new_flight_difference = account_info["total_dollars"] + account_info["total_miles_convertion_value"] - travel_expense_info["flight_cost"] - (travel_expense_info["hotel_cost"] + travel_expense_info["food_cost"])
			if new_flight_difference >= 0:

				#check % to see if actually still going
				print("Congrats!!! You can go with cash and mileage")
			else:

				#let's save up on this! create account and this is the projection
				print("You cannot go even with both cash and mileage currently. We can help you set up an account and help you with additional analysis. Would you like that?")
				projection_and_set_up_account = int(input("Please enter 0 or 1, 0 for setting it up, 1 for quitting this app: "))

				if projection_and_set_up_account == 0:


					# print("You cannot go even with both cash and mileage currently. We can help you set up an account and help you with additional analysis. Would you like that?")
					both_or_only_rewards = int(input("Please enter 0, 1, or 2, 0 for going with only rewards, 1 for going with both rewards and cash, 2 for displaying both results: "))
					if both_or_only_rewards == 0:


						miles_per_year = int(input("We would need a bit more info! Please enter the estimated miles you earn every year "))
						miles_per_day = miles_per_year/365
						values_per_day = miles_per_day * miles_convert_to_dollars
						positive_flight_difference = abs(new_flight_difference)
						num_of_days_it_takes = int(positive_flight_difference/values_per_day)

						plotting_array = []
						current_value = account_info["total_mileage"]
						while current_value < (travel_expense_info["flight_cost"]/miles_convert_to_dollars):
							current_value += miles_per_day
							plotting_array.append(current_value)



						plt.plot(plotting_array)
						plt.ylabel('some numbers')
						plt.show()

						print("It would take around " + str(num_of_days_it_takes) + " days")



					elif both_or_only_rewards == 1:

						miles_per_year = int(input("We would need a bit more info! Please enter the estimated miles you earn every year "))
						dollars_per_year = int(input("We would need a bit more info! Please enter the estimated number of dollars you earn every year "))

						miles_per_day = miles_per_year/365
						dollars_per_day = dollars_per_year/365

						values_per_day = (miles_per_day * miles_convert_to_dollars) + dollars_per_day

						positive_flight_difference = abs(new_flight_difference)
						num_of_days_it_takes = int(positive_flight_difference/values_per_day)
						print("It would take around " + str(num_of_days_it_takes) + " days")

					elif both_or_only_rewards == 2:


						miles_per_year = int(input("We would need a bit more info! Please enter the estimated miles you earn every year "))
						dollars_per_year = int(input("We would need a bit more info! Please enter the estimated number of dollars you earn every year "))

						miles_per_day = miles_per_year/365
						dollars_per_day = dollars_per_year/365

						values_per_day_with_only_miles = (miles_per_day * miles_convert_to_dollars)

						values_per_day = (miles_per_day * miles_convert_to_dollars) + dollars_per_day

						positive_flight_difference_1 = abs(new_flight_difference)
						num_of_days_it_takes_1 = int(positive_flight_difference_1/values_per_day_with_only_miles)

						positive_flight_difference_2 = abs(new_flight_difference)
						num_of_days_it_takes_2 = int(positive_flight_difference_2/values_per_day)




						print("It would take around " + str(num_of_days_it_takes_1) + " days with only rewards")
						print("It would take around " + str(num_of_days_it_takes_2) + " days with both rewards and dollars earned")




				elif projection_and_set_up_account == 1:
					print("Thank you for using this app!")

		elif going_or_not == 1:
			print("Thank you for using this app!")





# converter(intermediate_string)
# print("This is the output: ", comparison(converter(intermediate_string), travel_cost_string))
comparison(converter(intermediate_string), travel_cost_string)





	#parsing


