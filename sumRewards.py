import auth
import requests
import ast
import webbrowser
import json
import urllib
import time

def sumRewards(auth_code):
	rewardsTotal = {}	
	access_token_money = auth.authorize("money_movement")["access_token"]
	client_id = "enterpriseapi-sb-tJOw55ype3LktRNB5zY7oIHq"
	client_secret = "175384eb1888f2dded491e8d7242398f0c5901db"
	redirect_uri = "https://developer.capitalone.com/products/playground"

	##Money Transfer Info ######
	url = "https://api-sandbox.capitalone.com/money-movement/accounts"

	headers = {
	    'authorization': "Bearer " + access_token_money,
	    'accept': "application/json;v=0",
	    'cache-control': "no-cache",
	    'postman-token': "65c0519f-28f0-ed9f-30eb-8b4adf7ac7fa"
	    }

	response = requests.request("GET", url, headers=headers)
	account_hash = ast.literal_eval(response.text)

	### Rewards Info ####
	#access_token_rewards = "84b2d1f04c524be32630921e989e1954c"
	##Money Transfer Info ######
	
	###Get Access Code TESTING
	url = "https://api-sandbox.capitalone.com/oauth2/token"
	payload = "code=" + auth_code + "&client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=authorization_code&redirect_uri=" + redirect_uri
	headers = {
		"content-type": "application/x-www-form-urlencoded",
	    }

	response = requests.request("POST", url, data=payload, headers=headers)
	rewards_hash = ast.literal_eval(response.text)

	access_token_rewards = rewards_hash["access_token"]
	refresh_token_rewards = rewards_hash["refresh_token"]
	#access_token_rewards = auth.authorize("rewards")["access_token"]
	

	url = "https://api-sandbox.capitalone.com/rewards/accounts"

	headers = {
	    'authorization': "Bearer " + access_token_rewards,
	    'accept': "application/json;v=1",
	    'accept-language': "en-US",
	    }

	response1 = requests.request("GET", url, headers=headers)
	rewards_hash = json.loads(response1.text)

	##Find rewards ID and the rewards currency
	for account in rewards_hash["rewardsAccounts"]:
		for infoType in account:
			if (type(account[infoType]) == dict) and ("lastFour" in account[infoType].keys()):
				lastFour = account[infoType]["lastFour"]
				#print (lastFour)
				rewardsTotal[lastFour] = {}
				rewardsTotal[lastFour]["rewardsAccountReferenceId"] = account["rewardsAccountReferenceId"]
	##Refresh token
	url = "https://api-sandbox.capitalone.com/oauth2/token"
	payload = "client_id=" + client_id + "&client_secret=" + client_secret + "&grant_type=refresh_token&refresh_token="+refresh_token_rewards
	headers = {
		"content-type": "application/x-www-form-urlencoded"
	    }

	response = requests.request("POST", url, data=payload, headers=headers)
	rewards_hash = json.loads(response.text)
#	print ("######")
#	print (rewardsTotal)
	access_token_rewards = rewards_hash["access_token"]

	url = "https://api-sandbox.capitalone.com/rewards/accounts/"
	#Find Reward balance
	for card in rewardsTotal:
		refid = urllib.parse.quote_plus(rewardsTotal[card]["rewardsAccountReferenceId"])
		url = "https://api-sandbox.capitalone.com/rewards/accounts/" + refid
		headers={
		    'authorization': "Bearer " + access_token_rewards,
		    'accept': "application/json;v=1",
		    'accept-language': "en-US"
		}
		response = requests.request("GET", url, headers=headers)
		rewards_hash = json.loads(response.text)
#		print (card)
#		print ("PER CARD *******")
#		print (rewards_hash)

		if rewards_hash["canRedeem"] == True:
			for redemptionCategory in rewards_hash["redemptionOpportunities"]:
				if redemptionCategory["category"] == "Travel":
					rewardsCurrency = rewards_hash["rewardsCurrency"]
					rewardsTotal[card][rewardsCurrency] = rewards_hash["rewardsBalance"]
					rewardsTotal[card]["Cash Equivalent"] = redemptionCategory["cashValue"]
		else:
			rewardsTotal[card]["Cash Equivalent"] = 0

	#Current available balance
	for account in account_hash["accounts"]:
		rewardsTotal[account["lastFourAccountNumber"]] = {}
		#print ("ACCOUNT")
		#print (account)
		for infoType in account:
			if infoType == "availableBalance":
				rewardsTotal[account["lastFourAccountNumber"]]["Balance"] = account["availableBalance"]
				break
	#print (rewardsTotal)
	return rewardsTotal

sumRewards("cc7624f4421a46cfaddac68f2d4d9431")