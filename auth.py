import requests
import ast

def authorize(api):
	url = "https://api-sandbox.capitalone.com/oauth2/token"
	if api == "money_movement":
		payload = "client_id=83c59ee7d6a4479c8e142422cbe9022a&client_secret=6d5c0077c6d4e214c6850d5f1611689e&grant_type=client_credentials"
		headers = {
		    'content-type': "application/x-www-form-urlencoded",
		    'accept': "application/json",
		    'cache-control': "no-cache",
		    'postman-token': "fed54cf8-34ac-f4bb-3514-286a85e52384"
		    }
	elif api == "account_starter":
		payload = "client_id=cc2f96ed55c54755ac591e5e790146d8&client_secret=6c605ddbc36990f77c12f650e7b448cd&grant_type=client_credentials"
		headers = {
		    'content-type': "application/x-www-form-urlencoded",
		    'accept': "application/json",
		    'cache-control': "no-cache",
		    'postman-token': "5a905cc9-e837-b6ad-ab46-caa9b2c19322"
		    }
	elif api == "credit_offer":
		payload = "client_id=cc2f96ed55c54755ac591e5e790146d8&client_secret=6c605ddbc36990f77c12f650e7b448cd&grant_type=client_credentials"
		headers = {
		    'content-type': "application/x-www-form-urlencoded",
		    'accept': "application/json",
		    'cache-control': "no-cache",
		    'postman-token': "672d1046-d0b4-cd69-85c8-6a23636a63ff"
		    }
	else:
		print "UNDEFINED API"

	response = requests.request("POST", url, data=payload, headers=headers)
	data_hash = ast.literal_eval(response.text)

	return data_hash